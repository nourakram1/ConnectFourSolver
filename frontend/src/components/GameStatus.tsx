interface Props {
  currentPlayer: 1 | 2;
  gameOver: boolean;
  humanCount: number;
  aiCount: number;
  isAiThinking: boolean;
}

export default function GameStatus({ currentPlayer, gameOver, humanCount, aiCount, isAiThinking }: Props) {
  const getStatusMessage = () => {
    if (gameOver) {
      if (humanCount > aiCount) {
        return { 
          text: `🎉 You Win! ${humanCount} vs ${aiCount}`, 
          class: "status-human-win" 
        };
      } else if (aiCount > humanCount) {
        return { 
          text: `AI Wins! ${aiCount} vs ${humanCount}`, 
          class: "status-ai-win" 
        };
      } else {
        return { 
          text: `It's a Draw! ${humanCount} vs ${aiCount}`, 
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