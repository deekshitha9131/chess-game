import pygame
from ..utils.constants import *


class MenuRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        
        self.buttons = {
            'beginner': pygame.Rect(BOARD_SIZE // 2 - 100, 200, 200, 50),
            'intermediate': pygame.Rect(BOARD_SIZE // 2 - 100, 270, 200, 50),
            'advanced': pygame.Rect(BOARD_SIZE // 2 - 100, 340, 200, 50)
        }

    def draw(self, result_message=""):
        self.screen.fill(WHITE)
        
        # Draw title
        title = self.title_font.render("Chess Game", True, BLACK)
        title_rect = title.get_rect(center=(BOARD_SIZE // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw result message
        if result_message:
            color = (0, 128, 0) if "won" in result_message else (255, 0, 0)
            result_text = self.font.render(result_message, True, color)
            result_rect = result_text.get_rect(center=(BOARD_SIZE // 2, 160))
            self.screen.blit(result_text, result_rect)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn_name, btn_rect in self.buttons.items():
            btn_color = BUTTON_HOVER if btn_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.screen, btn_color, btn_rect, border_radius=5)
            pygame.draw.rect(self.screen, BLACK, btn_rect, 2, border_radius=5)
            
            btn_text = self.font.render(btn_name.capitalize(), True, WHITE)
            text_rect = btn_text.get_rect(center=btn_rect.center)
            self.screen.blit(btn_text, text_rect)

    def handle_click(self, pos):
        for btn_name, btn_rect in self.buttons.items():
            if btn_rect.collidepoint(pos):
                return btn_name
        return None