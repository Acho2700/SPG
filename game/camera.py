import pygame, utils

class Camera:
    """
        Класс камеры для смещения и центрирования отображаемой области игры.

        Атрибуты:
            offset (pygame.math.Vector2): Вектор смещения камеры по осям x и y.
            map_width (int): Ширина игрового мира в пикселях.
            map_height (int): Высота игрового мира в пикселях.
    """
    def __init__(self, map_width, map_height):
        self.offset = pygame.math.Vector2()
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        """
               Применяет смещение камеры к объекту для корректной отрисовки на экране.

               Args:
                   entity (pygame.sprite.Sprite): Игровой объект с атрибутом rect.

               Returns:
                   pygame.Rect: Прямоугольник объекта с учётом смещения камеры.
        """
        return entity.rect.move(-self.offset.x, -self.offset.y)

    def update(self, target):
        """
                Обновляет смещение камеры, центрируя её на целевом объекте.

                Args:
                    target (pygame.sprite.Sprite): Объект, на котором должна быть центрирована камера.
        """
        x = target.rect.centerx - utils.WIDTH // 2
        y = target.rect.centery - utils.HEIGHT // 2


        self.offset.x = x
        self.offset.y = y