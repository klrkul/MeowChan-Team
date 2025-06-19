import pygame
from settings import *


class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.score_font = pygame.font.Font(None, 48)
        self.last_score = 0
        self.score_scale = 1.0
        self.scale_direction = 0.01
        self.pulse_speed = 0.05
        self.score_color = (255, 215, 0)  # голден
        self.last_score_change = 0
        self.combo = 0
        self.score_bg = self.create_score_background()

    def create_score_background(self):
        surface = pygame.Surface((200, 60), pygame.SRCALPHA)

        for i in range(60):
            alpha = 150 - i * 2
            pygame.draw.line(
                surface, (0, 0, 50, alpha),
                (0, i),
                (200, i))

        pygame.draw.rect(surface,
            (255, 255, 255, 30),
            (0, 0, 200, 60), 2)

        pygame.draw.circle(surface,
            (255, 215, 0, 50),
            (10, 30), 5)

        pygame.draw.circle(surface,
            (255, 215, 0, 50),
            (190, 30), 5)
        return surface

    def draw_score(self, screen, score):
        current_time = pygame.time.get_ticks()
        self.last_score = score
        if current_time - self.last_score_change < 300:
            self.score_scale += self.scale_direction

            if self.score_scale > 1.2 or self.score_scale < 1.0:
                self.scale_direction *= -1
        else:
            self.score_scale = 1.0

        screen.blit(self.score_bg,(20, 20))

        score_text = self.score_font.render(
            f"{int(score)}",
            True,
            self.score_color)

        scaled_text = pygame.transform.scale(
            score_text, (int(score_text.get_width() * self.score_scale),
                         int(score_text.get_height() * self.score_scale)))

        text_rect = scaled_text.get_rect(midleft=(50, 50))

        shadow = self.score_font.render(
            f"{int(score)}",
            True,
            (0, 0, 0, 150))

        screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(scaled_text, text_rect)

        if self.combo > 5:
            combo_text = self.font.render(
                f"x{self.combo} COMBO!",
                True,
                (255, 50, 50)
            )
            screen.blit(
                combo_text,
                (text_rect.right + 10, text_rect.y)
            )

    def draw_game_over(self, screen):
        if hasattr(self, 'sound_manager'):
            self.sound_manager.play_sound('gameover')
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        text = pygame.font.Font(None, 72).render("GAME OVER",
                                                 True,
                                                 (255, 50, 50))

        text_rect = text.get_rect(
            center=(SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2 - 50))

        glow = pygame.Surface((text.get_width() + 20,
                               text.get_height() + 20),
                              pygame.SRCALPHA)

        pygame.draw.rect(glow, (255, 50, 50, 50),
            (0, 0, *glow.get_size()),
                         border_radius=10)

        screen.blit(glow, (text_rect.x - 10, text_rect.y - 10))
        screen.blit(text, text_rect)

        restart = pygame.font.Font(None, 36).render(
            "Press R to restart",
            True,
            (255, 255, 255))

        screen.blit(restart,
                    (SCREEN_WIDTH // 2 - restart.get_width() // 2,
                     SCREEN_HEIGHT // 2 + 20))

        final_score = pygame.font.Font(None, 48).render(
            f"Final Score: {self.last_score}",
            True,
            (255, 215, 0))

        screen.blit(
            final_score,
            (SCREEN_WIDTH // 2 - final_score.get_width() // 2,
             SCREEN_HEIGHT // 2 + 80))
