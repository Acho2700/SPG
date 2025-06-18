import pygame
from game.models import utils
from game.models.chest import Chest
from game.models.potion import HealthPotion, SpeedPotion
from game.controller.paths import *

class Obstacle(pygame.sprite.Sprite):
    """
      Класс препятствия на карте (стена, вода и т.п.).

      Атрибуты:
          image (pygame.Surface): Текущая текстура препятствия.
          rect (pygame.Rect): Прямоугольник для позиционирования и коллизий.
          water_textures (tuple or list): Кортеж/список из текстур для анимации воды (если есть).
          size (int): Размер тайла (ширина и высота).
          current_texture_index (int): Индекс текущей текстуры для анимации.
          last_switch_time (int): Время последнего переключения текстуры (в миллисекундах).
          switch_interval (int): Интервал переключения текстуры (в миллисекундах).
    """

    def __init__(self, x, y, size, texture, water_textures=None):
        """
               Инициализация препятствия.

               Args:
                   x (int): Координата X верхнего левого угла.
                   y (int): Координата Y верхнего левого угла.
                   size (int): Размер тайла (ширина и высота).
                   texture (pygame.Surface): Текстура препятствия.
                   water_textures (tuple or list, optional): Текстуры для анимации воды.
        """
        super().__init__()
        self.image = pygame.transform.scale(texture, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.water_textures = water_textures
        self.size = size
        self.current_texture_index = 0
        self.last_switch_time = 0
        self.switch_interval = 500
    def animation(self, current_time):
        """
                Обновляет анимацию воды, переключая текстуры с заданным интервалом.

                Args:
                    current_time (int): Текущее время в миллисекундах (обычно pygame.time.get_ticks()).
        """

        if self.water_textures is None:
            return  # Не вода, анимация не нужна

        # Проверка прошёл ли интервал переключения
        if current_time - self.last_switch_time > self.switch_interval:
            self.current_texture_index = (self.current_texture_index + 1) % len(self.water_textures)
            new_texture = self.water_textures[self.current_texture_index]
            self.image = pygame.transform.scale(new_texture, (self.size, self.size))
            self.last_switch_time = current_time




class Level:
    """
        Класс уровня, загружающий и хранящий карту, текстуры и группы спрайтов.

        Атрибуты:
            tile_size (int): Размер одного тайла в пикселях.
            wall_texture (pygame.Surface): Текстура стены.
            floor_texture (pygame.Surface): Текстура пола.
            water_texture1 (pygame.Surface): Первая текстура воды для анимации.
            water_texture2 (pygame.Surface): Вторая текстура воды для анимации.
            walls (pygame.sprite.Group): Группа спрайтов стен.
            floors (pygame.sprite.Group): Группа спрайтов пола.
            waters (pygame.sprite.Group): Группа спрайтов воды.
            list_level_map (list): Список строк карты уровня.
            level_width (int): Ширина уровня в тайлах.
            level_height (int): Высота уровня в тайлах.
            level_pixel_width (int): Ширина уровня в пикселях.
            level_pixel_height (int): Высота уровня в пикселях.
            spawn_point (tuple): Координаты точки спавна игрока.
            spawn_monster (list): Список координат спавнеров монстров.
    """
    def __init__(self, level_map):
        """
                Инициализация уровня.

                Args:
                    level_map : Файл, представляющих карту уровня.
        """
        self.tile_size = utils.TILE_SIZE[0]
        self.wall_texture = pygame.image.load(os.path.join(ASSETS_DIR, 'wall2.jpg')).convert()
        self.floor_texture = pygame.image.load(os.path.join(ASSETS_DIR, 'floor2.jpg')).convert()
        self.water_texture1 = pygame.image.load(os.path.join(ASSETS_DIR, 'water_r.jpg')).convert()
        self.water_texture2 = pygame.image.load(os.path.join(ASSETS_DIR, 'water_l.jpg')).convert()
        self.portal_texture1 = pygame.image.load(os.path.join(ASSETS_DIR, 'portal_1.png')).convert()
        self.portal_texture2 = pygame.image.load(os.path.join(ASSETS_DIR, 'portal_2.png')).convert()
        self.portal_texture3 = pygame.image.load(os.path.join(ASSETS_DIR, 'portal_3.png')).convert()
        self.walls = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.waters = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.potions = pygame.sprite.Group()  # Группа для зелий

        self.list_level_map = []
        # Считывание файла
        for s in level_map:
            self.list_level_map.append(s)

        self.level_width = len(self.list_level_map[0])  # Ширина в тайлах
        self.level_height = len(self.list_level_map)  # Высота в тайлах
        self.level_pixel_width = self.level_width * self.tile_size
        self.level_pixel_height = self.level_height * self.tile_size

        self.chest_potions = [HealthPotion, SpeedPotion]
        self.player = None

        self.load_level(self.list_level_map)        # Загрузка уровня

    def set_player(self, player):
        self.player = player
        for chest in self.chests:
            chest.set_player(player)

    def load_level(self, level_map):
        """
                Загружает уровень из списка строк, создавая объекты и добавляя их в группы.

                Args:
                    level_map (list): Список строк карты уровня.
        """
        self.spawn_point = None
        self.spawn_monster = []         # Список спавнеров монстров
        self.chest = None

            # -- Генерация блоков и др --
        for y, row in enumerate(level_map):
            for x, char in enumerate(row):
                pos_x = x * self.tile_size
                pos_y = y * self.tile_size

                if char == '#':

                    wall = Obstacle(pos_x, pos_y, self.tile_size, self.wall_texture)
                    self.walls.add(wall)

                if char == '-':
                    water = Obstacle(pos_x, pos_y, self.tile_size, self.water_texture1,
                                     water_textures=(self.water_texture1,
                                                     self.water_texture2
                                                     ))
                    self.waters.add(water)

                if char == '0':
                    portal = Obstacle(pos_x, pos_y, self.tile_size, self.water_texture1,
                                     water_textures=(self.portal_texture1,
                                                     self.portal_texture2,
                                                     self.portal_texture3
                                                     ))
                    self.portals.add(portal)

                if char in ('n', 's', 'w', 'e'):
                    chest = Chest(
                        closed_image_path= os.path.join(ASSETS_DIR, 'chest_close.png'),
                        opened_image_path=os.path.join(ASSETS_DIR, 'cheast_open.png'),
                        pos=(pos_x, pos_y),
                        size=self.tile_size,
                        direction=char,
                        potion_group=self.potions,
                        potion_classes=self.chest_potions,
                        player=self.player
                    )
                    chest.set_potions(self.chest_potions)
                    self.chests.add(chest)
                    self.walls.add(chest)

                if char in ('.', '$', '*'):

                    floor = Obstacle(pos_x, pos_y, self.tile_size, self.floor_texture)

                    if char == '$':
                        self.spawn_point = (pos_x, pos_y)

                    if char == '*':
                        self.spawn_monster.append((pos_x, pos_y))


                    self.floors.add(floor)



