import pygame
from ..core.game import ChessGame
from ..utils.constants import *


class SidebarRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
        self.buttons = {
            'undo': pygame.Rect(BOARD_SIZE + 10, 400, 180, 40),
            'restart': pygame.Rect(BOARD_SIZE + 10, 450, 180, 40),
            'back': pygame.Rect(BOARD_SIZE + 10, 500, 180, 40)
        }

    @staticmethod
    def _format_search_time(search_time: float) -> str:
        if search_time <= 0:
            return "--"
        if search_time < 1.0:
            return f"{int(round(search_time * 1000))} ms"
        return f"{search_time:.2f} s"

    @staticmethod
    def _format_evaluation(value: object) -> str:
        if value in (None, "--"):
            return "--"
        if isinstance(value, str):
            return value
        if value >= 100000:
            return "Mate"
        if value <= -100000:
            return "Mated"
        sign = "+" if value >= 0 else "-"
        return f"{sign}{abs(value) / 100:.2f}"

    def _draw_ai_statistics(self, ai_level: str) -> None:
        game = ChessGame.get_active_instance()
        stats = game.get_ai_statistics() if game else {
            "difficulty": "--",
            "depth": "--",
            "evaluation": "--",
            "nodes": "--",
            "search_time": "--",
            "best_move": "--",
        }

        title = self.font.render("AI Statistics", True, BLACK)
        self.screen.blit(title, (BOARD_SIZE + 10, 95))

        rows = [
            ("Difficulty", stats.get("difficulty", ai_level.capitalize() or "--")),
            ("Depth", stats.get("depth", "--")),
            ("Evaluation", self._format_evaluation(stats.get("evaluation", "--")) if stats.get("has_data", False) else "--"),
            ("Nodes", stats.get("nodes", "--") if stats.get("has_data", False) else "--"),
            ("Search Time", self._format_search_time(float(stats.get("search_time", 0)) if stats.get("has_data", False) and isinstance(stats.get("search_time"), (int, float)) else 0.0) if stats.get("has_data", False) else "--"),
            ("Best Move", stats.get("best_move", "--") if stats.get("has_data", False) else "--"),
        ]

        y = 135
        for label, value in rows:
            self.screen.blit(self.small_font.render(label, True, BLACK), (BOARD_SIZE + 10, y))
            display_value = str(value)
            self.screen.blit(self.small_font.render(display_value, True, BLACK), (BOARD_SIZE + 10, y + 20))
            y += 40

    def _draw_move_history(self) -> None:
        game = ChessGame.get_active_instance()
        if game is None:
            return

        title = self.font.render("Move History", True, BLACK)
        self.screen.blit(title, (BOARD_SIZE + 10, 300))

        rows = game.get_move_history_rows(16)
        if not rows:
            text = self.small_font.render("--", True, BLACK)
            self.screen.blit(text, (BOARD_SIZE + 10, 340))
            return

        y = 340
        for move_number, white_move, black_move in rows:
            row_text = f"{move_number}."
            if white_move:
                row_text += f" {white_move}"
            if black_move:
                row_text += f" {black_move}"

            if len(row_text) > 34:
                row_text = row_text[:31] + "..."

            self.screen.blit(self.small_font.render(row_text, True, BLACK), (BOARD_SIZE + 10, y))
            y += 18

    def draw(self, ai_level="", game_over=False, message="", check_timer=0):
        sidebar = pygame.Rect(BOARD_SIZE, 0, 200, BOARD_SIZE)
        pygame.draw.rect(self.screen, (200, 200, 200), sidebar)
        
        # Title
        title = self.font.render("Chess Game", True, BLACK)
        self.screen.blit(title, (BOARD_SIZE + 10, 20))
        
        # Level
        if ai_level:
            level_text = self.font.render(f"Level: {ai_level}", True, BLACK)
            self.screen.blit(level_text, (BOARD_SIZE + 10, 60))
        
        self._draw_ai_statistics(ai_level)
        self._draw_move_history()

        # Buttons
        undo_color = (100, 100, 100) if game_over else (150, 150, 255)
        pygame.draw.rect(self.screen, undo_color, self.buttons['undo'])
        pygame.draw.rect(self.screen, (255, 150, 150), self.buttons['restart'])
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.buttons['back'])
        
        for btn_rect in self.buttons.values():
            pygame.draw.rect(self.screen, BLACK, btn_rect, 2)
        
        # Button text
        self.screen.blit(self.small_font.render("Undo Move", True, BLACK), 
                        (self.buttons['undo'].x + 10, self.buttons['undo'].y + 10))
        self.screen.blit(self.small_font.render("Restart Game", True, BLACK), 
                        (self.buttons['restart'].x + 10, self.buttons['restart'].y + 10))
        self.screen.blit(self.small_font.render("Back to Menu", True, WHITE), 
                        (self.buttons['back'].x + 10, self.buttons['back'].y + 10))
        
        # Messages
        if game_over and message:
            result_text = self.font.render(message, True, BLACK)
            self.screen.blit(result_text, (BOARD_SIZE + 10, 300))
        
        if check_timer > 0:
            check_text = self.font.render("Check!!", True, (255, 0, 0))
            self.screen.blit(check_text, (BOARD_SIZE + 10, 350))

    def handle_click(self, pos):
        for btn_name, btn_rect in self.buttons.items():
            if btn_rect.collidepoint(pos):
                return btn_name
        return None