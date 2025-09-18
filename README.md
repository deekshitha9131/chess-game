# Chess Game

A Python chess game with GUI using Pygame and a chess AI with multiple difficulty levels.

## Features

- Interactive chess board with piece movement
- AI opponent with 3 difficulty levels (Beginner, Intermediate, Advanced)
- Pawn promotion handling
- Check and checkmate detection
- Undo move functionality
- Game restart and menu navigation

## Requirements

- Python 3.7+
- pygame
- python-chess

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

**For IDE users:** Use the play button on `src/chess_game/run_direct.py`

## How to Play

1. Select a difficulty level from the main menu
2. Click on a piece to select it (highlighted in yellow)
3. Click on a valid move square (shown with green dots) to move
4. The AI will automatically make its move after yours
5. Use the sidebar buttons to:
   - Undo your last move
   - Restart the current game
   - Return to the main menu

## Game Controls

- **Mouse Click**: Select pieces and make moves
- **Undo Button**: Undo the last move (undoes both player and AI moves)
- **Restart Button**: Start a new game with the same difficulty
- **Back to Menu**: Return to difficulty selection

## AI Difficulty Levels

- **Beginner**: Shallow search depth (1), 40% random moves
- **Intermediate**: Medium search depth (3), 10% random moves  
- **Advanced**: Deep search depth (4), deterministic play with positional evaluation

Enjoy playing chess!