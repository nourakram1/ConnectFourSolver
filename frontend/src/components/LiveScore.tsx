interface Props {
  humanScore: number;
  aiScore: number;
  gameOver: boolean;
}

export default function LiveScore({ humanScore, aiScore, gameOver }: Props) {
  return (
    <div className="live-score">
      <h2 className="panel-title">Current Game Score</h2>
      
      <div className="live-score-grid">
        <div className="live-score-box human-live">
          <div className="live-score-label">Human</div>
          <div className="live-score-value">{humanScore}</div>
        </div>
        
        <div className="live-score-box ai-live">
          <div className="live-score-label">AI</div>
          <div className="live-score-value">{aiScore}</div>
        </div>
      </div>

      {gameOver && (
        <div className={`game-result-badge ${
          humanScore > aiScore ? 'win' : 
          aiScore > humanScore ? 'lose' : 
          'draw'
        }`}>
          {humanScore > aiScore && "🎉 You Win!"}
          {aiScore > humanScore && "AI Wins!"}
          {humanScore === aiScore && "Draw!"}
        </div>
      )}
    </div>
  );
}