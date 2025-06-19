import pygame
from settings import *


class Road:
    """ класс для отрисовки дороги и разметки """
    def __init__(self):
        self.width = ROAD_WIDTH  # ширина дороги
        self.x = (SCREEN_WIDTH - self.width) // 2  # позиция по х
        self.mark_offset = 0  # текущее смещение разметки
        self.mark_speed = 3  # базовая скорость движения разметки

    def update(self, speed_ratio):
        """ обновление дорожной разметки"""
        # увеличиваем смещение с учетом текущей скорости игры
        self.mark_offset += self.mark_speed * speed_ratio

        # сброс смещения при превышении высоты полосы + промежутка
        if self.mark_offset > ROAD_MARK_HEIGHT + ROAD_MARK_GAP:
            self.mark_offset -= (ROAD_MARK_HEIGHT + ROAD_MARK_GAP)

    def draw(self, screen):
        """отрисовка дороги и разметки """
        pygame.draw.rect(screen, ROAD_COLOR, # рисуем основное полотно дороги
                         (self.x, 0, self.width, SCREEN_HEIGHT))

        # параметры разметки
        mark_width = ROAD_MARK_WIDTH
        mark_height = ROAD_MARK_HEIGHT
        mark_gap = ROAD_MARK_GAP

        # начальная позиция первой полосы с учетом смещения
        start_y = -mark_height + self.mark_offset

        # расчет количества полос с запасом
        num_marks = int(SCREEN_HEIGHT / (mark_height + mark_gap)) + 2

        for i in range(num_marks):
            # вычисляем позицию по Y для текущей полосы
            current_y = start_y + i * (mark_height + mark_gap)

            # пропускаем полосы выше экрана
            if current_y < -mark_height:
                continue

            # прекращаем рисование если полоса ниже экрана
            if current_y > SCREEN_HEIGHT:
                break

            # рисуем полосу разметки по центру дороги
            pygame.draw.rect(screen, WHITE,
                             (self.x + self.width // 2 - mark_width // 2,
                              current_y,
                              mark_width,
                              mark_height))