import pygame
import sys
import os
from settings import *
from player import Player
from road import Road
from enemies import Enemies
from ui import UI
from coins import Coins
from menu import StartMenu
from sound import SoundManager


class Game:
    """
    главный класс игры, управляющий всеми процессами:
    - инициализацией
    - обработкой событий
    - обновлением состояния
    - отрисовкой
    """

    def __init__(self):
        # Инициализация pygame
        pygame.init()

        # создание игрового окна
        self.screen = pygame.display.set_mode((
            SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Кчааууууу")
        self.clock = pygame.time.Clock()

        self.background = None
        self.bg_y = 0
        self.load_background()

        # игровые объекты
        self.player = Player()
        self.road = Road()
        self.enemies = Enemies()
        self.ui = UI()
        self.coins = Coins()
        self.menu = StartMenu()

        # звук
        self.sound_manager = SoundManager()

        # время начала игры
        self.start_time = pygame.time.get_ticks()

        # система счета
        self.base_score = 0
        self.coins_score = 0
        self.total_score = 0

        # состояния игры
        self.game_over = False
        self.running = True
        self.paused = False
        self.in_menu = True

        # музыкаменю
        self.sound_manager.play_music('menu')

    def load_background(self):
        bg_path = os.path.join(
            'images',
            'png',
            'bg.jpg'
        )

        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(
                self.background,
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        else:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 100, 50))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_events(event)

    def handle_keydown_events(self, event):
        # Выход из игры/меню
        if event.key == pygame.K_ESCAPE:
            if self.in_menu:
                self.running = False
            else:
                self.sound_manager.play_music('menu')
                self.in_menu = True

        # Рестарт игры
        if event.key == pygame.K_r and self.game_over:
            self.reset_game()

        # Пауза
        if (event.key == pygame.K_p
                and not self.game_over
                and not self.in_menu):
            self.toggle_pause()

        # Обработка меню
        if self.in_menu:
            self.handle_menu_input(event)

    def toggle_pause(self):
        #пауза
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def handle_menu_input(self, event):
        result = self.menu.handle_event(event)

        if result == 0:  # Start
            self.sound_manager.play_music('game')
            self.reset_game()

        elif result == 1:  # Exit
            self.running = False

    def reset_game(self):
        self.__init__()
        self.in_menu = False
        self.sound_manager.play_music('game')

    def check_collisions(self):
        for enemy in self.enemies.enemies[:]:
            enemy.mask = pygame.mask.from_surface(enemy.image)
            offset_x = enemy.rect.x - self.player.rect.x
            offset_y = enemy.rect.y - self.player.rect.y

            if self.player.mask.overlap(
                    enemy.mask,
                    (offset_x, offset_y)):
                self.sound_manager.play_sound('gameover')
                self.game_over = True
                break

    def update(self):
        if self.in_menu:
            self.menu.update()
            return

        if self.game_over or self.paused:
            return

        self.update_game_state()

    def update_game_state(self):
        # обновление монет
        coins_collected = self.coins.update(
            self.enemies.enemies,
            self.player)

        if coins_collected > 0:
            self.sound_manager.play_sound('coin')
            self.coins_score += 5 * coins_collected

        # обновление счета
        game_time = pygame.time.get_ticks() - self.start_time
        self.base_score = game_time // 1000
        self.total_score = self.base_score + self.coins_score

        # расчет скорости
        speed_ratio = self.enemies.current_speed / BASE_SPEED

        # Обновление объектов
        self.enemies.update(game_time, self.total_score)
        self.road.update(speed_ratio * 0.6)
        self.player.update(self.road, self.enemies.current_speed)

        # проверка столкновений
        self.check_collisions()

        # обновление фона
        self.update_background(speed_ratio)

    def update_background(self, speed_ratio):
        self.bg_y += speed_ratio * 1.0

        if self.bg_y >= SCREEN_HEIGHT:
            self.bg_y = 0

    def draw(self):
        self.draw_background()
        if self.in_menu:
            self.menu.draw(self.screen)

        else:
            self.draw_game_objects()

        pygame.display.flip()

    def draw_background(self):
        self.screen.blit(
            self.background,
            (0, self.bg_y))

        self.screen.blit(
            self.background,
            (0, self.bg_y - SCREEN_HEIGHT))

    def draw_game_objects(self):
        self.road.draw(self.screen)
        self.enemies.draw(self.screen)
        self.coins.draw(self.screen)
        self.player.draw(self.screen)
        self.ui.draw_score(self.screen, self.total_score)

        if self.game_over:
            self.ui.draw_game_over(self.screen)

        elif self.paused:
            self.draw_pause_screen()

    def draw_pause_screen(self):
        pause_text = self.ui.font.render(
            "PAUSED",
            True,
            WHITE)

        self.screen.blit(
            pause_text,
            (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
             SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))

    def run(self):

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
