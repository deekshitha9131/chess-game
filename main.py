import pygame
import chess
from src.core.game import ChessGame
from src.ui.board import BoardRenderer
from src.ui.menu import MenuRenderer
from src.ui.sidebar import SidebarRenderer
from src.ui.promotion import PromotionDialog
from src.utils.constants import *

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
        self.pending_move_animation = None
        self.animation_active = False
        self.animation_start_time = 0
        self.animation_duration = 180
        self.animation_start_pos = (0, 0)
        self.animation_end_pos = (0, 0)
        self.animation_current_pos = (0, 0)
        self.animation_piece = None
        self.animation_source_square = None
        self.animation_board = None

    def _square_to_pixel(self, square):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        return (file * SQUARE_SIZE, (7 - rank) * SQUARE_SIZE)

    def _start_move_animation(self, move):
        if self.animation_active:
            return False

        piece = self.game.board.piece_at(move.from_square)
        if piece is None:
            return False

        self.pending_move_animation = move
        self.animation_active = True
        self.animation_start_time = pygame.time.get_ticks()
        self.animation_piece = piece
        self.animation_source_square = move.from_square
        self.animation_board = self.game.board.copy()
        self.animation_start_pos = self._square_to_pixel(move.from_square)
        self.animation_end_pos = self._square_to_pixel(move.to_square)
        self.animation_current_pos = self.animation_start_pos
        return True

    def _advance_animation(self):
        if not self.animation_active:
            return False

        elapsed = pygame.time.get_ticks() - self.animation_start_time
        progress = min(1.0, elapsed / self.animation_duration)
        self.animation_current_pos = (
            self.animation_start_pos[0] + (self.animation_end_pos[0] - self.animation_start_pos[0]) * progress,
            self.animation_start_pos[1] + (self.animation_end_pos[1] - self.animation_start_pos[1]) * progress,
        )

        if progress >= 1.0:
            self.animation_active = False
            self.pending_move_animation = None
            self.game.commit_pending_move()
            self.animation_board = None
            self.game.selected_square = None
            self.game.valid_moves = []
            if self.game.board.is_check():
                self.check_timer = 60
            if not self.game.game_over and self.game.board.turn == chess.BLACK:
                self.game.start_ai_search()

        return True

    def handle_board_click(self, pos):
        if self.game.game_over or self.game.ai_thinking or self.animation_active or self.game.board.turn != chess.WHITE:
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
                
                if self.game.queue_pending_move(move):
                    self.game.selected_square = None
                    self.game.valid_moves = []
                    self._start_move_animation(move)
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
            
            if self.game.ai_thinking and self.game.ai_thread is None:
                if self.game.apply_pending_ai_move():
                    if self.game.board.is_check():
                        self.check_timer = 60

            # Update check timer
            if self.check_timer > 0:
                self.check_timer -= 1
                
            # Check for game over
            if self.game.game_over and self.game_active:
                self.result_message = self.game.message
                pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
                self.game_active = False
            
            if self.animation_active:
                self._advance_animation()

            # Draw
            self.screen.fill(WHITE)
            if self.game_active:
                if self.animation_active:
                    render_board = self.animation_board if self.animation_board is not None else self.game.board
                    self.board_renderer.draw(
                        render_board,
                        self.game.selected_square,
                        self.game.valid_moves,
                        animated_piece=(self.animation_piece, self.animation_current_pos),
                        skip_square=self.animation_source_square if self.animation_active else None,
                    )
                else:
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