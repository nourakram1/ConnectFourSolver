import { useState, useRef, useEffect } from "react";
import Tree from "react-d3-tree";

interface Props {
  data: any;
  onClose: () => void;
  algorithm: string;
  nodesExpanded: number;
}

export default function TreeModal({ data, onClose, algorithm, nodesExpanded }: Props) {
  const [viewMode, setViewMode] = useState<"visual" | "json">("visual");
  const [translate, setTranslate] = useState({ x: 0, y: 0 });
  const treeContainerRef = useRef<HTMLDivElement>(null);

  // Center the tree on mount
  useEffect(() => {
    if (treeContainerRef.current) {
      const dimensions = treeContainerRef.current.getBoundingClientRect();
      setTranslate({
        x: dimensions.width / 2,
        y: 50,
      });
    }
  }, []);

  const getNodeColor = (nodeName: string) => {
    if (nodeName.includes("MAX")) {
      return "#ef4444"; // red for MAX
    } else if (nodeName.includes("MIN")) {
      return "#fbbf24"; // yellow for MIN
    } else if (nodeName.includes("CHANCE")) {
      return "#6366f1"; // purple for CHANCE
    }
    return "#94a3b8"; // gray default
  };

  const renderCustomNode = ({ nodeDatum, toggleNode }: any) => {
    const nodeColor = getNodeColor(nodeDatum.name);
    const hasChildren = nodeDatum.children && nodeDatum.children.length > 0;

    return (
      <g>
        {/* Node circle */}
        <circle
          r={25}
          fill={nodeColor}
          stroke="#fff"
          strokeWidth={3}
          onClick={toggleNode}
          style={{ cursor: hasChildren ? "pointer" : "default" }}
        />
        
        {/* Node name */}
        <text
          fill="#fff"
          strokeWidth="0"
          x="0"
          y="5"
          textAnchor="middle"
          style={{ 
            fontSize: "11px", 
            fontWeight: "bold",
            pointerEvents: "none"
          }}
        >
          {nodeDatum.name}
        </text>

        {/* Attributes box below node */}
        {nodeDatum.attributes && (
          <g>
            <rect
              x="-60"
              y="35"
              width="120"
              height={Object.keys(nodeDatum.attributes).length * 16 + 8}
              fill="rgba(30, 41, 59, 0.95)"
              stroke={nodeColor}
              strokeWidth="2"
              rx="5"
            />
            {Object.entries(nodeDatum.attributes).map(([key, value], idx) => (
              <text
                key={key}
                fill="#f1f5f9"
                strokeWidth="0"
                x="0"
                y={50 + idx * 16}
                textAnchor="middle"
                style={{ 
                  fontSize: "10px",
                  pointerEvents: "none"
                }}
              >
                {key}: {String(value as any)}
              </text>
            ))}
          </g>
        )}
      </g>
    );
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content tree-modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Decision Tree Visualization</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-info">
          <div className="info-item">
            <strong>Algorithm:</strong> {algorithm}
          </div>
          <div className="info-item">
            <strong>Nodes Expanded:</strong> {nodesExpanded.toLocaleString()}
          </div>
          <div className="info-item">
            <strong>Instructions:</strong> Drag to pan, scroll to zoom, click nodes to expand/collapse
          </div>
        </div>

        <div className="view-toggle">
          <button
            className={`toggle-btn ${viewMode === "visual" ? "active" : ""}`}
            onClick={() => setViewMode("visual")}
          >
            🌳 Visual Tree
          </button>
          <button
            className={`toggle-btn ${viewMode === "json" ? "active" : ""}`}
            onClick={() => setViewMode("json")}
          >
            📄 JSON View
          </button>
        </div>

        <div className="modal-body">
          {viewMode === "visual" ? (
            <div 
              className="tree-visualization-d3" 
              ref={treeContainerRef}
              style={{ width: "100%", height: "600px" }}
            >
              {data && (
                <Tree
                  data={data}
                  translate={translate}
                  orientation="vertical"
                  pathFunc="step"
                  separation={{ siblings: 1.5, nonSiblings: 2 }}
                  nodeSize={{ x: 180, y: 140 }}
                  renderCustomNodeElement={renderCustomNode}
                  svgClassName="custom-tree"
                  zoom={0.8}
                  scaleExtent={{ min: 0.1, max: 3 }}
                  enableLegacyTransitions
                  collapsible={true}
                  shouldCollapseNeighborNodes={false}
                  depthFactor={140}
                />
              )}
            </div>
          ) : (
            <pre className="json-view">{JSON.stringify(data, null, 2)}</pre>
          )}
        </div>

        <div className="tree-legend">
          <div className="legend-item">
            <div className="legend-color" style={{ background: "#ef4444" }}></div>
            <span>AI (MAX) - Maximizing player</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ background: "#fbbf24" }}></div>
            <span>Human (MIN) - Minimizing player</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ background: "#6366f1" }}></div>
            <span>Chance - Random outcomes</span>
          </div>
        </div>
      </div>
    </div>
  );
}