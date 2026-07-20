import chess
import random
import time
from typing import Optional


class ChessAI:
    """
    Chess AI using:
    - Minimax
    - Alpha-Beta Pruning
    - Material Evaluation
    - Piece-Square Tables
    - Mobility
    - Center Control
    """

    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000,
    }

    # -----------------------------
    # Piece Square Tables
    # Values adapted from simplified
    # chess engine heuristics.
    # -----------------------------

    PAWN_TABLE = [
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10,-20,-20, 10, 10,  5,
         5, -5,-10,  0,  0,-10, -5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
         0,  0,  0,  0,  0,  0,  0,  0,
    ]

    KNIGHT_TABLE = [
       -50,-40,-30,-30,-30,-30,-40,-50,
       -40,-20,  0,  0,  0,  0,-20,-40,
       -30,  0, 10, 15, 15, 10,  0,-30,
       -30,  5, 15, 20, 20, 15,  5,-30,
       -30,  0, 15, 20, 20, 15,  0,-30,
       -30,  5, 10, 15, 15, 10,  5,-30,
       -40,-20,  0,  5,  5,  0,-20,-40,
       -50,-40,-30,-30,-30,-30,-40,-50,
    ]

    BISHOP_TABLE = [
       -20,-10,-10,-10,-10,-10,-10,-20,
       -10,  5,  0,  0,  0,  0,  5,-10,
       -10, 10, 10, 10, 10, 10, 10,-10,
       -10,  0, 10, 10, 10, 10,  0,-10,
       -10,  5,  5, 10, 10,  5,  5,-10,
       -10,  0,  5, 10, 10,  5,  0,-10,
       -10,  0,  0,  0,  0,  0,  0,-10,
       -20,-10,-10,-10,-10,-10,-10,-20,
    ]

    ROOK_TABLE = [
         0,  0,  5, 10, 10,  5,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         5, 10, 10, 10, 10, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0,
    ]

    QUEEN_TABLE = [
       -20,-10,-10, -5, -5,-10,-10,-20,
       -10,  0,  5,  0,  0,  0,  0,-10,
       -10,  5,  5,  5,  5,  5,  0,-10,
         0,  0,  5,  5,  5,  5,  0, -5,
        -5,  0,  5,  5,  5,  5,  0, -5,
       -10,  0,  5,  5,  5,  5,  0,-10,
       -10,  0,  0,  0,  0,  0,  0,-10,
       -20,-10,-10, -5, -5,-10,-10,-20,
    ]

    KING_TABLE = [
        20, 30, 10,  0,  0, 10, 30, 20,
        20, 20,  0,  0,  0,  0, 20, 20,
       -10,-20,-20,-20,-20,-20,-20,-10,
       -20,-30,-30,-40,-40,-30,-30,-20,
       -30,-40,-40,-50,-50,-40,-40,-30,
       -30,-40,-40,-50,-50,-40,-40,-30,
       -30,-40,-40,-50,-50,-40,-40,-30,
       -30,-40,-40,-50,-50,-40,-40,-30,
    ]

    def __init__(self, level: str = "intermediate"):

        self.level = level

        if level == "beginner":
            self.depth = 1
            self.randomness = 0.40

        elif level == "intermediate":
            self.depth = 3
            self.randomness = 0.10

        else:
            self.depth = 4
            self.randomness = 0.0

        # Statistics (used later in sidebar)
        self.nodes_searched = 0
        self.last_search_time = 0
        self.last_evaluation = 0

    def get_piece_square_value(self, piece: chess.Piece, square: int) -> int:

        # Flip table for black pieces
        if piece.color == chess.BLACK:
            square = chess.square_mirror(square)

        if piece.piece_type == chess.PAWN:
            return self.PAWN_TABLE[square]

        if piece.piece_type == chess.KNIGHT:
            return self.KNIGHT_TABLE[square]

        if piece.piece_type == chess.BISHOP:
            return self.BISHOP_TABLE[square]

        if piece.piece_type == chess.ROOK:
            return self.ROOK_TABLE[square]

        if piece.piece_type == chess.QUEEN:
            return self.QUEEN_TABLE[square]

        if piece.piece_type == chess.KING:
            return self.KING_TABLE[square]

        return 0
    # ----------------------------------------------------
    # Evaluation Functions
    # ----------------------------------------------------

    def evaluate_material(self, board: chess.Board) -> int:
        """Evaluate material + piece positions."""

        score = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)

            if piece is None:
                continue

            value = self.PIECE_VALUES[piece.piece_type]
            positional = self.get_piece_square_value(piece, square)

            if piece.color == chess.WHITE:
                score += value + positional
            else:
                score -= value + positional

        return score


    def evaluate_mobility(self, board: chess.Board) -> int:
        """
        Reward positions with more legal moves.
        """

        current_turn = board.turn

        board.turn = chess.WHITE
        white_moves = board.legal_moves.count()

        board.turn = chess.BLACK
        black_moves = board.legal_moves.count()

        board.turn = current_turn

        return (white_moves - black_moves) * 5


    def evaluate_center_control(self, board: chess.Board) -> int:
        """
        Reward occupying and attacking
        D4, E4, D5, E5.
        """

        score = 0

        center = [
            chess.D4,
            chess.E4,
            chess.D5,
            chess.E5,
        ]

        for sq in center:

            piece = board.piece_at(sq)

            if piece:

                if piece.color == chess.WHITE:
                    score += 20
                else:
                    score -= 20

            white_attackers = len(board.attackers(chess.WHITE, sq))
            black_attackers = len(board.attackers(chess.BLACK, sq))

            score += (white_attackers - black_attackers) * 3

        return score


    def evaluate_board(self, board: chess.Board) -> int:
        """
        Overall board evaluation.

        Positive score = White advantage

        Negative score = Black advantage
        """

        if board.is_checkmate():

            if board.turn == chess.WHITE:
                return -100000

            return 100000

        if board.is_stalemate():
            return 0

        if board.is_insufficient_material():
            return 0

        score = 0

        score += self.evaluate_material(board)

        score += self.evaluate_mobility(board)

        score += self.evaluate_center_control(board)

        return score


    # ----------------------------------------------------
    # Minimax + Alpha Beta
    # ----------------------------------------------------

    def minimax(
        self,
        board: chess.Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> int:

        self.nodes_searched += 1

        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing:

            max_eval = -float("inf")

            for move in board.legal_moves:

                board.push(move)

                evaluation = self.minimax(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                )

                board.pop()

                max_eval = max(max_eval, evaluation)

                alpha = max(alpha, evaluation)

                if beta <= alpha:
                    break

            return max_eval

        else:

            min_eval = float("inf")

            for move in board.legal_moves:

                board.push(move)

                evaluation = self.minimax(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    True,
                )

                board.pop()

                min_eval = min(min_eval, evaluation)

                beta = min(beta, evaluation)

                if beta <= alpha:
                    break

            return min_eval
