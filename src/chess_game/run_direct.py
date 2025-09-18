"""Direct run script for IDE play button"""

import sys
import os

# Add parent directories to path for absolute imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(src_dir)

sys.path.insert(0, src_dir)
sys.path.insert(0, root_dir)

# Now we can import and run
from chess_game.main import main

if __name__ == "__main__":
    main()