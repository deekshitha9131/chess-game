# ♟️ Chess AI

A desktop chess application built with **Python**, **Pygame**, and **python-chess**, featuring a modular architecture and an AI opponent powered by **Minimax** with **Alpha-Beta Pruning**.

---

## Features

- ♟️ Interactive chess board with legal move validation
- 🤖 AI opponent with **3 difficulty levels**
- 🧠 Minimax search with Alpha-Beta pruning
- 📈 Piece-Square Table positional evaluation
- ⚡ Move ordering for faster search
- 📚 Built-in opening book
- 📊 Live AI statistics
  - Search depth
  - Evaluation score
  - Nodes searched
  - Search time
  - Best move
- 📝 Move history in SAN notation
- 📄 PGN export
- 🔄 Undo and restart game
- ♛ Pawn promotion
- ✅ Check, checkmate, and stalemate detection
- 🖥️ Background AI computation for a responsive UI

---

## AI Features

The chess engine includes:

- Minimax Algorithm
- Alpha-Beta Pruning
- Piece-Square Tables
- Move Ordering
- Opening Book
- Background Search Thread

---

## Tech Stack

- Python
- Pygame
- python-chess

---

## Project Structure

```
src/
├── assets/
├── core/
│   ├── ai.py
│   ├── game.py
│   └── opening_book.py
├── ui/
│   ├── board.py
│   ├── menu.py
│   ├── promotion.py
│   └── sidebar.py
└── utils/
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python main.py
```

---

## Controls

| Action | Control |
|---------|---------|
| Select Piece | Left Click |
| Move Piece | Left Click |
| Undo | Sidebar Button |
| Restart | Sidebar Button |
| Main Menu | Sidebar Button |

---

## Screenshots

> Screenshots will be added here.

---

## Future Improvements

- Sound effects
- Piece animations
- Unit tests
- GitHub Actions CI
- Additional opening lines

---

## License

This project is licensed under the MIT License.