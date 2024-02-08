from typing import List, Tuple

class Shape:
    # Shapes are represented by an array of tuple
    # Each tuple represent a coordinate where a block is present
    # Coordinates are (x, y) where x is the horizontal axis and y is vertical axis
    # Top left corner is the origin (0,0)
    def __init__(self, coordinates: List[Tuple[int]]):
        self.coordinates = coordinates
        self.xs = set(x for x, _ in coordinates)
        self.ys = set(y for _, y in coordinates)
        self.height = max(self.ys) + 1
        self.width = max(self.xs) - min(self.xs) + 1

    def profile(self):
        # The profile of a piece is an array
        profile = [None] * self.width
        for x, y in self.coordinates:
            if profile[x] is None or y + 1 > profile[x]:
                profile[x] = y + 1
        return profile

Shapes = {
    'Q': Shape([(0, 0), (1, 0), (0, 1), (1, 1)]),
    'Z': Shape([(0, 0), (1, 0), (1, 1), (2, 1)]),
    'S': Shape([(0, 1), (1, 0), (1, 1), (2, 0)]),
    'T': Shape([(0, 0), (1, 0), (1, 1), (2, 0)]),
    'I': Shape([(0, 0), (1, 0), (2, 0), (3, 0)]),
    'L': Shape([(0, 0), (0, 1), (0, 2), (1, 2)]),
    'J': Shape([(0, 2), (1, 0), (1, 1), (1, 2)])
}