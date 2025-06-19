import pygame
import random
import os
from settings import *


class Coin:
    def __init__(self, x, y):
        """ основ параметры монетки """
        self.size = (30, 30)  # размер 30x30 пикселей
        self.image = self.load_coin_image()  # загрузка спрайта
        self.rect = self.image.get_rect(topleft=(x, y))  # хитбокс для коллизий
        self.collected = False  # флаг, собрана ли монеткай

    def load_coin_image(self):
        """ загрузка спрайта """
        try:  # пытаемся загрузить изображение монетки
            paths = [
                os.path.join('images', 'png', 'coin.png'),
                os.path.join('images', 'coin.png')
            ]

            for path in paths:
                if os.path.exists(path):
                    img = pygame.image.load(path).convert_alpha()
                    # масштабируем если размер не совпадает
                    return pygame.transform.scale(img, self.size)\
                        if img.get_size() != self.size else img

            # Если файл не найден - создаем простую монетку
            surf = pygame.Surface(self.size, pygame.SRCALPHA)
            pygame.draw.circle(surf,  (255, 215, 0),
                               (15, 15), 15)  # желтый круг
            return surf

        except Exception as e: # настроить спрайты уже
            print(f"Ошибка загрузки монетки: {e}")

            # заглушка при ошибке
            surf = pygame.Surface(self.size, pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 215, 0),
                               (15, 15), 15)

            return surf

    def draw(self, screen):
        """ ттрисовка только если не собрана """
        if not self.collected:
            screen.blit(self.image, self.rect)


class Coins:
    def __init__(self):
        self.coins = []  # список монеток на дороге которые
        self.spawn_chance = 0.005  # 0.5% шанс появления
        self.last_spawn_time = 0  # для контроля частоты спавна

    def can_spawn(self, new_rect, enemies):
        """ проверка возможности спавна """

        # проверка расстояния до врагов
        for enemy in enemies:
            if new_rect.inflate(40, 40).colliderect(enemy.rect.inflate(40, 40)): #40 пикс
                return False

        # проверка расстояния до других монеток
        for coin in self.coins:
            if new_rect.inflate(20, 20).colliderect(coin.rect.inflate(20, 20)):
                return False

        return True

    def spawn_coin(self, enemies):
        """ спавн новой монетки """

        if random.random() < self.spawn_chance:
            # 5 попыток найти подходящее место
            for _ in range(5):
                # случайная позиция в пределах дороги
                x = random.randint(
                    SCREEN_WIDTH // 2 - ROAD_WIDTH // 2 + 30,
                    SCREEN_WIDTH // 2 + ROAD_WIDTH // 2 - 30
                )
                new_rect = pygame.Rect(x, -30, 30, 30)

                if self.can_spawn(new_rect, enemies):
                    self.coins.append(Coin(x, -30))
                    return True

        return False

    def update(self, enemies, player):
        """ обновление монеток и их проверка """
        collected = 0  # счетчик собранных монет

        # обновляем состояние всех монеток
        for coin in self.coins[:]:  # копия списка
            if not coin.collected:
                # двигаем монетку
                coin.rect.y += BASE_SPEED * 0.8

                # проверка столкновения с игроком
                if player.rect.colliderect(coin.rect):
                    coin.collected = True
                    collected += 1

            # удаляем вышедшие за экран монетки
            elif coin.rect.top > SCREEN_HEIGHT + 50:
                self.coins.remove(coin)

        # пытаемся создать новую монетку
        self.spawn_coin(enemies)

        return collected  # возвращаем количество собранных монет

    def draw(self, screen):
        #отрисовка всех активных монеток

        for coin in self.coins:
            coin.draw(screen)