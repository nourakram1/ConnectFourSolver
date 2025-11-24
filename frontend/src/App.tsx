import { useState, useEffect } from "react";
import GameBoard from "./components/GameBoard";
import ControlPanel from "./components/ControlPanel";
import ScoreBoard from "./components/ScoreBoard";
import TreeModal from "./components/TreeModal";
import GameStatus from "./components/GameStatus";
import LiveScore from "./components/LiveScore";
import { solveMove } from "./api";

export default function App() {
  // Board state: 0 = empty, 1 = human (red), 2 = AI (yellow)
  const [board, setBoard] = useState<number[][]>(
    Array(6).fill(null).map(() => Array(7).fill(0))
  );
  const [algorithm, setAlgorithm] = useState("expectiminimax");
  const [depth, setDepth] = useState(4);
  const [prune, setPrune] = useState(true);
  const [aiPlayer, setAiPlayer] = useState(true);
  const [treeData, setTreeData] = useState(null);
  const [showTree, setShowTree] = useState(false);
  const [score, setScore] = useState({ human: 0, ai: 0, draws: 0 });
  const [currentPlayer, setCurrentPlayer] = useState<1 | 2>(1); // 1 = human, 2 = AI
  const [gameOver, setGameOver] = useState(false);
  const [liveHumanScore, setLiveHumanScore] = useState(0);
  const [liveAiScore, setLiveAiScore] = useState(0);
  const [isAiThinking, setIsAiThinking] = useState(false);
  const [lastMove, setLastMove] = useState<{ row: number; col: number } | null>(null);
  const [nodesExpanded, setNodesExpanded] = useState(0);
  const [evaluationValue, setEvaluationValue] = useState<number | null>(null);

  // Check if board is full
  const isBoardFull = (board: number[][]): boolean => {
    return board[0].every(cell => cell !== 0);
  };

  // Check if column is full
  const isColumnFull = (board: number[][], col: number): boolean => {
    return board[0][col] !== 0;
  };

  // Handle human move
  const handleHumanMove = (col: number) => {
    if (gameOver || currentPlayer !== 1 || isAiThinking || isColumnFull(board, col)) {
      return;
    }

    // Create a deep copy of the board
    const newBoard = board.map(row => [...row]);
    
    // Find the lowest empty row in the column
    for (let r = 5; r >= 0; r--) {
      if (newBoard[r][col] === 0) {
        newBoard[r][col] = 1;
        setLastMove({ row: r, col });
        setBoard(newBoard);

        // Check if board is full
        if (isBoardFull(newBoard)) {
          // Game over - trigger AI to get final scores
          setCurrentPlayer(2);
        } else {
          setCurrentPlayer(2);
        }
        break;
      }
    }
  };

  // Handle AI move
  const handleAiMove = async () => {
    if (currentPlayer !== 2 || isAiThinking || gameOver) return;

    setIsAiThinking(true);
    try {
      const result = await solveMove(board, algorithm, depth, prune, aiPlayer);
      setTreeData(result.tree);
      setNodesExpanded(result.nodes_expanded);
      setEvaluationValue(result.value);
      
      // Update live scores from backend
      setLiveHumanScore(result.HumanScore);
      setLiveAiScore(result.AiScore);

      // Check if game is over before making move
      const isFull = isBoardFull(board);

      if (result.best_col !== null && result.best_col >= 0 && result.best_col < 7 && !isFull) {
        // Create a deep copy of the board
        const newBoard = board.map(row => [...row]);
        
        // Find the lowest empty row in the column
        for (let r = 5; r >= 0; r--) {
          if (newBoard[r][result.best_col] === 0) {
            newBoard[r][result.best_col] = 2;
            setLastMove({ row: r, col: result.best_col });
            setBoard(newBoard);

            // Check if board is full after AI move
            if (isBoardFull(newBoard)) {
              setGameOver(true);
              
              // Update match score based on who won
              if (result.HumanScore > result.AiScore) {
                setScore(prev => ({ ...prev, human: prev.human + 1 }));
              } else if (result.AiScore > result.HumanScore) {
                setScore(prev => ({ ...prev, ai: prev.ai + 1 }));
              } else {
                setScore(prev => ({ ...prev, draws: prev.draws + 1 }));
              }
            } else {
              setCurrentPlayer(1);
            }
            break;
          }
        }
      } else if (isFull) {
        // Board is full, game over
        setGameOver(true);
        
        // Update match score based on who won
        if (result.HumanScore > result.AiScore) {
          setScore(prev => ({ ...prev, human: prev.human + 1 }));
        } else if (result.AiScore > result.HumanScore) {
          setScore(prev => ({ ...prev, ai: prev.ai + 1 }));
        } else {
          setScore(prev => ({ ...prev, draws: prev.draws + 1 }));
        }
      }
    } catch (error) {
      console.error("AI move failed:", error);
      alert("AI move failed. Please try again.");
      setCurrentPlayer(1);
    } finally {
      setIsAiThinking(false);
    }
  };

  // Auto-trigger AI move
  useEffect(() => {
    if (currentPlayer === 2 && !isAiThinking) {
      const timer = setTimeout(() => {
        handleAiMove();
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [currentPlayer, board]);

  // Reset game
  const resetGame = () => {
    setBoard(Array(6).fill(null).map(() => Array(7).fill(0)));
    setCurrentPlayer(1);
    setGameOver(false);
    setLiveHumanScore(0);
    setLiveAiScore(0);
    setLastMove(null);
    setTreeData(null);
    setNodesExpanded(0);
    setEvaluationValue(null);
  };

  const resetScore = () => {
    setScore({ human: 0, ai: 0, draws: 0 });
  };

  return (
    <div className="app">
      <div className="background-animation"></div>
      
      <div className="game-container">
        <div className="left-panel">
          <ScoreBoard score={score} onResetScore={resetScore} />
          <ControlPanel
            algorithm={algorithm}
            setAlgorithm={setAlgorithm}
            depth={depth}
            setDepth={setDepth}
            prune={prune}
            setPrune={setPrune}
            aiPlayer={aiPlayer}
            setAiPlayer={setAiPlayer}
            onShowTree={() => setShowTree(true)}
            hasTreeData={treeData !== null}
            nodesExpanded={nodesExpanded}
            evaluationValue={evaluationValue}
          />
        </div>

        <div className="center-panel">
          <header className="header">
            <h1 className="title">
              <span className="title-connect">CONNECT</span>
              <span className="title-four">4</span>
              <span className="title-ai">AI</span>
            </h1>
            <p className="subtitle">Advanced Game Theory & Decision Algorithms</p>
          </header>

          <GameStatus
            currentPlayer={currentPlayer}
            gameOver={gameOver}
            humanScore={liveHumanScore}
            aiScore={liveAiScore}
            isAiThinking={isAiThinking}
          />
          <GameBoard
            board={board}
            onColumnClick={handleHumanMove}
            lastMove={lastMove}
            disabled={gameOver || currentPlayer !== 1 || isAiThinking}
          />
          <button className="reset-button" onClick={resetGame}>
            <span className="button-icon">⟳</span>
            New Game
          </button>
        </div>

        <div className="right-panel">
          <LiveScore 
            humanScore={liveHumanScore} 
            aiScore={liveAiScore}
            gameOver={gameOver}
          />
          
          <div className="info-card">
            <h3>How to Play</h3>
            <ul>
              <li>Click any column to drop your red disc</li>
              <li>Game continues until board is full</li>
              <li>Winner has most Connect 4s at the end</li>
              <li>AI uses advanced algorithms to maximize connections</li>
            </ul>
          </div>
          
          <div className="info-card">
            <h3>Algorithms</h3>
            <p><strong>Minimax:</strong> Explores all possible moves assuming optimal play from both players</p>
            <p><strong>Expectiminimax:</strong> Models opponent as making random moves, useful for uncertainty</p>
            <p><strong>Alpha-Beta Pruning:</strong> Optimizes search by eliminating branches that won't affect the outcome</p>
          </div>
        </div>
      </div>

      {showTree && (
        <TreeModal
          data={treeData}
          onClose={() => setShowTree(false)}
          algorithm={algorithm}
          nodesExpanded={nodesExpanded}
        />
      )}
    </div>
  );
}