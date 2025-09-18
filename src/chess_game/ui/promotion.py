import pygame
import chess
from ..utils.constants import *


class PromotionDialog:
    def __init__(self, screen, piece_images):
        self.screen = screen
        self.piece_images = piece_images

    def show(self, move, is_white_turn):
        pieces = ['q', 'r', 'b', 'n'] if is_white_turn else ['Q', 'R', 'B', 'N']
        
        dialog = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE * 4))
        dialog.fill((240, 240, 240))
        pygame.draw.rect(dialog, BLACK, (0, 0, SQUARE_SIZE, SQUARE_SIZE * 4), 2)
        
        for i, piece in enumerate(pieces):
            dialog.blit(self.piece_images[piece], (0, i * SQUARE_SIZE))
        
        rect = pygame.Rect(chess.square_file(move.to_square) * SQUARE_SIZE, 0, 
                          SQUARE_SIZE, SQUARE_SIZE * 4)
        
        if rect.y + rect.height > BOARD_SIZE:
            rect.y = BOARD_SIZE - rect.height
        
        self.screen.blit(dialog, rect)
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if rect.collidepoint(mouse_x, mouse_y):
                        rel_y = mouse_y - rect.y
                        piece_index = rel_y // SQUARE_SIZE
                        if 0 <= piece_index < len(pieces):
                            return pieces[piece_index]
        return 'q'