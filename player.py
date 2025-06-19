import pygame
import os
from settings import *


class Player:
    def __init__(self):
        self.original_image = None
        self.image = None
        self.rect = None  #границы машины
        self.mask = None
        self.rotation_angle = 0  #угол поворота

        #загрузка изображения машины
        self.load_image()

        #параметры движения
        self.base_y = PLAYER_START_POS[1]  #базовая позиция по Y
        self.speed_forward = PLAYER_SPEED_FORWARD
        self.speed_backward = PLAYER_SPEED_BACKWARD

        #параметры поворота
        self.rotation_speed = 3  #скорость изменения угла поворота
        self.max_rotation = 25  #макс угол поворота
        self.rotation_decay = 2

    def load_image(self):
        #изображение
        image_path = os.path.join('images', 'png', 'player_car.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=PLAYER_START_POS)
        self.mask = pygame.mask.from_surface(self.original_image)

    def update(self, road, game_speed):
        """Обновляет позицию и состояние машины"""

        keys = pygame.key.get_pressed()

        #движение влево и поворота
        if keys[pygame.K_LEFT]:
            self.rect.x = max(road.x, self.rect.x - self.speed_forward)
            self.rotation_angle = min(self.rotation_angle + self.rotation_speed,
                                      self.max_rotation)

        #движение вправо и поворота
        elif keys[pygame.K_RIGHT]:
            self.rect.x = min(road.x + road.width - self.rect.width,
                              self.rect.x + self.speed_forward)
            self.rotation_angle = max(self.rotation_angle - self.rotation_speed,
                                      -self.max_rotation)

        #возврат угла поворота к нулю, если клавиши не нажаты
        else:
            if abs(self.rotation_angle) < self.rotation_decay:
                self.rotation_angle = 0

            elif self.rotation_angle > 0:
                self.rotation_angle -= self.rotation_decay

            else:
                self.rotation_angle += self.rotation_decay

        #движение вперед/назад
        if keys[pygame.K_UP]:
            self.base_y -= self.speed_forward

        if keys[pygame.K_DOWN]:
            self.base_y += self.speed_backward

        #ограничение для машины чтоб не выезжала за пределы экрана
        self.base_y = max(PLAYER_MIN_Y, min(self.base_y,
                                            SCREEN_HEIGHT - self.rect.height))
        self.rect.y = self.base_y - game_speed * PLAYER_SPEED_INFLUENCE

        #обновление картинки и маски при повороте
        if self.rotation_angle != 0:
            center = self.rect.center
            self.image = pygame.transform.rotate(self.original_image,
                                                 self.rotation_angle)
            self.rect = self.image.get_rect(center=center)
            self.mask = pygame.mask.from_surface(self.image)

        #возврат ориг изображения, если поворота нет
        elif self.image != self.original_image:
            self.image = self.original_image
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.original_image)

    def check_collision(self, enemy):
        """Проверка столкновения с вражеской машиной с учетом маски"""
        offset_x = enemy.rect.x - self.rect.x
        offset_y = enemy.rect.y - self.rect.y

        return self.mask.overlap(enemy.mask, (offset_x, offset_y)) is not None

    def draw(self, screen):
        """Отрисовка машины игрока"""

        screen.blit(self.image, self.rect)

        #отрисовка хитбокса для отладки
        if SHOW_HITBOX:
            mask_surf = self.mask.to_surface(setcolor=(255, 0, 0, 100),
                                             unsetcolor=(0, 0, 0, 0))
            screen.blit(mask_surf, self.rect)