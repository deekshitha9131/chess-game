import time

import chess

from src.core.game import ChessGame


def test_new_game_initializes_board():
    game = ChessGame()

    game.start_new_game("beginner")

    assert game.board is not None
    assert game.ai is not None
    assert game.game_over is False


def test_make_move_updates_history():
    game = ChessGame()

    game.start_new_game("beginner")

    move = chess.Move.from_uci("e2e4")

    assert game.make_move(move)

    assert len(game.move_history) == 1


def test_pending_move_is_not_applied_until_committed():
    game = ChessGame()

    game.start_new_game("beginner")

    move = chess.Move.from_uci("e2e4")

    assert game.queue_pending_move(move)
    assert game.board.move_stack == []
    assert game.move_history == []

    assert game.commit_pending_move()
    assert len(game.board.move_stack) == 1
    assert len(game.move_history) == 1


def test_undo_removes_history():
    game = ChessGame()

    game.start_new_game("beginner")

    game.make_move(chess.Move.from_uci("e2e4"))

    game.undo_move()

    assert len(game.move_history) == 0


def test_ai_search_uses_independent_board_copy():
    game = ChessGame()

    game.start_new_game("beginner")

    class MutatingAI:
        def __init__(self):
            self.level = "beginner"
            self.depth = 1
            self.randomness = 0.0
            self.nodes_searched = 0
            self.last_search_time = 0.0
            self.last_evaluation = 0
            self.last_best_move = None
            self.last_best_move_san = None
            self.has_completed_search = False

        def find_best_move(self, board):
            board.push(chess.Move.from_uci("e2e4"))
            time.sleep(0.1)
            return None

    game.ai = MutatingAI()
    game.start_ai_search()

    time.sleep(0.2)

    assert game.board.move_stack == []


def test_export_pgn_contains_headers():
    game = ChessGame()

    game.start_new_game("beginner")

    pgn = game.export_pgn()

    assert "Event" in pgn
    assert "White" in pgn
    assert "Black" in pgn


def test_move_history_rows():
    game = ChessGame()

    game.start_new_game("beginner")

    game.make_move(chess.Move.from_uci("e2e4"))
    game.make_move(chess.Move.from_uci("e7e5"))

    rows = game.get_move_history_rows()

    assert len(rows) == 1

    move_number, white, black = rows[0]

    assert move_number == 1
    assert white == "e4"
    assert black == "e5"


def test_statistics_dictionary_exists():
    game = ChessGame()

    game.start_new_game("beginner")

    stats = game.get_ai_statistics()

    assert "difficulty" in stats
    assert "depth" in stats
    assert "nodes" in stats