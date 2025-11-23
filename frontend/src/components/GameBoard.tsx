import Disc from "./Disc";

interface Props {
  board: number[][];
  onColumnClick: (col: number) => void;
  lastMove: { row: number; col: number } | null;
  disabled: boolean;
}

export default function GameBoard({ board, onColumnClick, lastMove, disabled }: Props) {
  const isLastMove = (row: number, col: number) => {
    return lastMove?.row === row && lastMove?.col === col;
  };

  return (
    <div className="board-container">
      <div className="board">
        {board.map((row, rIdx) => (
          <div key={rIdx} className="row">
            {row.map((cell, cIdx) => (
              <div
                key={cIdx}
                className={`cell ${disabled ? 'disabled' : ''} ${isLastMove(rIdx, cIdx) ? 'last-move' : ''}`}
                onClick={() => !disabled && onColumnClick(cIdx)}
              >
                <Disc player={cell} />
              </div>
            ))}
          </div>
        ))}
      </div>
      
      {!disabled && (
        <div className="column-indicators">
          {Array(7).fill(0).map((_, idx) => (
            <div
              key={idx}
              className="column-indicator"
              onClick={() => onColumnClick(idx)}
            >
              ▼
            </div>
          ))}
        </div>
      )}
    </div>
  );
}