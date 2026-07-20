import chess
import random
import time
from typing import Optional

from .opening_book import OPENING_BOOK


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
        self.last_search_time = 0.0
        self.last_evaluation = 0
        self.last_best_move: Optional[chess.Move] = None
        self.last_best_move_san: Optional[str] = None
        self.has_completed_search = False

    def _material_score(self, piece: chess.Piece) -> int:
        """Return material value for a single piece from White's perspective."""
        value = self.PIECE_VALUES[piece.piece_type]
        return value if piece.color == chess.WHITE else -value

    def _piece_square_score(self, piece: chess.Piece, square: int) -> int:
        """Return the positional PST bonus for a single piece from White's perspective."""
        if piece.color == chess.BLACK:
            square = chess.square_mirror(square)

        if piece.piece_type == chess.PAWN:
            bonus = self.PAWN_TABLE[square]
        elif piece.piece_type == chess.KNIGHT:
            bonus = self.KNIGHT_TABLE[square]
        elif piece.piece_type == chess.BISHOP:
            bonus = self.BISHOP_TABLE[square]
        elif piece.piece_type == chess.ROOK:
            bonus = self.ROOK_TABLE[square]
        elif piece.piece_type == chess.QUEEN:
            bonus = self.QUEEN_TABLE[square]
        elif piece.piece_type == chess.KING:
            bonus = self.KING_TABLE[square]
        else:
            bonus = 0

        return bonus if piece.color == chess.WHITE else -bonus

    def _get_book_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Return a book move for the current position if the FEN exists in the opening book."""
        fen = board.fen()
        moves = OPENING_BOOK.get(fen)
        if not moves:
            return None

        book_move = random.choice(moves)
        try:
            move = chess.Move.from_uci(book_move)
        except ValueError:
            return None

        if move in board.legal_moves:
            return move

        return None

    def _order_moves(self, board: chess.Board, moves: list[chess.Move]) -> list[chess.Move]:
        """Return legal moves sorted by lightweight tactical heuristics."""
        scored_moves: list[tuple[int, chess.Move]] = []

        for move in moves:
            piece = board.piece_at(move.from_square)
            captured_piece = board.piece_at(move.to_square)
            score = 0

            board.push(move)
            try:
                # Checkmate is the strongest possible outcome and should be searched first.
                if board.is_checkmate():
                    score += 1000000

                # Promotions are often tactically important and should be tried early.
                if move.promotion is not None:
                    score += 500000

                # MVV-LVA: prefer capturing a more valuable enemy piece with a less valuable attacker.
                if captured_piece is not None:
                    victim_value = self.PIECE_VALUES[captured_piece.piece_type]
                    attacker_value = self.PIECE_VALUES[piece.piece_type]
                    score += victim_value * 10 - attacker_value

                # Checks are usually stronger than quiet moves and should be preferred.
                if board.is_check():
                    score += 10000

                # Small bonus for moving toward the center.
                center_squares = {chess.E4, chess.D4, chess.E5, chess.D5}
                if move.to_square in center_squares:
                    score += 20
            finally:
                board.pop()

            scored_moves.append((score, move))

        scored_moves.sort(key=lambda item: item[0], reverse=True)
        return [move for _, move in scored_moves]

    def get_piece_square_value(self, piece: chess.Piece, square: int) -> int:
        """Get the PST bonus for a piece on a square."""
        return self._piece_square_score(piece, square)

    # ----------------------------------------------------
    # Evaluation Functions
    # ----------------------------------------------------

    def evaluate_material(self, board: chess.Board) -> int:
        """Evaluate material + piece-square bonuses for the current board."""

        score = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)

            if piece is None:
                continue

            material_score = self._material_score(piece)
            piece_square_bonus = self._piece_square_score(piece, square)
            score += material_score + piece_square_bonus

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
            ordered_moves = self._order_moves(board, list(board.legal_moves))

            for move in ordered_moves:

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
            ordered_moves = self._order_moves(board, list(board.legal_moves))

            for move in ordered_moves:

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
    # ----------------------------------------------------
    # Root Move Selection
    # ----------------------------------------------------

    def find_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """
        Search from the root and return the best legal move
        for the side to move, using the existing minimax +
        alpha-beta search.
        """

        legal_moves = list(board.legal_moves)

        if not legal_moves:
            return None

        book_move = self._get_book_move(board)
        if book_move is not None:
            self.nodes_searched = 0
            self.last_search_time = 0.0
            self.last_evaluation = 0
            self.last_best_move = book_move
            self.last_best_move_san = None if book_move is None else board.san(book_move)
            self.has_completed_search = True
            return book_move

        ordered_moves = self._order_moves(board, legal_moves)

        self.nodes_searched = 0
        self.last_search_time = 0.0
        self.last_evaluation = 0
        self.last_best_move = None
        self.last_best_move_san = None
        self.has_completed_search = False
        start_time = time.perf_counter()

        maximizing = board.turn == chess.WHITE

        best_move = None
        best_eval = -float("inf") if maximizing else float("inf")

        alpha = -float("inf")
        beta = float("inf")

        for move in ordered_moves:

            board.push(move)

            evaluation = self.minimax(
                board,
                self.depth - 1,
                alpha,
                beta,
                not maximizing,
            )

            board.pop()

            if maximizing:
                if evaluation > best_eval:
                    best_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
            else:
                if evaluation < best_eval:
                    best_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)

        self.last_search_time = time.perf_counter() - start_time
        self.last_evaluation = best_eval
        self.last_best_move = best_move
        self.last_best_move_san = None if best_move is None else board.san(best_move)
        self.has_completed_search = True

        # Fallback safety net: should not trigger since legal_moves
        # is non-empty, but guarantees a legal move is always returned.
        return best_move if best_move is not None else legal_moves[0]
