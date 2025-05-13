import pygame, random, os
from potion import HealthPotion, SpeedPotion
from paths import *


class Chest(pygame.sprite.Sprite):
    def __init__(self, closed_image_path, opened_image_path, pos, size, direction='n', potion_group=None, potion_classes=None, player=None):
        """
        Args:
            closed_image_path (str): Путь к изображению закрытого сундука.
            opened_image_path (str): Путь к изображению открытого сундука.
            pos (tuple): Координаты (x, y) для размещения сундука.
        """
        super().__init__()
        self.closed_image = pygame.image.load(closed_image_path).convert_alpha()
        self.closed_image = pygame.transform.scale(self.closed_image, (size, size))
        self.opened_image = pygame.image.load(opened_image_path).convert_alpha()
        self.opened_image = pygame.transform.scale(self.opened_image, (size, size))

        self.sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds/open-magic-chest.mp3'))
        self.sound.set_volume(0.1)

        angle = 0
        if direction == 'n':
            angle = 0
        elif direction == 'e':
            angle = -90
        elif direction == 's':
            angle = 180
        elif direction == 'w':
            angle = 90

        self.closed_image = pygame.transform.rotate(self.closed_image, angle)
        self.opened_image = pygame.transform.rotate(self.opened_image, angle)

        self.image = self.closed_image
        self.rect = self.image.get_rect(topleft=pos)
        self.is_opened = False

        self.potion_group = potion_group  # группа для зелья
        self.potion_classes = potion_classes  # список классов зелий (например, [HealthPotion])
        self.player = player  # ссылка на игрока, чтобы передать в зелье

    def set_potions(self, potion_classes):
        self.potion_classes = potion_classes

    def set_player(self, player):
        self.player = player

    def update(self, player_rect):
        """
        Проверяет столкновение с игроком и открывает сундук при первом контакте.

        Args:
            player_rect (pygame.Rect): Прямоугольник игрока для проверки коллизии.
        """
        if self.is_opened:
            return  # Уже открыт, ничего не делаем

            # Создаём расширенный прямоугольник вокруг сундука (например, на 10 пикселей больше с каждой стороны)
        expanded_rect = self.rect.inflate(20, 20)  # расширение на 20 пикселей по ширине и высоте

        # Проверяем пересечение с расширенным прямоугольником
        if expanded_rect.colliderect(player_rect):
            self.open()

    def open(self):
        """Открывает сундук и меняет изображение."""
        self.sound.play()
        self.is_opened = True
        self.image = self.opened_image
        self.drop_potion()

    def drop_potion(self):
        if  self.potion_classes and self.player:
            PotionClass = random.choice(self.potion_classes)
            potion = PotionClass(self.rect.center)
            potion.player = self.player

            self.potion_group.add(potion)  # добавляем в группу спрайтов
        else:
