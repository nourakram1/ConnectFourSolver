import { useState, useEffect } from "react";
import GameBoard from "./components/GameBoard";
import ControlPanel from "./components/ControlPanel";
import ScoreBoard from "./components/ScoreBoard";
import TreeModal from "./components/TreeModal";
import GameStatus from "./components/GameStatus";
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
  const [humanCount, setHumanCount] = useState(0);
  const [aiCount, setAiCount] = useState(0);
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

  // Count Connect 4s for a player
  const countConnect4s = (board: number[][], player: number): number => {
    let count = 0;

    // Check horizontal
    for (let row = 0; row < 6; row++) {
      for (let col = 0; col < 4; col++) {
        if (board[row][col] === player) {
          if (
            board[row][col] === board[row][col + 1] &&
            board[row][col] === board[row][col + 2] &&
            board[row][col] === board[row][col + 3]
          ) {
            count++;
          }
        }
      }
    }

    // Check vertical
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 7; col++) {
        if (board[row][col] === player) {
          if (
            board[row][col] === board[row + 1][col] &&
            board[row][col] === board[row + 2][col] &&
            board[row][col] === board[row + 3][col]
          ) {
            count++;
          }
        }
      }
    }

    // Check diagonal (top-left to bottom-right)
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 4; col++) {
        if (board[row][col] === player) {
          if (
            board[row][col] === board[row + 1][col + 1] &&
            board[row][col] === board[row + 2][col + 2] &&
            board[row][col] === board[row + 3][col + 3]
          ) {
            count++;
          }
        }
      }
    }

    // Check diagonal (bottom-left to top-right)
    for (let row = 3; row < 6; row++) {
      for (let col = 0; col < 4; col++) {
        if (board[row][col] === player) {
          if (
            board[row][col] === board[row - 1][col + 1] &&
            board[row][col] === board[row - 2][col + 2] &&
            board[row][col] === board[row - 3][col + 3]
          ) {
            count++;
          }
        }
      }
    }

    return count;
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
          const humanConnections = countConnect4s(newBoard, 1);
          const aiConnections = countConnect4s(newBoard, 2);
          
          setHumanCount(humanConnections);
          setAiCount(aiConnections);
          setGameOver(true);

          if (humanConnections > aiConnections) {
            setScore(prev => ({ ...prev, human: prev.human + 1 }));
          } else if (aiConnections > humanConnections) {
            setScore(prev => ({ ...prev, ai: prev.ai + 1 }));
          } else {
            setScore(prev => ({ ...prev, draws: prev.draws + 1 }));
          }
        } else {
          setCurrentPlayer(2);
        }
        break;
      }
    }
  };

  // Handle AI move
  const handleAiMove = async () => {
    if (gameOver || currentPlayer !== 2 || isAiThinking) return;

    setIsAiThinking(true);
    try {
      const result = await solveMove(board, algorithm, depth, prune, aiPlayer);
      setTreeData(result.tree);
      setNodesExpanded(result.nodes_expanded);
      setEvaluationValue(result.value);

      if (result.best_col !== null && result.best_col >= 0 && result.best_col < 7) {
        // Create a deep copy of the board
        const newBoard = board.map(row => [...row]);
        
        // Find the lowest empty row in the column
        for (let r = 5; r >= 0; r--) {
          if (newBoard[r][result.best_col] === 0) {
            newBoard[r][result.best_col] = 2;
            setLastMove({ row: r, col: result.best_col });
            setBoard(newBoard);

            // Check if board is full
            if (isBoardFull(newBoard)) {
              const humanConnections = countConnect4s(newBoard, 1);
              const aiConnections = countConnect4s(newBoard, 2);
              
              setHumanCount(humanConnections);
              setAiCount(aiConnections);
              setGameOver(true);

              if (humanConnections > aiConnections) {
                setScore(prev => ({ ...prev, human: prev.human + 1 }));
              } else if (aiConnections > humanConnections) {
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
    if (currentPlayer === 2 && !gameOver && !isAiThinking) {
      const timer = setTimeout(() => {
        handleAiMove();
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [currentPlayer, gameOver, board]);

  // Reset game
  const resetGame = () => {
    setBoard(Array(6).fill(null).map(() => Array(7).fill(0)));
    setCurrentPlayer(1);
    setGameOver(false);
    setHumanCount(0);
    setAiCount(0);
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
      
      <header className="header">
        <h1 className="title">
          <span className="title-connect">CONNECT</span>
          <span className="title-four">4</span>
          <span className="title-ai">AI</span>
        </h1>
        <p className="subtitle">Advanced Game Theory & Decision Algorithms</p>
      </header>

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
          <GameStatus
            currentPlayer={currentPlayer}
            gameOver={gameOver}
            humanCount={humanCount}
            aiCount={aiCount}
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