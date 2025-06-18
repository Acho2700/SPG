import pygame
from pygame.math import Vector2
from game.controller.paths import *


class Monster(pygame.sprite.Sprite):
    """
        Класс монстра
    """
    def __init__(self, frames, speed=2, health=10, damage=10.0):
        """
               Инициализация монстра.

               Args:
                   frames (list): Кадры анимации.
                   speed (float, optional): Скорость монстра. По умолчанию 2.
                   health (float, optional): Здоровье монстра. По умолчанию 10.
                   damage (float, optional): Урон монстра. По умолчанию 10.0.
        """
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.scaled_image = self.frames[self.current_frame]
        self.image = self.scaled_image
        self.rect = self.image.get_rect()

        self.animation_speed = 0.1
        self.animation_timer = 0

        self.sound_radius = 1000
        self.sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds/beg-monstra-v-peschere.mp3'))
        self.sound.set_volume(0.1)
        self.is_running_sound_playing = False

        self.speed = speed
        self.health = health
        self.damage = damage
        self.target = None  # Цель (игрок)
        self.angle = 0
        self.bullets = pygame.sprite.Group()

    def update(self, player_rect, walls, bullets, waters):
        """
                Обновляет состояние монстра: анимация, движение, звук, получение урона и смерть.

                Args:
                    player_rect (pygame.Rect): Коллизии игрока.
                    walls (pygame.sprite.Group): Группа стен для проверки коллизий.
                    bullets (pygame.sprite.Group): Группа пуль игрока.
                    waters (pygame.sprite.Group): Группа водных препятствий.
        """
        moving = False

        # Анимация
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.scaled_image = self.frames[self.current_frame]

        # Поворот и движение
        if self.target:
            direction = pygame.math.Vector2(player_rect.center) - pygame.math.Vector2(self.rect.center)
            if direction.length() > 0:
                direction = direction.normalize()
                moving = True

            new_angle = direction.angle_to(pygame.math.Vector2(0, -1))

            if new_angle != self.angle:
                self.angle = new_angle
                self.image = pygame.transform.rotate(self.scaled_image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)

            # Движение
            self.rect.x += direction.x * self.speed
            if (pygame.sprite.spritecollide(self, walls, False)
                    or pygame.sprite.spritecollide(self, waters, False)):
                self.rect.x -= direction.x * self.speed

            self.rect.y += direction.y * self.speed
            if (pygame.sprite.spritecollide(self, walls, False)
                    or pygame.sprite.spritecollide(self, waters, False)):
                self.rect.y -= direction.y * self.speed

        distance = pygame.math.Vector2(self.rect.center).distance_to(player_rect.center)
        if moving and distance <= self.sound_radius:
            if not self.is_running_sound_playing:
                self.sound.play(-1)  # -1 для зацикливания звука
                self.is_running_sound_playing = True
        else:
            if self.is_running_sound_playing:
                self.sound.stop()
                self.is_running_sound_playing = False

        # Получение урона
        self.taking_damage(bullets)
        #Смерть монстра
        if self.health <= 0:
            self.sound.stop()
            self.kill()

    def taking_damage(self, bullets):
        """
                Обрабатывает получение урона от пуль.

                Args:
                    bullets (pygame.sprite.Group): Группа пуль, с которыми проверяется столкновение.
        """
        if pygame.sprite.spritecollide(self, bullets, False):
            damage = bullets.sprites()[0].damage #урон одного патрона
            self.health -= damage


class Kusaka(Monster):
    """
        Класс монстра 'Кусака'. Наследует базовый функционал от Monster.

        Особенности:
            - Уникальные кадры анимации.
            - Повышенная скорость и здоровье.
    """
    def __init__(self):
        frame1 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/Kusaka_animation/1.png')).convert_alpha()
        frame2 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/Kusaka_animation/2.png')).convert_alpha()
        frame3 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/Kusaka_animation/3.png')).convert_alpha()
        frame4 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/Kusaka_animation/4.png')).convert_alpha()
        frame5 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/Kusaka_animation/5.png')).convert_alpha()
        frame6 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/Kusaka_animation/6.png')).convert_alpha()
        frames = [
            pygame.transform.scale(frame1, (80, 80)),
            pygame.transform.scale(frame2, (80, 80)),
            pygame.transform.scale(frame3, (80, 80)),
            pygame.transform.scale(frame4, (80, 80)),
            pygame.transform.scale(frame5, (80, 80)),
            pygame.transform.scale(frame6, (80, 80)),
        ]
        super().__init__(
            frames=frames,
            speed=5,
            health=100,
            damage=0.3
        )


class Pluvaka(Monster):
    """
        Класс монстра 'Плювака'. Наследует базовый функционал от Monster.

        Особенности:
            - Может стрелять токсичными снарядами.
            - Имеет радиус стрельбы и радиус слышимости звука.
            - Пониженная скорость.
    """
    def __init__(self):
        frame1 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/pluvaka_animation/1.png')).convert_alpha()
        frame2 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/pluvaka_animation/2.png')).convert_alpha()
        frame3 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/pluvaka_animation/3.png')).convert_alpha()
        frame4 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/pluvaka_animation/4.png')).convert_alpha()
        frame5 = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/pluvaka_animation/5.png')).convert_alpha()
        frames = [
            pygame.transform.scale(frame1, (80, 100)),
            pygame.transform.scale(frame2, (80, 100)),
            pygame.transform.scale(frame3, (80, 100)),
            pygame.transform.scale(frame4, (80, 100)),
            pygame.transform.scale(frame5, (80, 100)),
        ]
        super().__init__(
            frames=frames,
            speed=2,
            health=100,
            damage=1
        )

        self.monster_bullets = pygame.sprite.Group()
        self.last_shot_time = 0
        self.spit_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds/plevok-verblyuda.mp3'))
        self.spit_sound.set_volume(0.1)

        self.shoot_radius = 600  # радиус стрельбы в пикселях
        self.sound_radius = 500  # радиус слышимости звука

    def update(self, player_rect, walls, bullets, waters):
        """
                Дополненный метод update родительского класса.
                Обновляет состояние монстра, включая стрельбу по игроку и обновление снарядов.

                Args:
                    player_rect (pygame.Rect): Коллизии игрока.
                    walls (pygame.sprite.Group): Группа стен для проверки коллизий.
                    bullets (pygame.sprite.Group): Группа пуль игрока.
                    waters (pygame.sprite.Group): Группа водных препятствий.
        """
        super().update(player_rect, walls, bullets, waters)

        # Рассчитываем расстояние до игрока
        distance_to_player = pygame.math.Vector2(self.rect.center).distance_to(player_rect.center)

        # Стрельба по таймеру
        now = pygame.time.get_ticks()
        if distance_to_player <= self.shoot_radius and now - self.last_shot_time > 3000:  # 3 секунды
            self.shoot(player_rect.center)
            self.last_shot_time = now

        # Обновление пуль
        self.monster_bullets.update(walls, self.target, waters)

    def shoot(self, target_pos):
        """
                Создаёт и выпускает токсичный снаряд в сторону цели.

                Args:
                    target_pos (tuple): Координаты цели (игрока).
        """
        bullet = ToxicBullet(
            start_pos=self.rect.center,
            target_pos=target_pos,
            speed=4,
            damage=15
        )
        self.monster_bullets.add(bullet)
        distance = pygame.math.Vector2(self.rect.center).distance_to(target_pos)
        if distance <= self.sound_radius:
            self.spit_sound.play()

    def draw_bullets(self, surface, camera):
        """Отрисовка пуль"""
        for bullet in self.monster_bullets:
            surface.blit(bullet.image, camera.apply(bullet))


class ToxicBullet(pygame.sprite.Sprite):
    """
        Класс токсичного снаряда, выпускаемого монстром Pluvaka.
    """
    def __init__(self, start_pos, target_pos, speed=4, damage=1):
        """
                Инициализация токсичного снаряда.

                Args:
                    start_pos (tuple): Начальная позиция снаряда.
                    target_pos (tuple): Позиция цели.
                    speed (float, optional): Скорость снаряда. По умолчанию 4.
                    damage (float, optional): Урон снаряда. По умолчанию 1.
        """
        super().__init__()
        self.original_image = pygame.image.load(os.path.join(ASSETS_DIR, 'monsters/toxic_ball.png')).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (24, 24))
        self.rect = self.image.get_rect(center=start_pos)

        # Параметры движения
        self.direction = Vector2(target_pos) - Vector2(start_pos)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        self.speed = speed
        self.damage = damage

    def update(self, walls, player, waters):
        """
                Обновляет положение снаряда и проверяет столкновения со стенами.

                Args:
                    walls (pygame.sprite.Group): Группа стен для проверки коллизий.
                    player: Объект игрока (не используется напрямую).
                    waters (pygame.sprite.Group): Группа водных препятствий.
        """
        # Движение
        self.rect.center += self.direction * self.speed

        # Коллизия со стенами
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()


