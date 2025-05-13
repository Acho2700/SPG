import pygame, utils, os
from projectile import RifleBullet, FireBullet, Axe
from paths import *

class Character(pygame.sprite.Sprite):
    """
        Класс персонажа игрока.

        Атрибуты:
            original_image (pygame.Surface): Исходное изображение персонажа.
            scaled_image (pygame.Surface): Масштабированное изображение под размер тайла.
            image (pygame.Surface): Текущее изображение персонажа (с учётом поворота).
            rect (pygame.Rect): Прямоугольник для позиционирования и коллизий.
            speed (int): Скорость перемещения персонажа.
            direction (pygame.math.Vector2): Вектор направления движения.
            angle (float): Текущий угол поворота персонажа.
            health (int): Здоровье персонажа.
            bullets (pygame.sprite.Group): Группа пуль, выпущенных персонажем.
    """
    def __init__(self, image_path, pos=(0, 0), speed=5, max_speed=9, health=100, max_health=100):
        """
               Инициализация персонажа.

               Args:
                   image_path (str): Путь к изображению персонажа.
                   pos (tuple): Начальная позиция (x, y) персонажа.
                   speed (int): Скорость перемещения.
                   health (int): Начальное здоровье.
        """
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.original_image, utils.TILE_SIZE)
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center=pos)

        self.hit_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds/monstr-est-plot.mp3'))
        self.hit_sound.set_volume(0.1)
        self.is_hit_sound_playing = False

        self.speed = speed
        self.max_speed = max_speed
        self.direction = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.health = health
        self.max_health = max_health
        self.bullets = pygame.sprite.Group()

    def update(self, keys_pressed, walls, monsters, monster_bullets, waters):
        """
               Обновляет состояние персонажа: движение, поворот, получение урона.

               Args:
                   keys_pressed (list): Список нажатых клавиш.
                   walls (pygame.sprite.Group): Группа стен для коллизий.
                   monsters (pygame.sprite.Group): Группа монстров для проверки урона.
                   monster_bullets (pygame.sprite.Group): Группа пуль монстров.
                   waters (pygame.sprite.Group): Группа водных препятствий для коллизий.

               Returns:
                   bool: True, если персонаж умер (здоровье <= 0), иначе False.
        """
        dx = dy = 0
        if keys_pressed[pygame.K_w]: dy -= self.speed
        if keys_pressed[pygame.K_s]: dy += self.speed
        if keys_pressed[pygame.K_a]: dx -= self.speed
        if keys_pressed[pygame.K_d]: dx += self.speed

        # Обновляем направление для поворота (если есть движение)
        direction = pygame.math.Vector2(dx, dy)
        if direction.length() != 0:
            direction = direction.normalize()
            self.angle = direction.angle_to(pygame.math.Vector2(0, -1))

        # Двигаем персонажа с учётом коллизий
        self.move(dx, dy, walls, waters)

        # Поворачиваем изображение персонажа под текущий угол
        self.image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Проверяем получение урона от монстров и пуль
        self.taking_damage(monsters, monster_bullets)

        if self.health > self.max_health:
            self.health = self.max_health

        if self.speed > self.max_speed:
            self.speed = self.max_speed

        if self.health <= 0:
            self.hit_sound.stop()
            for monster in monsters: # Выклбчение звуков для всех монстров
                monster.sound.stop()
            self.kill()
            return True  # Персонаж умер
        return False

    def move(self, dx, dy, walls, waters):
        """
                Перемещает персонажа с учётом коллизий со стенами и водой.

                Args:
                    dx (int): Смещение по оси X.
                    dy (int): Смещение по оси Y.
                    walls (pygame.sprite.Group): Группа стен.
                    waters (pygame.sprite.Group): Группа водных препятствий.
        """


        # Двигаемся по X и проверяем коллизии
        self.rect.x += dx
        if pygame.sprite.spritecollide(self, walls, False) or pygame.sprite.spritecollide(self, waters, False):
            self.rect.x -= dx

        # Двигаемся по Y и проверяем коллизии
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, walls, False) or pygame.sprite.spritecollide(self, waters, False):
            self.rect.y -= dy

    def taking_damage(self, monsters, monster_bullets):
        collided_monsters = pygame.sprite.spritecollide(self, monsters, False)
        collided_bullets = pygame.sprite.spritecollide(self, monster_bullets, True)

        damage_taken = 0

        for monster in collided_monsters:
            damage_taken += monster.damage

        for bullet in collided_bullets:
            damage_taken += bullet.damage

        if damage_taken > 0:
            self.health -= damage_taken
            if not self.is_hit_sound_playing:
                self.hit_sound.play(-1)  # Запускаем звук в зацикленном режиме
                self.is_hit_sound_playing = True
        else:
            # Если урона нет, останавливаем звук, если он играет
            if self.is_hit_sound_playing:
                self.hit_sound.stop()
                self.is_hit_sound_playing = False


# Дочерние классы персонажей

class Tank(Character):
    """
        Класс танка - специализированный персонаж с возможностью бросать топор.

        Атрибуты:
            image_with_axe (pygame.Surface): Изображение танка с топором.
            original_image (pygame.Surface): Исходное изображение танка.
            throw_cooldown (int): Текущий кулдаун перед следующим броском топора.
            throw_delay (int): Задержка (в кадрах) между бросками топора.
            bullets (pygame.sprite.Group): Группа активных топоров (снарядов).
            health (int): Здоровье танка.
        """
    def __init__(self, pos=(0, 0)):
        """
                Инициализация танка.

                Args:
                    pos (tuple): Начальная позиция (x, y).
        """

        super().__init__(os.path.join(ASSETS_DIR, 'Tank/game_model_t_axe.png'), pos, speed=5, health=200, max_health=200)
        self.image_with_axe = pygame.image.load(os.path.join(ASSETS_DIR, 'Tank/game_model_t-Photoroom.png')).convert_alpha()
        self.image_with_axe = pygame.transform.scale(self.image_with_axe, self.rect.size)
        self.original_image = self.image

        self.shoot_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR,'sounds/vzmah-toporom.mp3'))
        self.shoot_sound.set_volume(0.1)

        self.throw_cooldown = 0
        self.throw_delay = 60     # Задержка между бросками (примерно 1 секунда при 60 FPS)
        self.bullets = pygame.sprite.Group()
        self.health = 200

    def handle_shooting(self, target_pos, mouse_click, walls):
        """
                Обрабатывает логику броска топора и обновление пуль (топоров).

                Args:
                    target_pos (tuple): Координаты цели для броска.
                    mouse_click (tuple): Состояние кнопок мыши (например, pygame.mouse.get_pressed()).
                    walls (pygame.sprite.Group): Группа стен для проверки коллизий пуль.
        """
        # Удаляем мертвые топоры из группы
        self.bullets = pygame.sprite.Group([b for b in self.bullets if b.alive()])

        # Проверка есть ли активный топор
        has_axe = len(self.bullets) > 0

        # Переключаем изображение танка в зависимости от наличия топора
        if has_axe:
            self.image = self.image_with_axe
        else:
            self.image = self.original_image

        # Обновляем rect и маску для корректной коллизии
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

        # Бросок при условии
        if mouse_click[0] and len(self.bullets) == 0 and self.throw_cooldown <= 0:
            new_axe = Axe(owner=self, target_pos=target_pos)
            self.bullets.add(new_axe)
            self.throw_cooldown = self.throw_delay
            self.shoot_sound.play()

        # Обновление кулдауна
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

        # Обновляем все активные топоры
        self.bullets.update(walls)


class Engineer(Character):
    """
        Класс инженера - персонаж с возможностью вести очередь из выстрелов (burst fire).

        Атрибуты:
            burst_count (int): Текущий счётчик оставшихся выстрелов в очереди.
            burst_size (int): Размер очереди выстрелов.
            burst_delay (int): Задержка между выстрелами в очереди (в кадрах).
            shoot_cooldown (int): Таймер задержки между выстрелами.
            bullets (pygame.sprite.Group): Группа пуль, выпущенных инженером.
            health (int): Здоровье персонажа.
    """
    def __init__(self, pos=(0, 0)):
        """
                Инициализация инженера.

                Args:
                    pos (tuple): Начальная позиция (x, y).
        """
        super().__init__(os.path.join(ASSETS_DIR,'Engineer/game_model_e.png'), pos, speed=5, health=100, max_health=100)
        self.burst_count = 0  # Текущий счётчик очереди
        self.burst_size = 30  # Размер очереди
        self.burst_delay = 2  # Задержка между выстрелами (в кадрах)
        self.shoot_cooldown = 0  # Таймер задержки
        self.shoot_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR,'sounds/engeenir_shot.mp3'))
        self.shoot_sound.set_volume(0.1)
        self.bullets = pygame.sprite.Group()
        self.health = 100


    def handle_shooting(self, target_pos, mouse_click, walls):
        """
        Обрабатывает стрельбу инженера с очередью выстрелов по нажатию мыши.

        Args:
            target_pos (tuple): Координаты курсора мыши (цель).
            mouse_click (tuple): Состояние кнопок мыши (например, pygame.mouse.get_pressed()).
            walls (pygame.sprite.Group): Группа стен для проверки коллизий пуль.
        """
        # Запуск очереди выстрелов при первом нажатии и отсутствии текущей очереди
        if mouse_click[0] and self.burst_count == 0 and self.shoot_cooldown <= 0:
            self.burst_count = self.burst_size
            self.shoot_cooldown = 60   # Задержка перед началом очереди

        if self.burst_count == 29:
            self.shoot_sound.play()

        # Выполнение выстрелов из очереди с задержкой между ними
        if self.burst_count > 0 and self.shoot_cooldown <= 0:

            bullet = FireBullet(
                start_pos=self.rect.center,
                target_pos=target_pos,
            )
            self.bullets.add(bullet)
            self.burst_count -= 1
            self.shoot_cooldown = self.burst_delay   # Задержка между выстрелами


        # Уменьшаем таймер задержки, если он активен
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Обновляем все пули (движение и коллизии)
        self.bullets.update(walls)


class Stormtrooper(Character):
    """
        Класс штурмовика - персонаж с очередной стрельбой из трёх выстрелов (burst fire).

        Атрибуты:
            burst_count (int): Текущий счётчик оставшихся выстрелов в очереди.
            burst_size (int): Размер очереди выстрелов (3 выстрела).
            burst_delay (int): Задержка между выстрелами в очереди (в кадрах).
            shoot_cooldown (int): Таймер задержки между выстрелами.
            bullets (pygame.sprite.Group): Группа пуль, выпущенных штурмовиком.
            health (int): Здоровье персонажа.
    """
    def __init__(self, pos=(0, 0)):
        """
                Инициализация штурмовика.

                Args:
                    pos (tuple): Начальная позиция (x, y).
        """
        super().__init__(os.path.join(ASSETS_DIR,'Stormtrooper/game_model_s.png'), pos, speed=5, health=150, max_health=150)
        self.burst_count = 0  # Текущий счётчик очереди
        self.burst_size = 3  # Размер очереди
        self.burst_delay = 7  # Задержка между выстрелами (в кадрах)
        self.shoot_cooldown = 0  # Таймер задержки
        self.shoot_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR,'sounds/stormtrooper_shot.mp3'))
        self.shoot_sound.set_volume(0.1)
        self.bullets = pygame.sprite.Group()
        self.health = 150

    def handle_shooting(self, target_pos, mouse_click, walls):
        """
        Обрабатывает стрельбу штурмовика с очередью из трёх выстрелов по нажатию мыши.

        Args:
            target_pos (tuple): Координаты курсора мыши (цель).
            mouse_click (tuple): Состояние кнопок мыши (например, pygame.mouse.get_pressed()).
            walls (pygame.sprite.Group): Группа стен для проверки коллизий пуль.
        """

        # Запуск очереди выстрелов при первом нажатии и отсутствии текущей очереди
        if mouse_click[0] and self.burst_count == 0 and self.shoot_cooldown <= 0:
            self.burst_count = self.burst_size
            self.shoot_cooldown = 20   # Задержка перед началом очереди

        # Выполнение выстрелов из очереди с задержкой между ними
        if self.burst_count > 0 and self.shoot_cooldown <= 0:
            bullet = RifleBullet(
                start_pos=self.rect.center,
                target_pos=target_pos
            )
            self.bullets.add(bullet)
            self.burst_count -= 1
            self.shoot_cooldown = self.burst_delay
            self.shoot_sound.play()


        # Уменьшаем таймер задержки, если он активен
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Обновляем все пули (движение и коллизии)
        self.bullets.update(walls)

