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
        self.tile_size = utils.TILE_SIZE[0]  # Размер одного блока (тайла)
        self.wall_texture = pygame.image.load('tempelates/wall_block.jpg') # Текстура для стен
        self.floor_texture = pygame.image.load('tempelates/floor_block.jpg')  # Текстура для стен
        self.walls = pygame.sprite.Group()  # Группа спрайтов для стен
        self.floors = pygame.sprite.Group()

        self.level_pixel_width = len(level_map[0]) * self.tile_size
        self.level_pixel_height = len(level_map) * self.tile_size

        # Вычисляем смещение для центровки
        self.offset_x = (utils.WIDTH - self.level_pixel_width) // 2
        self.offset_y = (utils.HEIGHT - self.level_pixel_height) // 2

        self.load_level(level_map)  # Загружаем уровень из карты


    # Метод для загрузки уровня по карте (список строк)
    def load_level(self, level_map):
        # Проходим по каждой строке с индексом y
        for y, row in enumerate(level_map):
            # Проходим по каждому символу в строке с индексом x
            for x, char in enumerate(row):
                # Вычисляем позицию на экране по координатам в карте
                # Если символ '#' — создаём стену
                if char == '#':
                    pos_x = self.offset_x + x * self.tile_size
                    pos_y = self.offset_y + y * self.tile_size
                    wall = Wall(pos_x, pos_y, self.tile_size, self.wall_texture)
                    self.walls.add(wall)  # Добавляем стену в группу

                if char == '.':
                    pos_x = self.offset_x + x * self.tile_size
                    pos_y = self.offset_y + y * self.tile_size
                    floor = Floor(pos_x, pos_y, self.tile_size, self.floor_texture)
                    self.floors.add(floor)  # Добавляем стену в группу

                # Здесь можно добавить обработку других символов для пола, врагов и т.д.

    # Метод для отрисовки уровня (всех стен)
    def draw(self, surface):
        self.walls.draw(surface)  # Отрисовываем все стены на переданной поверхности
        self.floors.draw(surface)
