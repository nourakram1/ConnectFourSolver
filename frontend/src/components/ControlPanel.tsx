interface Props {
  algorithm: string;
  setAlgorithm: (algo: string) => void;
  depth: number;
  setDepth: (d: number) => void;
  prune: boolean;
  setPrune: (p: boolean) => void;
  aiPlayer: boolean;
  setAiPlayer: (ai: boolean) => void;
  onShowTree: () => void;
  hasTreeData: boolean;
  nodesExpanded: number;
  evaluationValue: number | null;
}

export default function ControlPanel({
  algorithm,
  setAlgorithm,
  depth,
  setDepth,
  prune,
  setPrune,
  aiPlayer,
  setAiPlayer,
  onShowTree,
  hasTreeData,
  nodesExpanded,
  evaluationValue
}: Props) {
  return (
    <div className="control-panel">
      <h2 className="panel-title">AI Configuration</h2>
      
      <div className="control-group">
        <label className="control-label">
          <span className="label-text">Algorithm</span>
          <select 
            value={algorithm} 
            onChange={e => setAlgorithm(e.target.value)}
            className="control-select"
          >
            <option value="minimax">Minimax</option>
            <option value="expectiminimax">Expectiminimax</option>
          </select>
        </label>
      </div>

      <div className="control-group">
        <label className="control-label">
          <span className="label-text">Search Depth: {depth}</span>
          <input
            type="range"
            min="1"
            max="8"
            value={depth}
            onChange={e => setDepth(Number(e.target.value))}
            className="control-slider"
          />
          <span className="range-labels">
            <span>1</span>
            <span>8</span>
          </span>
        </label>
      </div>

      <div className="control-group">
        <label className="control-checkbox">
          <input
            type="checkbox"
            checked={prune}
            onChange={e => setPrune(e.target.checked)}
          />
          <span className="checkbox-label">
            <span className="checkbox-custom"></span>
            Alpha-Beta Pruning
          </span>
        </label>
      </div>

      <div className="control-group">
        <label className="control-checkbox">
          <input
            type="checkbox"
            checked={aiPlayer}
            onChange={e => setAiPlayer(e.target.checked)}
            disabled
          />
        </label>
      </div>

      {nodesExpanded > 0 && (
        <div className="stats-display">
          <div className="stat-item">
            <span className="stat-label">Nodes Explored:</span>
            <span className="stat-value">{nodesExpanded.toLocaleString()}</span>
          </div>
          {evaluationValue !== null && (
            <div className="stat-item">
              <span className="stat-label">Evaluation:</span>
              <span className="stat-value">{evaluationValue.toFixed(2)}</span>
            </div>
          )}
        </div>
      )}

      <button
        className="tree-button"
        onClick={onShowTree}
        disabled={!hasTreeData}
      >
        <span className="button-icon">🌳</span>
        View Decision Tree
      </button>
    </div>
  );
}