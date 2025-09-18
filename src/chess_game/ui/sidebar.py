import pygame
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