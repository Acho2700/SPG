import pygame, utils

# Класс для стены
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size, texture):
        super().__init__()
        # Масштабируем текстуру под размер тайла
        self.image = pygame.transform.scale(texture, (size, size))
        # Получаем прямоугольник для позиционирования и коллизий
        self.rect = self.image.get_rect(topleft=(x, y))  # Устанавливаем позицию стены

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, size, texture):
        super().__init__()
        # Масштабируем текстуру под размер тайла
        self.image = pygame.transform.scale(texture, (size, size))
        # Получаем прямоугольник для позиционирования и коллизий
        self.rect = self.image.get_rect(topleft=(x, y))  # Устанавливаем позицию стены


# Класс уровня, который загружает карту и создаёт стены
class Level:
    def __init__(self, level_map):
        self.tile_size = utils.TILE_SIZE[0]
        self.wall_texture = pygame.image.load('tempelates/wall_block.jpg').convert()
        self.floor_texture = pygame.image.load('tempelates/floor_block.jpg').convert()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()

        self.level_width = len(level_map[0])  # Ширина в тайлах
        self.level_height = len(level_map)  # Высота в тайлах
        self.level_pixel_width = self.level_width * self.tile_size
        self.level_pixel_height = self.level_height * self.tile_size

        # # Убираем центровку уровня
        # self.offset_x = 0
        # self.offset_y = 0

        self.load_level(level_map)

    def load_level(self, level_map):
        self.spawn_point = None

        for y, row in enumerate(level_map):
            for x, char in enumerate(row):
                pos_x = x * self.tile_size
                pos_y = y * self.tile_size

                if char == '#':

                    wall = Wall(pos_x, pos_y, self.tile_size, self.wall_texture)
                    self.walls.add(wall)

                if char == '.' or char == '$':

                    floor = Floor(pos_x, pos_y, self.tile_size, self.floor_texture)
                    if char == '$':
                        print((pos_x, pos_y))
                        self.spawn_point = (pos_x, pos_y)
                    self.floors.add(floor)




                # Здесь можно добавить обработку других символов для пола, врагов и т.д.

    # Метод для отрисовки уровня (всех стен)
    def draw(self, surface):
        self.walls.draw(surface)  # Отрисовываем все стены на переданной поверхности
        self.floors.draw(surface)
