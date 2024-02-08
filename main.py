import sys
import logging, sys
from engine import board

# Switch the log level to see game state as it plays the move
logging.basicConfig(stream=sys.stderr, format="%(message)s", level=logging.DEBUG)

for line in sys.stdin:
    trimmed_line = line.rstrip()
    logging.info('Processing line: %s', trimmed_line)
    game = board.Board(logger=logging.getLogger())
    sequence = trimmed_line.split(",")
    heights_sequence = game.play_sequence(sequence)
    last_height = None
    for height in heights_sequence:
        last_height = height
        game.print()
    print(last_height)