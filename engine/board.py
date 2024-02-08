import copy
from typing import List, Tuple
from engine.utils import substract_from_list
from engine.shapes import Shape, Shapes
import logging

class Board:
    """
    Represents a game of Tetris.

    This class provides methods to manipulate the game state, including dropping shapes.
    and clearing completed rows.
    The game is represented by a list of rows, each row is a list of int.
    1 represent the presence of a block, 0 means no block.

    As we can't move piece while they are dropping, when dropping pieces we only care about
    where is the highest piece in each column. To be compute efficient, we maintain this information in the 'profile'.

    Because new shapes can only ever drop as low as the lowest block in the profile, we don't have
    to keep track of the entire board. We can just keep track of the profile and the rows that are
    """
    def __init__(self, width: int = 10, logger: logging.Logger = logging.root):
        # Single row to start with
        self.width = width
        self.rows = [[0]*width for _ in range(100)]
        self.profile = copy.copy(self.rows[0])
        self.height_offset = 0
        self.logger = logger


    def get_profile(self, offset: int, width: int):
        return self.profile[offset:offset+width]

    def get_height(self):
        return max(self.profile) + self.height_offset

    def add_rows(self, n: int = 50):
        self.rows.extend([[0]*self.width for _ in range(n)])

    def play_move(self, move: str):
        self.logger.log(logging.DEBUG, "Playing move: %s", move)
        letter, dx_str = tuple(move)
        dx = int(dx_str)
        shape = Shapes[letter.upper()]
        if shape.height >= len(self.rows) - max(self.profile):
            self.add_rows()
        self.drop_shape_at(shape, dx)
        self.clear_complete_rows()
        self.drop_unreachable_rows()

    def play_sequence(self, sequence: List[str]):
        # Play sequence and return a generator that yield the resulting height after playing each move
        if sequence:
            # A move is a shape and dx position
            move = sequence.pop(0)
            self.play_move(move)
            yield self.get_height()
            yield from self.play_sequence(sequence)

    def drop_shape_at(self, shape: Shape, dx: int):
        # Find at which height the shape would drop
        # We only care about a subset area to calculate where/how it drops
        board_profile = self.get_profile(dx, shape.width)
        shape_profile = shape.profile()
        dy = 0
        for i in range(shape.width):
            if board_profile[i] + shape_profile[i] >= dy:
                dy = board_profile[i] + shape_profile[i]

        for x_block, y_block in shape.coordinates:
            self.rows[dy - y_block][dx + x_block] = 1
            self.profile[dx + x_block] = max(dy - y_block, self.profile[dx + x_block])

    def clear_complete_rows(self):
        # Clear complete rows
        previous_len = len(self.rows)
        self.rows = [row for row in self.rows if not all(row)]
        new_len = len(self.rows)
        if new_len < previous_len:
            self.profile = substract_from_list(self.profile, previous_len - new_len)

    def drop_unreachable_rows(self):
        # Every row that is below the lowest height in the profile is technically unreachable now
        # Drop everything below it and keep track using height_offset
        min_profile_height = min(self.profile)
        self.rows = self.rows[min_profile_height:]
        self.profile = substract_from_list(self.profile, min_profile_height)
        self.height_offset = self.height_offset + min_profile_height

    def print(self):
        # Print the board, allows to visualize the game state for debugging
        for y in range(max(self.profile), -1, -1):
            line = ""
            for x in range(self.width):
                line += '#' if self.rows[y][x] else ' '
            self.logger.log(logging.DEBUG, line)
