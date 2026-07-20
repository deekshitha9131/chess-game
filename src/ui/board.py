import pygame
import chess
from ..utils.constants import *


class BoardRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.piece_images = self._load_piece_images()

    def _load_piece_images(self):
        images = {}
        for piece, filename in PIECE_IMAGES.items():
            images[piece] = pygame.image.load(get_image_path(filename)).convert_alpha()
            images[piece] = pygame.transform.scale(images[piece], (SQUARE_SIZE, SQUARE_SIZE))
        return images

    def draw(self, board, selected_square=None, valid_moves=None):
        valid_moves = valid_moves or []
        
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(self.screen, color, 
                               (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                square = chess.square(col, 7-row)
                
                # Highlight selected square
                if selected_square == square:
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill(HIGHLIGHT_COLOR)
                    self.screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                
                # Show dots for valid moves
                for move in valid_moves:
                    if move.from_square == selected_square and move.to_square == square:
                        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                        pygame.draw.circle(self.screen, (0, 150, 0), (center_x, center_y), 12)
                
                # Highlight king in check
                if board.is_check():
                    king_square = board.king(board.turn)
                    if square == king_square:
                        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        highlight.fill(CHECK_HIGHLIGHT)
                        self.screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                
                # Draw pieces
                piece = board.piece_at(square)
                if piece:
                    self.screen.blit(self.piece_images[piece.symbol()], 
                                   (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def coords_to_square(self, x, y):
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            file = x // SQUARE_SIZE
            rank = 7 - (y // SQUARE_SIZE)
            return chess.square(file, rank)
        return None