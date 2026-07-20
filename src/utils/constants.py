import os

# Board dimensions
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT_COLOR = (247, 247, 105, 150)
MOVE_HIGHLIGHT = (124, 252, 0, 150)
CHECK_HIGHLIGHT = (255, 0, 0, 150)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)

# Piece images
PIECE_IMAGES = {
    'P': 'wp.png', 'p': 'bp.png',
    'N': 'wn.png', 'n': 'bn.png',
    'B': 'wb.png', 'b': 'bb.png',
    'R': 'wr.png', 'r': 'br.png',
    'Q': 'wq.png', 'q': 'bq.png',
    'K': 'wk.png', 'k': 'bk.png'
}

def get_image_path(filename):
    """Get the absolute path to an image in the assets folder."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', filename)