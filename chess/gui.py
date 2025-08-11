import pygame
import chess
from constants import *
from ai import ChessAI

class ChessGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE + 200, BOARD_SIZE))
        pygame.display.set_caption('Chess Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        
        self.board = None
        self.ai = None
        self.ai_thinking = False
        
        # Game state
        self.selected_square = None
        self.valid_moves = []
        self.game_over = False
        self.message = ""
        self.message_timer = 0
        self.game_active = False
        self.result_message = ""
        
        # Load piece images
        self.piece_images = {}
        for piece, filename in PIECE_IMAGES.items():
            self.piece_images[piece] = pygame.image.load(get_image_path(filename)).convert_alpha()
            self.piece_images[piece] = pygame.transform.scale(
                self.piece_images[piece], 
                (SQUARE_SIZE, SQUARE_SIZE)
            )
        
        # UI buttons
        self.buttons = {
            'beginner': pygame.Rect(BOARD_SIZE // 2 - 100, 200, 200, 50),
            'intermediate': pygame.Rect(BOARD_SIZE // 2 - 100, 270, 200, 50),
            'advanced': pygame.Rect(BOARD_SIZE // 2 - 100, 340, 200, 50),
            'undo': pygame.Rect(BOARD_SIZE + 10, 400, 180, 40),
            'restart': pygame.Rect(BOARD_SIZE + 10, 450, 180, 40),
            'back': pygame.Rect(BOARD_SIZE + 10, 500, 180, 40)
        }

    def draw_level_selection(self):
        """Draw the level selection screen"""
        self.screen.fill(WHITE)
        
        # Draw title
        title = self.title_font.render("Chess Game", True, BLACK)
        title_rect = title.get_rect(center=(BOARD_SIZE // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw result message if any
        if self.result_message:
            result_text = self.font.render(self.result_message, True, 
                                         (0, 128, 0) if "won" in self.result_message else (255, 0, 0))
            result_rect = result_text.get_rect(center=(BOARD_SIZE // 2, 160))
            self.screen.blit(result_text, result_rect)
        
        # Draw level buttons
        for btn_name in ['beginner', 'intermediate', 'advanced']:
            btn_rect = self.buttons[btn_name]
            mouse_pos = pygame.mouse.get_pos()
            btn_color = BUTTON_HOVER if btn_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            
            pygame.draw.rect(self.screen, btn_color, btn_rect, border_radius=5)
            pygame.draw.rect(self.screen, BLACK, btn_rect, 2, border_radius=5)
            
            btn_text = self.font.render(btn_name.capitalize(), True, WHITE)
            text_rect = btn_text.get_rect(center=btn_rect.center)
            self.screen.blit(btn_text, text_rect)

    def draw_board(self):
        """Draw the chess board with pieces"""
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )
                
                # Highlight selected square
                if self.selected_square and chess.square(col, 7-row) == self.selected_square:
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill(HIGHLIGHT_COLOR)
                    self.screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                
                # Highlight valid moves
                for move in self.valid_moves:
                    if move.from_square == self.selected_square:
                        target_col = chess.square_file(move.to_square)
                        target_row = 7 - chess.square_rank(move.to_square)
                        if target_col == col and target_row == row:
                            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                            highlight.fill(MOVE_HIGHLIGHT)
                            self.screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                
                # Highlight king in check
                if self.board.is_check():
                    king_square = self.board.king(self.board.turn)
                    king_col = chess.square_file(king_square)
                    king_row = 7 - chess.square_rank(king_square)
                    if col == king_col and row == king_row:
                        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        highlight.fill(CHECK_HIGHLIGHT)
                        self.screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                
                # Draw pieces
                piece = self.board.piece_at(chess.square(col, 7-row))
                if piece:
                    piece_char = piece.symbol()
                    self.screen.blit(
                        self.piece_images[piece_char], 
                        (col * SQUARE_SIZE, row * SQUARE_SIZE)
                    )

    def draw_sidebar(self):
        """Draw the sidebar with buttons and game info"""
        sidebar = pygame.Rect(BOARD_SIZE, 0, 200, BOARD_SIZE)
        pygame.draw.rect(self.screen, (200, 200, 200), sidebar)
        
        # Draw title
        title = self.font.render("Chess Game", True, BLACK)
        self.screen.blit(title, (BOARD_SIZE + 10, 20))
        
        # Draw current level
        if self.ai:
            level_text = self.font.render(f"Level: {self.ai.level}", True, BLACK)
            self.screen.blit(level_text, (BOARD_SIZE + 10, 60))
        
        # Draw game buttons
        pygame.draw.rect(self.screen, (100, 100, 100) if self.game_over else (150, 150, 255), self.buttons['undo'])
        pygame.draw.rect(self.screen, (255, 150, 150), self.buttons['restart'])
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.buttons['back'])
        
        pygame.draw.rect(self.screen, BLACK, self.buttons['undo'], 2)
        pygame.draw.rect(self.screen, BLACK, self.buttons['restart'], 2)
        pygame.draw.rect(self.screen, BLACK, self.buttons['back'], 2)
        
        undo_text = self.small_font.render("Undo Move", True, BLACK)
        restart_text = self.small_font.render("Restart Game", True, BLACK)
        back_text = self.small_font.render("Back to Menu", True, WHITE)
        
        self.screen.blit(undo_text, (self.buttons['undo'].x + 10, self.buttons['undo'].y + 10))
        self.screen.blit(restart_text, (self.buttons['restart'].x + 10, self.buttons['restart'].y + 10))
        self.screen.blit(back_text, (self.buttons['back'].x + 10, self.buttons['back'].y + 10))
        
        # Draw game over message
        if self.game_over:
            result_text = self.font.render(self.message, True, BLACK)
            self.screen.blit(result_text, (BOARD_SIZE + 10, 300))
        
        # Draw check message
        if self.message_timer > 0:
            check_text = self.font.render("Check!!", True, (255, 0, 0))
            self.screen.blit(check_text, (BOARD_SIZE + 10, 350))
            self.message_timer -= 1

    def coords_to_square(self, x, y):
        """Convert screen coordinates to chess square"""
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            file = x // SQUARE_SIZE
            rank = 7 - (y // SQUARE_SIZE)
            return chess.square(file, rank)
        return None

    def handle_promotion(self, move):
        """Handle pawn promotion by showing a promotion dialog"""
        promotion_pieces = ['q', 'r', 'b', 'n'] if self.board.turn == chess.WHITE else ['Q', 'R', 'B', 'N']
        
        promotion_dialog = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE * 4))
        promotion_dialog.fill((240, 240, 240))
        pygame.draw.rect(promotion_dialog, BLACK, (0, 0, SQUARE_SIZE, SQUARE_SIZE * 4), 2)
        
        for i, piece in enumerate(promotion_pieces):
            promotion_dialog.blit(
                self.piece_images[piece], 
                (0, i * SQUARE_SIZE)
            )
        
        promotion_rect = pygame.Rect(
            chess.square_file(move.to_square) * SQUARE_SIZE,
            0,
            SQUARE_SIZE,
            SQUARE_SIZE * 4
        )
        
        if promotion_rect.y + promotion_rect.height > BOARD_SIZE:
            promotion_rect.y = BOARD_SIZE - promotion_rect.height
        
        self.screen.blit(promotion_dialog, promotion_rect)
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if promotion_rect.collidepoint(mouse_x, mouse_y):
                        rel_y = mouse_y - promotion_rect.y
                        piece_index = rel_y // SQUARE_SIZE
                        return promotion_pieces[piece_index]

    def handle_click(self, square):
        """Handle user click on the board"""
        if self.game_over or self.ai_thinking:
            return
        
        if self.board.turn != chess.WHITE:  # It's AI's turn
            return
        
        piece = self.board.piece_at(square) if square is not None else None
        
        # If a square is already selected
        if self.selected_square is not None:
            # If clicking on the same square, deselect it
            if square == self.selected_square:
                self.selected_square = None
                self.valid_moves = []
                return
            
            # Check if the move is valid
            move = None
            for valid_move in self.valid_moves:
                if valid_move.from_square == self.selected_square and valid_move.to_square == square:
                    move = valid_move
                    break
            
            if move:
                # Handle promotion
                if move.promotion is not None:
                    promotion_piece = self.handle_promotion(move)
                    if promotion_piece:
                        move.promotion = chess.Piece.from_symbol(promotion_piece).piece_type
                    else:
                        return
                
                self.make_move(move)
                self.selected_square = None
                self.valid_moves = []
                
                # AI makes a move after a short delay
                if not self.board.is_game_over() and self.board.turn == chess.BLACK:
                    self.ai_thinking = True
                    pygame.time.set_timer(pygame.USEREVENT, 500)  # Delay for AI move
            else:
                # Select a different piece
                if piece and piece.color == chess.WHITE:
                    self.selected_square = square
                    self.valid_moves = [move for move in self.board.legal_moves if move.from_square == square]
                else:
                    self.selected_square = None
                    self.valid_moves = []
        else:
            # Select a piece if it's the player's color
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
                self.valid_moves = [move for move in self.board.legal_moves if move.from_square == square]

    def make_move(self, move):
        """Make a move on the board"""
        self.board.push(move)
        
        # Check for check
        if self.board.is_check():
            self.message_timer = 60
        
        # Check for game over
        if self.board.is_game_over():
            self.game_over = True
            if self.board.is_checkmate():
                if self.board.turn == chess.WHITE:  # Last move was by black (AI)
                    self.result_message = "Checkmate!! You lost"
                    self.message = "Checkmate!! You lost"
                else:  # Last move was by white (user)
                    self.result_message = "Checkmate!! You won"
                    self.message = "Checkmate!! You won"
            else:  # Stalemate
                self.result_message = "Game drawn by stalemate"
                self.message = "Game drawn by stalemate"
            
            # Return to menu after a short delay
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 second delay

    def undo_move(self):
        """Undo the last move"""
        if len(self.board.move_stack) > 0:
            self.board.pop()
            self.game_over = False
            self.message = ""
            self.selected_square = None
            self.valid_moves = []

    def restart_game(self):
        """Restart the game with the same level"""
        if self.ai:
            self.board = chess.Board()
            self.game_over = False
            self.message = ""
            self.selected_square = None
            self.valid_moves = []

    def start_new_game(self, level):
        """Start a new game with the specified level"""
        self.board = chess.Board()
        self.ai = ChessAI(level)
        self.game_active = True
        self.game_over = False
        self.message = ""
        self.selected_square = None
        self.valid_moves = []
        self.ai_thinking = False

    def return_to_menu(self):
        """Return to the level selection menu"""
        self.game_active = False
        self.board = None
        self.ai = None
        self.game_over = False
        self.message = ""
        self.selected_square = None
        self.valid_moves = []
        self.ai_thinking = False

    def run(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.USEREVENT + 1:  # Timer for returning to menu
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the timer
                    self.return_to_menu()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    if not self.game_active:  # Level selection screen
                        for btn_name in ['beginner', 'intermediate', 'advanced']:
                            if self.buttons[btn_name].collidepoint(mouse_x, mouse_y):
                                self.start_new_game(btn_name)
                                break
                    else:  # Game screen
                        if self.buttons['back'].collidepoint(mouse_x, mouse_y):
                            self.return_to_menu()
                        elif self.buttons['undo'].collidepoint(mouse_x, mouse_y) and not self.game_over and not self.ai_thinking:
                            self.undo_move()
                        elif self.buttons['restart'].collidepoint(mouse_x, mouse_y):
                            self.restart_game()
                        else:  # Board click
                            square = self.coords_to_square(mouse_x, mouse_y)
                            self.handle_click(square)
                
                elif event.type == pygame.USEREVENT and self.ai_thinking:
                    pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer
                    ai_move = self.ai.find_best_move(self.board)
                    self.make_move(ai_move)
                    self.ai_thinking = False
            
            # Draw everything
            self.screen.fill(WHITE)
            
            if self.game_active:
                self.draw_board()
                self.draw_sidebar()
            else:
                self.draw_level_selection()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()