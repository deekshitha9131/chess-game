import chess

from src.core.ai import ChessAI
from src.core.opening_book import OPENING_BOOK


def test_opening_book_not_empty():
    assert len(OPENING_BOOK) > 0


def test_start_position_exists():
    board = chess.Board()

    assert board.fen() in OPENING_BOOK


def test_every_book_move_is_valid_uci():
    for moves in OPENING_BOOK.values():

        for move in moves:

            chess.Move.from_uci(move)


def test_book_lookup_returns_legal_move():
    ai = ChessAI()

    board = chess.Board()

    move = ai._get_book_move(board)

    assert move in board.legal_moves