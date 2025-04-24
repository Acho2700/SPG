import pygame, utils

class Camera:
    def __init__(self, map_width, map_height):
        self.offset = pygame.math.Vector2()
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        # Смещаем объект относительно камеры
        return entity.rect.move(-self.offset.x, -self.offset.y)

    def update(self, target):
        # Центрируем камеру на цели
        x = target.rect.centerx - utils.WIDTH // 2
        y = target.rect.centery - utils.HEIGHT // 2


        self.offset.x = x
        self.offset.y = y