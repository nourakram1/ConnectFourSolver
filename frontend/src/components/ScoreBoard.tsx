interface Props {
  score: { human: number; ai: number; draws: number };
  onResetScore: () => void;
}

export default function ScoreBoard({ score, onResetScore }: Props) {
  return (
    <div className="scoreboard">
      <h2 className="panel-title">Score</h2>
      
      <div className="score-grid">
        <div className="score-item human-score">
          <div className="score-label">Human</div>
          <div className="score-value">{score.human}</div>
        </div>
        
        <div className="score-item ai-score">
          <div className="score-label">AI</div>
          <div className="score-value">{score.ai}</div>
        </div>
        
        <div className="score-item draw-score">
          <div className="score-label">Draws</div>
          <div className="score-value">{score.draws}</div>
        </div>
      </div>

      <button className="reset-score-button" onClick={onResetScore}>
        Reset Score
      </button>
    </div>
  );
}