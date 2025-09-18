import chess
import random
from typing import Optional


class ChessAI:
    def __init__(self, level: str = "intermediate"):
        self.level = level
        self.depth = self._get_depth_for_level()
        self.randomness = self._get_randomness_for_level()

    def _get_depth_for_level(self) -> int:
        if self.level == "beginner":
            return 1
        elif self.level == "intermediate":
            return 3
        else:  # advanced
            return 4

    def _get_randomness_for_level(self) -> float:
        if self.level == "beginner":
            return 0.4
        elif self.level == "intermediate":
            return 0.1
        else:  # advanced
            return 0.0

    def evaluate_board(self, board: chess.Board) -> int:
        if board.is_checkmate():
            return -99999 if board.turn == chess.WHITE else 99999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        piece_values = {
            chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
            chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000,
        }

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                score += value if piece.color == chess.WHITE else -value

        if self.level == "advanced":
            center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
            for sq in center_squares:
                piece = board.piece_at(sq)
                if piece and piece.color == chess.WHITE:
                    score += 20
                elif piece and piece.color == chess.BLACK:
                    score -= 20

        return score

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool) -> int:
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing:
            max_eval = -float("inf")
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        if random.random() < self.randomness:
            return random.choice(legal_moves)

        best_move = legal_moves[0]
        maximizing_player = (board.turn == chess.WHITE)

        try:
            if maximizing_player:
                best_value = -float("inf")
                for move in legal_moves:
                    board.push(move)
                    board_value = self.minimax(board, self.depth - 1, -float("inf"), float("inf"), False)
                    board.pop()
                    if board_value > best_value:
                        best_value = board_value
                        best_move = move
            else:
                best_value = float("inf")
                for move in legal_moves:
                    board.push(move)
                    board_value = self.minimax(board, self.depth - 1, -float("inf"), float("inf"), True)
                    board.pop()
                    if board_value < best_value:
                        best_value = board_value
                        best_move = move
        except Exception:
            return random.choice(legal_moves)

        return best_move