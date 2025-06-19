import pygame
from settings import *


class StartMenu:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.title_y = SCREEN_HEIGHT // 4
        self.title_target_y = SCREEN_HEIGHT // 3
        self.animation_speed = 2
        # кнопки рисую
        self.start_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2,
            200,
            50
        )
        self.exit_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2 + 70,
            200,
            50
        )
        self.selected_button = 0  # 0 - start, 1 - exit
        self.button_colors = [
            (100, 200, 100),
            (200, 100, 100)
        ]

    def update(self):
        if self.title_y < self.title_target_y:
            self.title_y += self.animation_speed
            # в самом начале заголовок красиво появляется

    def draw(self, screen):
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        title = self.font_large.render(
            "RACING GAME",
            True,
            (255, 215, 0)
        )

        title_rect = title.get_rect(
            center=(SCREEN_WIDTH // 2, self.title_y)
        )

        shadow = self.font_large.render("RACING GAME", True, (0, 0, 0, 150)
        )

        screen.blit(shadow, (title_rect.x + 5, title_rect.y + 5))
        screen.blit(title, title_rect)
        start_color = (
            self.button_colors[0]
            if self.selected_button == 0
            else (150, 150, 150)
        )
        pygame.draw.rect(
            screen,
            start_color,
            self.start_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            WHITE,
            self.start_button,
            2,
            border_radius=10
        )
        start_text = self.font_medium.render("START",True,WHITE)
        screen.blit(
            start_text,
            (
                self.start_button.centerx - start_text.get_width() // 2,
                self.start_button.centery - start_text.get_height() // 2
            )
        )
        exit_color = (
            self.button_colors[1]
            if self.selected_button == 1
            else (150, 150, 150)
        )
        pygame.draw.rect(
            screen,
            exit_color,
            self.exit_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            WHITE,
            self.exit_button,
            2,
            border_radius=10
        )
        exit_text = self.font_medium.render("EXIT",True,WHITE)
        screen.blit(
            exit_text,
            (
                self.exit_button.centerx - exit_text.get_width() // 2,
                self.exit_button.centery - exit_text.get_height() // 2
            )
        )
        instr = self.font_small.render("Use ARROW KEYS and ENTER to navigate",True,WHITE)
        screen.blit(
            instr,
            (SCREEN_WIDTH // 2 - instr.get_width() // 2,
             SCREEN_HEIGHT - 50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_UP):
                # здесь звук если что
                if hasattr(self, 'sound_manager'):
                    self.sound_manager.play_sound('menu')
                self.selected_button = (
                    1 if event.key == pygame.K_DOWN else 0
                )
                return None
            elif event.key == pygame.K_RETURN:
                # здесь тоже
                if hasattr(self, 'sound_manager'):
                    self.sound_manager.play_sound('menu')
                return self.selected_button
        return None