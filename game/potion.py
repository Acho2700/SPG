import pygame, os
import random
from paths import *


class Potion(pygame.sprite.Sprite):
    def __init__(self, image_path, size, pos, sound):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = self.original_image
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(center=pos)

        self.sound = pygame.mixer.Sound(sound)
        self.sound.set_volume(0.1)

        # Параметры падения
        self.float_distance = 27  # на сколько пикселей падает зелье
        self.float_speed = 2  # скорость падения (пикселей за кадр)
        self.start_y = self.rect.y  # начальная позиция по Y
        self.falling = True  # флаг падения

    def update(self, player_rect):
        if self.falling:
            self.rect.y += self.float_speed
            if self.rect.y >= self.start_y + self.float_distance:
                self.rect.y = self.start_y + self.float_distance
                self.falling = False  # остановить падение

            # Здесь можно добавить проверку подбора игроком
        if self.rect.colliderect(player_rect):
            self.on_pickup()
            self.kill()


    def on_pickup(self):
        """
        Метод вызывается при подборе зелья игроком.
        В дочерних классах переопределяется для конкретного эффекта.
        """
        self.picked_up = True
        self.kill()  # Удаляем зелье из игры

class HealthPotion(Potion):
    def __init__(self, pos):
        super().__init__(os.path.join(ASSETS_DIR, 'health_potion.png'),
                         (32, 40),
                         pos,
                         os.path.join(ASSETS_DIR, 'sounds/sound_potion.mp3')
                         )
        self.heal_amount = 20

    def on_pickup(self):
        if hasattr(self, 'player'):
            self.sound.play()
            self.player.health = self.player.health + self.heal_amount

class SpeedPotion(Potion):
    def __init__(self, pos):
        super().__init__(os.path.join(ASSETS_DIR, 'speed_potion.png'),
                         (40, 40),
                         pos,
                         os.path.join(ASSETS_DIR, 'sounds/sound_book.mp3')
                         )
        self.speed_amount = 2
        self.effect_duration = 10000

    def on_pickup(self):
        if hasattr(self, 'player'):
            self.sound.play()
            self.player.speed = self.player.speed + self.speed_amount





