import chess
from .ai import ChessAI


class ChessGame:
    def __init__(self):
        self.board = None
        self.ai = None
        self.selected_square = None
        self.valid_moves = []
        self.game_over = False
        self.message = ""
        self.ai_thinking = False

    def start_new_game(self, level: str):
        self.board = chess.Board()
        self.ai = ChessAI(level)
        self.selected_square = None
        self.valid_moves = []
        self.game_over = False
        self.message = ""
        self.ai_thinking = False

    def make_move(self, move: chess.Move):
        if self.board and move in self.board.legal_moves:
            self.board.push(move)
            self._check_game_state()
            return True
        return False

    def undo_move(self):
        if self.board and len(self.board.move_stack) > 0:
            self.board.pop()
            if len(self.board.move_stack) > 0 and self.board.turn == chess.BLACK:
                self.board.pop()
            self.game_over = False
            self.message = ""

    def get_ai_move(self):
        if self.ai and self.board:
            return self.ai.find_best_move(self.board)
        return None

    def _check_game_state(self):
        if self.board.is_game_over():
            self.game_over = True
            if self.board.is_checkmate():
                winner = "White" if self.board.turn == chess.BLACK else "Black"
                self.message = f"Checkmate! {winner} wins!"
            else:
                self.message = "Game drawn!"