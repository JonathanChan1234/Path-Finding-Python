from typing import Union, Dict, Optional, Tuple


class PathFindingState:
    """
    Data Structure
    {
       x: int,
       y: int,
       visited: int,
       debug_text: str,
       distance: float,
       visited: bool,
       previous: { x: int, y: int }
   }
    """
    def __init__(self,
                 x: int,
                 y: int,
                 visited: bool,
                 debug_text: str,
                 distance: Union[int, float],
                 previous: Optional[Tuple[int, int]]):
        self.x: int = x
        self.y: int = y
        self.visited = visited
        self.debug_text = debug_text
        self.distance = distance
        self.previous = previous
