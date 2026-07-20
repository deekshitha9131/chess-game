from datetime import date
import threading
from typing import Any, Optional

import chess
import chess.pgn
from .ai import ChessAI


class ChessGame:
    _active_instance: Optional["ChessGame"] = None

    def __init__(self):
        self.board = None
        self.ai = None
        self.selected_square = None
        self.valid_moves = []
        self.game_over = False
        self.message = ""
        self.ai_thinking = False
        self.pending_ai_move: Optional[chess.Move] = None
        self.ai_thread: Optional[threading.Thread] = None
        self.move_history: list[str] = []
        self._last_exported_pgn = ""
        ChessGame._active_instance = self

    def start_new_game(self, level: str):
        self.board = chess.Board()
        self.ai = ChessAI(level)
        self.selected_square = None
        self.valid_moves = []
        self.game_over = False
        self.message = ""
        self.ai_thinking = False
        self.pending_ai_move = None
        self.ai_thread = None
        self.move_history = []
        self._last_exported_pgn = ""

    def make_move(self, move: chess.Move):
        if self.board and move in self.board.legal_moves:
            san_move = self.board.san(move)
            self.board.push(move)
            self.move_history.append(san_move)
            self._check_game_state()
            return True
        return False

    def undo_move(self):
        if self.board and len(self.board.move_stack) > 0:
            self.board.pop()
            if self.move_history:
                self.move_history.pop()
            if len(self.board.move_stack) > 0 and self.board.turn == chess.BLACK:
                self.board.pop()
                if self.move_history:
                    self.move_history.pop()
            self.game_over = False
            self.message = ""

    @classmethod
    def get_active_instance(cls) -> Optional["ChessGame"]:
        return cls._active_instance

    def get_ai_move(self):
        if self.ai and self.board:
            return self.ai.find_best_move(self.board)
        return None

    def start_ai_search(self) -> None:
        """Start a background thread to compute the AI move without blocking the UI."""
        if not self.ai or not self.board or self.ai_thinking or self.ai_thread is not None:
            return

        self.ai_thinking = True
        self.pending_ai_move = None

        def _worker() -> None:
            try:
                move = self.ai.find_best_move(self.board)
                self.pending_ai_move = move
            except Exception as exc:
                print(f"AI search error: {exc}")
                self.pending_ai_move = None
                self.ai_thinking = False
            finally:
                self.ai_thread = None

        self.ai_thread = threading.Thread(target=_worker, daemon=True)
        self.ai_thread.start()

    def apply_pending_ai_move(self) -> bool:
        """Apply the AI move from the worker thread safely on the main thread."""
        if not self.ai_thinking or self.ai_thread is not None:
            return False

        move = self.pending_ai_move
        self.pending_ai_move = None

        if move is None:
            self.ai_thinking = False
            return False

        if self.make_move(move):
            self.ai_thinking = False
            return True

        self.ai_thinking = False
        return False

    def get_ai_statistics(self) -> dict[str, Any]:
        if not self.ai:
            return {
                "difficulty": "--",
                "depth": "--",
                "evaluation": "--",
                "nodes": "--",
                "search_time": "--",
                "best_move": "--",
                "has_data": False,
            }

        return {
            "difficulty": self.ai.level.capitalize(),
            "depth": self.ai.depth,
            "evaluation": self.ai.last_evaluation if self.ai.has_completed_search else "--",
            "nodes": self.ai.nodes_searched if self.ai.has_completed_search else "--",
            "search_time": self.ai.last_search_time if self.ai.has_completed_search else "--",
            "best_move": self.ai.last_best_move_san or self.ai.last_best_move.uci() if self.ai.has_completed_search and self.ai.last_best_move else "--",
            "has_data": self.ai.has_completed_search,
        }

    def get_move_history_rows(self, max_half_moves: int = 16) -> list[tuple[int, Optional[str], Optional[str]]]:
        if not self.move_history:
            return []

        rows: list[tuple[int, Optional[str], Optional[str]]] = []
        for index in range(0, len(self.move_history), 2):
            white_move = self.move_history[index]
            black_move = self.move_history[index + 1] if index + 1 < len(self.move_history) else None
            rows.append(((index // 2) + 1, white_move, black_move))

        if len(rows) > max_half_moves // 2:
            rows = rows[-(max_half_moves // 2):]

        return rows

    def export_pgn(self) -> str:
        """Return the current game position as a PGN string."""
        if self.board is None:
            return ""

        game = chess.pgn.Game()
        game.headers["Event"] = "Local Game"
        game.headers["Date"] = date.today().strftime("%Y.%m.%d")
        game.headers["White"] = "Player"
        game.headers["Black"] = "Chess AI"
        game.headers["Result"] = self.board.result() if self.board.is_game_over() else "*"

        node = game
        for move in self.board.move_stack:
            node = node.add_main_variation(move)

        self._last_exported_pgn = str(game)
        return self._last_exported_pgn

    def _check_game_state(self):
        if self.board.is_game_over():
            self.game_over = True
            if self.board.is_checkmate():
                winner = "White" if self.board.turn == chess.BLACK else "Black"
                self.message = f"Checkmate! {winner} wins!"
            else:
                self.message = "Game drawn!"