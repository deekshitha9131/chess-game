import pygame
import chess
from .core.game import ChessGame
from .ui.board import BoardRenderer
from .ui.menu import MenuRenderer
from .ui.sidebar import SidebarRenderer
from .ui.promotion import PromotionDialog
from .utils.constants import *


class ChessApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE + 200, BOARD_SIZE))
        pygame.display.set_caption('Chess Game')
        self.clock = pygame.time.Clock()
        
        self.game = ChessGame()
        self.board_renderer = BoardRenderer(self.screen)
        self.menu_renderer = MenuRenderer(self.screen)
        self.sidebar_renderer = SidebarRenderer(self.screen)
        self.promotion_dialog = PromotionDialog(self.screen, self.board_renderer.piece_images)
        
        self.game_active = False
        self.result_message = ""
        self.check_timer = 0

    def handle_board_click(self, pos):
        if self.game.game_over or self.game.ai_thinking or self.game.board.turn != chess.WHITE:
            return
            
        square = self.board_renderer.coords_to_square(*pos)
        if square is None:
            return
            
        piece = self.game.board.piece_at(square)
        
        if self.game.selected_square is not None:
            if square == self.game.selected_square:
                self.game.selected_square = None
                self.game.valid_moves = []
                return
                
            move = None
            for valid_move in self.game.valid_moves:
                if valid_move.from_square == self.game.selected_square and valid_move.to_square == square:
                    move = valid_move
                    break
                    
            if move:
                # Handle promotion
                selected_piece = self.game.board.piece_at(self.game.selected_square)
                if (selected_piece and selected_piece.piece_type == chess.PAWN and
                    ((self.game.board.turn == chess.WHITE and chess.square_rank(square) == 7) or
                     (self.game.board.turn == chess.BLACK and chess.square_rank(square) == 0))):
                    promotion_piece = self.promotion_dialog.show(move, self.game.board.turn == chess.WHITE)
                    if promotion_piece:
                        move = chess.Move(self.game.selected_square, square, 
                                        promotion=chess.Piece.from_symbol(promotion_piece).piece_type)
                
                if self.game.make_move(move):
                    self.game.selected_square = None
                    self.game.valid_moves = []
                    
                    if self.game.board.is_check():
                        self.check_timer = 60
                        
                    if not self.game.game_over and self.game.board.turn == chess.BLACK:
                        self.game.ai_thinking = True
                        pygame.time.set_timer(pygame.USEREVENT, 500)
            else:
                if piece and piece.color == chess.WHITE:
                    self.game.selected_square = square
                    self.game.valid_moves = [m for m in self.game.board.legal_moves if m.from_square == square]
                else:
                    self.game.selected_square = None
                    self.game.valid_moves = []
        else:
            if piece and piece.color == chess.WHITE:
                self.game.selected_square = square
                self.game.valid_moves = [m for m in self.game.board.legal_moves if m.from_square == square]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.USEREVENT and self.game.ai_thinking:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    ai_move = self.game.get_ai_move()
                    if ai_move:
                        self.game.make_move(ai_move)
                        if self.game.board.is_check():
                            self.check_timer = 60
                    self.game.ai_thinking = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if not self.game_active:
                        level = self.menu_renderer.handle_click(pos)
                        if level:
                            self.game.start_new_game(level)
                            self.game_active = True
                            self.result_message = ""
                    else:
                        sidebar_action = self.sidebar_renderer.handle_click(pos)
                        if sidebar_action == 'back':
                            self.game_active = False
                        elif sidebar_action == 'undo' and not self.game.game_over:
                            self.game.undo_move()
                        elif sidebar_action == 'restart':
                            level = self.game.ai.level if self.game.ai else 'intermediate'
                            self.game.start_new_game(level)
                        else:
                            self.handle_board_click(pos)
            
            # Update check timer
            if self.check_timer > 0:
                self.check_timer -= 1
                
            # Check for game over
            if self.game.game_over and self.game_active:
                self.result_message = self.game.message
                pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
                self.game_active = False
            
            # Draw
            self.screen.fill(WHITE)
            if self.game_active:
                self.board_renderer.draw(self.game.board, self.game.selected_square, self.game.valid_moves)
                ai_level = self.game.ai.level if self.game.ai else ""
                self.sidebar_renderer.draw(ai_level, self.game.game_over, self.game.message, self.check_timer)
            else:
                self.menu_renderer.draw(self.result_message)
                
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()


def main():
    app = ChessApp()
    app.run()


if __name__ == "__main__":
    main()