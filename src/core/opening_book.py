"""Small built-in opening book keyed by FEN strings.

The book is intentionally compact and easy to extend. It is only used as a
fast-path before the existing minimax search.
"""

OPENING_BOOK: dict[str, list[str]] = {
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": ["e2e4", "d2d4", "c2c4", "g2g3", "f2f4"],
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2": ["g8f6", "b8c6", "d7d5"],
    "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2": ["g8f6", "b8c6", "d7d5"],
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2": ["d7d5", "g8f6", "b8c6"],
    "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2": ["g8f6", "b8c6", "d7d5"],
    "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 2": ["c7c5", "g8f6", "c7c6"],
    "rnbqkbnr/pp2pppp/2p5/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3": ["g2g3", "b1c3", "f1g2"],
    "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1": ["e7e5", "d7d5", "g7g6"],
    "rnbqkbnr/pppppppp/8/8/2PpPP2/6p1/PP5P/RNBQKBNR b KQkq - 0 3": ["e7e5", "g8f6", "d7d5"],
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3": ["f8c5", "g8f6", "d8h4"],
    "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3": ["f8c5", "g8f6", "d8h4"],
    "r1bqkbnr/pppp1ppp/2n5/4p3/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq - 0 3": ["f8c5", "g8f6", "d8e7"],
    "rnbqkb1r/ppp1pppp/5n2/3p4/2PP4/2N1P3/PP3PbP/R1BQK1NR b KQkq - 0 4": ["c7c5", "g8f6", "d8c7"],
    "rnbqkb1r/pppppp1p/5np1/8/2PP4/6P1/PP2PP1P/RNBQKBNR b KQkq - 0 3": ["e7e5", "c7c5", "d7d5"],
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2": ["d2d4", "g1f3", "b1c3"],
    "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2": ["d2d4", "g1f3", "c2c4"],
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2": ["d2d4", "g1f3", "b1c3"],
    "rnbqkb1r/pppppppp/5n2/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1": ["e7e5", "d7d5", "c7c5"],
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2": ["c7c5", "g8f6", "e7e6"],
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2": ["c7c5", "g8f6", "e7e6"],
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2": ["c7c5", "g8f6", "e7e6"],
    "rnbqkbnr/pppppppp/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": ["e2e4", "d2d4", "c2c4", "g2g3", "f2f4"],
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1": ["e7e5", "d7d5", "g7g6"],
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1": ["e7e5", "d7d5", "g7g6"],
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1": ["e7e5", "d7d5", "g7g6"],
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1": ["e7e5", "d7d5", "g7g6"],
}
