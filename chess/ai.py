import chess
import random

class ChessAI:
    def __init__(self, level='intermediate'):
        self.level = level
        self.depth = self._get_depth_for_level()
        self.randomness = self._get_randomness_for_level()
        
    def _get_depth_for_level(self):
        if self.level == 'beginner':
            return 1  # Very simple moves
        elif self.level == 'intermediate':
            return 3  # Moderate difficulty
        else:  # advanced
            return 4  # Stronger moves
    
    def _get_randomness_for_level(self):
        if self.level == 'beginner':
            return 0.4  # 40% chance to make a random move
        elif self.level == 'intermediate':
            return 0.1  # 10% chance to make a random move
        else:  # advanced
            return 0   # Always optimal moves
    
    def evaluate_board(self, board):
        """More sophisticated evaluation function"""
        if board.is_checkmate():
            return -99999 if board.turn == chess.WHITE else 99999
        
        if board.is_stalemate():
            return 0
        
        # Piece values with positional bonuses
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        score = 0
        
        # Material score
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                score += value if piece.color == chess.WHITE else -value
        
        # Add some simple positional bonuses for advanced level
        if self.level == 'advanced':
            # Encourage center control
            center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
            for square in center_squares:
                piece = board.piece_at(square)
                if piece and piece.color == chess.WHITE:
                    score += 20
                elif piece and piece.color == chess.BLACK:
                    score -= 20
        
        return score
    
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)
        
        if maximizing_player:
            max_eval = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def find_best_move(self, board):
        """Find the best move with level-appropriate difficulty"""
        # Occasionally make random moves at lower levels
        if random.random() < self.randomness:
            return random.choice(list(board.legal_moves))
        
        best_move = None
        best_value = -float('inf') if board.turn == chess.WHITE else float('inf')
        
        for move in board.legal_moves:
            board.push(move)
            board_value = self.minimax(
                board, 
                self.depth, 
                -float('inf'), 
                float('inf'), 
                board.turn == chess.BLACK
            )
            board.pop()
            
            if board.turn == chess.WHITE:
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
            else:
                if board_value < best_value:
                    best_value = board_value
                    best_move = move
        
        return best_move or random.choice(list(board.legal_moves))