# настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
ROAD_COLOR = (40, 40, 40)
GREEN = (34, 139, 34)

# параметры игрока
PLAYER_SIZE = (60, 90)
PLAYER_START_POS = (SCREEN_WIDTH//2 - 25, SCREEN_HEIGHT - 150)
PLAYER_SPEED_FORWARD = 5
PLAYER_SPEED_BACKWARD = 3
PLAYER_MIN_Y = 100
PLAYER_SPEED_INFLUENCE = 0.7

# параметры дороги
ROAD_WIDTH = 400
ROAD_MARK_WIDTH = 10
ROAD_MARK_HEIGHT = 50
ROAD_MARK_GAP = 100

# настройки скорости игры
BASE_SPEED = 5.0
MAX_SPEED = 8.0

# параметры вражеских машин
ENEMY_SIZES = [(55, 95), (75, 130)]

# настройки монеток
COIN_SIZE = (30, 30)
COIN_VALUE = 5

# настройки для обочины
BACKGROUND_IMAGE = 'images/png/bg.jpg'
BACKGROUND_SPEED_RATIO = 0.8
BACKGROUND_HEIGHT_RATIO = 1.2

SHOW_HITBOX = False
SIDEWALK_SPEED_RATIO = 0.8

# настройки для звука
SOUNDS_DIR = 'sounds'
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7

# звук для саунд.ру
SOUND_COIN = 'coins.mp3'
SOUND_GAME = 'game.wav'
SOUND_GAMEOVER = 'gameover.wav'
SOUND_MENU = 'menu.mp3'