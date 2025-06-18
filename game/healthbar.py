import pygame
from paths import *

class HealthBar:
    """
    Полоса здоровья (hilfbar) для отображения текущего здоровья персонажа.

    Args:
        max_health (int): Максимальное здоровье персонажа.
    """

    def __init__(self, max_health, image):
        self.x = 180
        self.y = 93
        self.width = 302
        self.height = 10
        self.max_health = max_health
        self.current_health = max_health
        self.face = pygame.image.load(image)
        self.face = pygame.transform.scale(self.face, (80, 90))

        # Цвета
        self.bg_color = (60, 60, 60)          # Фон полосы (тёмно-серый)
        self.health_color = (0, 255, 0)       # Зеленый цвет (здоровье)
        self.border_color = (255, 255, 255)   # Белая рамка

        self.image = pygame.image.load(os.path.join(ASSETS_DIR, 'health/healthbar.png'))
        # self.image = pygame.transform.scale(self.image, (128 * 2, 200 * 2))
        self.image = pygame.transform.scale(self.image, (500, 180))

    def update(self, new_health):
        """
        Обновляет текущее здоровье.

        Args:
            new_health (int): Новое значение здоровья.
        """
        self.current_health = max(0, min(new_health, self.max_health))

    def draw(self, surface):
        """
        Рисует полосу здоровья на переданной поверхности.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        surface.blit(self.face, (82, 80), )
        surface.blit(self.image, (20, 20))


        # Рисуем фон полосы
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))

        # Вычисляем ширину заполненной части в зависимости от здоровья
        fill_width = int(self.width * (self.current_health / self.max_health))

        # Меняем цвет
        self.health_color = (155, 1, 0)

        # Рисуем заполненную часть
        pygame.draw.rect(surface, self.health_color, (self.x, self.y, fill_width, self.height))

