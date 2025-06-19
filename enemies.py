import pygame
import random
import os
from settings import *


class Enemy:
    """
    Класс для представления вражеского автомобиля.
    Обрабатывает загрузку изображения, обновление позиции и отрисовку.
    """

    def __init__(self, x, y):
        # выбираем случайный размер из настроек
        self.size = random.choice(ENEMY_SIZES)

        # загружаем изображение врага
        self.image = self.load_enemy_image()

        # создаем прямоугольник для коллизий
        self.rect = self.image.get_rect(topleft=(x, y))

        # создаем маску для точных столкновений
        self.mask = pygame.mask.from_surface(self.image)

    def load_enemy_image(self):
        # определяем параметры в зависимости от размера
        is_small = self.size == (55, 95)
        filename = "enemy_small.png" if is_small else "enemy_large.png"
        color = (0, 100, 255) if is_small else (255, 100, 0)

        # проверяем возможные пути к файлам
        for path in [
            os.path.join('images',
                         'png',
                         'enemies',
                         filename),
            os.path.join('images',
                         'png',
                         filename),
            os.path.join('images', filename)
        ]:
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                if img.get_size() != self.size:
                    return pygame.transform.scale(
                        img,
                        self.size
                    )
                return img

        image = pygame.Surface(
            self.size,
            pygame.SRCALPHA
        )

        # рисуем кузов машины
        pygame.draw.rect(
            image,
            color,
            (0, 0, *self.size)
        )

        # рисуем стекло
        glass_pos = (
            (15, 15, 30, 20)
            if is_small
            else (20, 20, 30, 25)
        )

        pygame.draw.rect(
            image,
            (200, 200, 255),
            glass_pos
        )

        return image

    def update(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Enemies:
    """
    Класс для управления всеми врагами в игре.
    Обрабатывает спавн, обновление и отрисовку врагов.
    """

    def __init__(self):

        # список активных врагов
        self.enemies = []

        # текущая скорость врагов
        self.current_speed = BASE_SPEED

        # время последнего спавна
        self.last_spawn_time = 0

        # минимальное количество врагов
        self.min_enemies = 1

    def get_max_enemies(self, score):
        if score < 50:
            return random.randint(1, 2)

        if score < 100:
            return random.randint(2, 3)

        return random.randint(2, 4)

    def ensure_min_enemies(self, score):
        while len(self.enemies) < self.min_enemies:
            self.spawn_enemy(
                score,
                forced=True
            )

    def can_spawn(self, new_rect):
        for enemy in self.enemies:
            if new_rect.inflate(40, 40).colliderect(
                    enemy.rect.inflate(40, 40)
            ):
                return False

        return True

    def spawn_enemy(self, score, forced=False):
        if not forced and len(self.enemies) >= self.get_max_enemies(score):
            return False

        size = random.choice(ENEMY_SIZES)

        # делаем несколько попыток найти свободное место
        for _ in range(5):
            x = random.randint(
                SCREEN_WIDTH // 2 - ROAD_WIDTH // 2 + size[0] // 2,
                SCREEN_WIDTH // 2 + ROAD_WIDTH // 2 - size[0] - size[0] // 2
            )

            new_rect = pygame.Rect(
                x,
                -size[1],
                *size
            )

            if self.can_spawn(new_rect):
                self.enemies.append(
                    Enemy(x, -size[1])
                )
                return True

        return False

    def update(self, game_time, score):
        # плавное увеличение скорости

        self.current_speed = BASE_SPEED + (
                MAX_SPEED - BASE_SPEED
        ) * min(1.0, game_time / 90000)

        # гарантируем минимальное количество врагов
        self.ensure_min_enemies(score)

        # спавним новых врагов с вероятностью
        spawn_chance = 0.015 + min(
            0.025,
            score / 4000
        )

        if random.random() < spawn_chance:
            self.spawn_enemy(score)

        # обновляем позиции врагов
        for enemy in self.enemies[:]:
            enemy.update(self.current_speed)

            # удаляем врагов за экраном
            if enemy.rect.top > SCREEN_HEIGHT + 150:
                self.enemies.remove(enemy)

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)