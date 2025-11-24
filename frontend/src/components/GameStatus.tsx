interface Props {
  currentPlayer: 1 | 2;
  gameOver: boolean;
  humanScore: number;
  aiScore: number;
  isAiThinking: boolean;
}

export default function GameStatus({ currentPlayer, gameOver, humanScore, aiScore, isAiThinking }: Props) {
  const getStatusMessage = () => {
    if (gameOver) {
      if (humanScore > aiScore) {
        return { 
          text: `🎉 You Win! ${humanScore} - ${aiScore}`, 
          class: "status-human-win" 
        };
      } else if (aiScore > humanScore) {
        return { 
          text: `AI Wins! ${aiScore} - ${humanScore}`, 
          class: "status-ai-win" 
        };
      } else {
        return { 
          text: `It's a Draw! ${humanScore} - ${aiScore}`, 
          class: "status-draw" 
        };
      }
    } else if (isAiThinking) {
      return { text: "AI is thinking...", class: "status-thinking" };
    } else if (currentPlayer === 1) {
      return { text: "Your Turn", class: "status-human-turn" };
    } else {
      return { text: "AI's Turn", class: "status-ai-turn" };
    }
  };

  const status = getStatusMessage();

  return (
    <div className={`game-status ${status.class}`}>
      <div className="status-text">{status.text}</div>
      {isAiThinking && (
        <div className="thinking-animation">
          <span></span>
          <span></span>
          <span></span>
        </div>
      )}
    </div>
  );
}