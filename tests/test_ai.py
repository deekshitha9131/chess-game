import chess

from src.core.ai import ChessAI


def test_ai_initialization():
    ai = ChessAI("intermediate")

    assert ai.level == "intermediate"
    assert ai.depth == 3
    assert ai.randomness == 0.10


def test_difficulty_levels_use_distinct_search_depths():
    beginner = ChessAI("beginner")
    intermediate = ChessAI("intermediate")
    advanced = ChessAI("advanced")

    assert beginner.depth < intermediate.depth < advanced.depth


def test_material_evaluation_start_position():
    ai = ChessAI()

    board = chess.Board()

    assert ai.evaluate_material(board) == 0


def test_board_evaluation_returns_integer():
    ai = ChessAI()

    board = chess.Board()

    score = ai.evaluate_board(board)

    assert isinstance(score, int)


def test_find_best_move_returns_legal_move():
    ai = ChessAI()

    board = chess.Board()

    move = ai.find_best_move(board)

    assert move in board.legal_moves


def test_statistics_are_updated_after_search():
    ai = ChessAI()

    board = chess.Board()

    ai.find_best_move(board)

    assert ai.has_completed_search is True
    assert ai.last_best_move is not None
    assert ai.last_search_time >= 0
    assert ai.nodes_searched >= 0


def test_piece_square_value_returns_integer():
    ai = ChessAI()

    board = chess.Board()

    piece = board.piece_at(chess.E2)

    value = ai.get_piece_square_value(piece, chess.E2)

    assert isinstance(value, int)


def test_move_ordering_preserves_all_moves():
    ai = ChessAI()

    board = chess.Board()

    original = list(board.legal_moves)

    ordered = ai._order_moves(board, original)

    assert len(original) == len(ordered)

    assert set(original) == set(ordered)


def test_book_move_is_legal():
    ai = ChessAI()

    board = chess.Board()

    move = ai._get_book_move(board)

    assert move in board.legal_moves