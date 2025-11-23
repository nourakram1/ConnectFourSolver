export interface SolveResponse {
  algorithm: string;
  best_col: number | null;
  value: number;
  nodes_expanded: number;
  tree: any;
}

export const solveMove = async (
  board: number[][],
  algorithm: string,
  depth: number,
  prune: boolean,
  aiPlayer: boolean
): Promise<SolveResponse> => {
  // Backend expects row 0 = bottom, row 5 = top
  // Frontend has row 0 = top, row 5 = bottom
  // So we need to reverse the rows
  const flippedBoard = [...board].reverse();
  
  console.log("Frontend board (row 0 = top):", board);
  console.log("Flipped board for backend (row 0 = bottom):", flippedBoard);
  
  const res = await fetch("/solve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      board: flippedBoard,
      algorithm,
      depth,
      prune,
      ai_player: aiPlayer
    })
  });
  
  if (!res.ok) {
    const error = await res.json();
    console.error("Backend error:", error);
    throw new Error(error.error || "Failed to solve");
  }
  
  const result = await res.json();
  console.log("Backend response:", result);
  return result;
};