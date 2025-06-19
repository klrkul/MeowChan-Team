import pygame
import os
from settings import *


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {} #через словарь я добавила по ключу искать будем
        self.current_music = None
        self.load_sounds()

    def load_sounds(self):
        pygame.mixer.music.load(
            os.path.join(SOUNDS_DIR,SOUND_GAME))

        self.sounds['coin'] = pygame.mixer.Sound(
            os.path.join(SOUNDS_DIR, SOUND_COIN))

        self.sounds['gameover'] = pygame.mixer.Sound(
            os.path.join(SOUNDS_DIR, SOUND_GAMEOVER))

        self.sounds['menu'] = pygame.mixer.Sound(
            os.path.join(SOUNDS_DIR, SOUND_MENU))

        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        for sound in self.sounds.values():
            sound.set_volume(SFX_VOLUME)

    def play_music(self, track_name, loops=-1): #бесконечно воспроизводим
        if (track_name == 'game'
                and self.current_music != 'game'):
            pygame.mixer.music.load(
                os.path.join(SOUNDS_DIR, SOUND_GAME))
            pygame.mixer.music.play(loops)
            self.current_music = 'game'

        elif (track_name == 'menu'
              and self.current_music != 'menu'):
            pygame.mixer.music.load(
                os.path.join(SOUNDS_DIR, SOUND_MENU))
            pygame.mixer.music.play(loops)
            self.current_music = 'menu'

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def set_sfx_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)
