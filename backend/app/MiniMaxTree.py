from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class MiniMaxTree:
    move: Optional[int] = None              # column that led to this node (None at root)
    player: Optional[bool] = None           # True=AI, False=Human, None=Chance
    value: float = 0.0                      # evaluated value of this node
    alpha: Optional[float] = None           # alpha value (for Minimax)
    beta: Optional[float] = None            # beta value (for Minimax)
    prob: float = 1.0                       # probability for chance outcomes
    depth: int = 0                          # depth from root
    children: List['MiniMaxTree'] = field(default_factory=list)

    def add_child(self, child: 'MiniMaxTree'):
        self.children.append(child)

    def to_json(self) -> Dict[str, Any]:
        """
        Convert TreeNode to a JSON-friendly structure for react-d3-tree.
        - Root is always MAX
        - Leaf nodes are VALUE nodes
        - Internal nodes show MAX/MIN/CHANCE
        """

        is_leaf = (len(self.children) == 0)

        if is_leaf:
            node_type = "VALUE"
        else:
            if self.depth == 0:
                node_type = "MAX"
            elif self.player is True:
                node_type = "MAX"
            elif self.player is False:
                node_type = "MIN"
            else:
                node_type = "CHANCE"

        name = f"{node_type}"

        attributes: Dict[str, Any] = {"value": f"{self.value:.2f}"}

        if self.depth != 0:
            attributes["col"] = f"{self.move}"
        if self.alpha is not None:
            attributes["alpha"] = f"{self.alpha:.2f}"
        if self.beta is not None:
            attributes["beta"] = f"{self.beta:.2f}"
        if self.prob != 1.0:
            attributes["prob"] = f"{self.prob:.2f}"

        return {
            "name": name,
            "attributes": attributes,
            "children": [child.to_json() for child in self.children]
        }
