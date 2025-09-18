#!/usr/bin/env python3
"""Chess Game Entry Point"""

import sys
import os

# Add src to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'src'))

from chess_game.main import main

if __name__ == "__main__":
    main()