import pygame, utils, os
from paths import *


class Bullet(pygame.sprite.Sprite):
    """
        Базовый класс снаряда, движущегося в направлении цели с заданной скоростью и наносящего урон.
    """
    def __init__(self, image_path, size, start_pos, target_pos, speed, damage):
        """
                Инициализирует снаряд с изображением, позицией, направлением и параметрами движения.

                Args:
                    image_path (str): Путь к изображению снаряда.
                    size (tuple): Размер изображения (ширина, высота).
                    start_pos (tuple): Начальная позиция снаряда (x, y).
                    target_pos (tuple): Целевая позиция, в сторону которой летит снаряд.
                    speed (float): Скорость движения снаряда.
                    damage (int или float): Урон, наносимый при попадании.
        """
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, size)

        # Направление и поворот
        direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(start_pos)
        if direction.length() > 0:
            direction = direction.normalize()

        angle = direction.angle_to(pygame.math.Vector2(1, 0))    # Угол поворота (градусы)

        # Поворот изображения
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=start_pos)

        self.velocity = direction * speed
        self.damage = damage
        self.start_pos = pygame.math.Vector2(start_pos)



class RifleBullet(Bullet):
    """Класс снаряда винтовки с высокой скоростью и умеренным уроном."""
    def __init__(self, start_pos, target_pos, speed=15, damage=5):
        """
                Инициализирует снаряд винтовки.

                Args:
                    start_pos (tuple): Начальная позиция снаряда.
                    target_pos (tuple): Целевая позиция.
                    speed (float, optional): Скорость снаряда. По умолчанию 15.
                    damage (int, optional): Урон снаряда. По умолчанию 5.
        """
        super().__init__(
            image_path=os.path.join(ASSETS_DIR, 'Stormtrooper/ak_patron.png'),
            size=(16, 8),
            start_pos=start_pos,
            target_pos=target_pos,
            speed=speed,
            damage=4
        )


    def update(self, walls):
        """
                Обновляет позицию снаряда и уничтожает его при столкновении со стеной.

                Args:
                    walls (pygame.sprite.Group): Группа стен для проверки коллизий.
        """
        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

        if pygame.sprite.spritecollide(self, walls, False):
            self.kill()


class FireBullet(Bullet):
    """Класс огненного снаряда с большим размером, меньшей скоростью и ограниченным радиусом действия."""
    def __init__(self, start_pos, target_pos, speed=12, damage=1):
        """
                Инициализирует огненный снаряд.

                Args:
                    start_pos (tuple): Начальная позиция снаряда.
                    target_pos (tuple): Целевая позиция.
                    speed (float, optional): Скорость снаряда. По умолчанию 12.
                    damage (int, optional): Урон снаряда. По умолчанию 1.
        """
        super().__init__(
            image_path=os.path.join(ASSETS_DIR, 'Engineer/fire_patron.png'),
            size=(32, 32),
            start_pos=start_pos,
            target_pos=target_pos,
            speed=speed,
            damage=1
        )
        self.range = 500
        self.start_pos = pygame.math.Vector2(start_pos)


    def update(self, walls):
        """
                Обновляет позицию снаряда, уничтожает при столкновении со стеной или превышении радиуса действия.

                Args:
                    walls (pygame.sprite.Group): Группа стен для проверки коллизий.
        """
        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

        distance = pygame.math.Vector2(self.rect.center).distance_to(self.start_pos)
        if (pygame.sprite.spritecollide(self, walls, False)
                or distance > self.range):
            self.kill()




class Axe(Bullet):
    """Класс снаряда-топора, который вращается и возвращается к владельцу после столкновения или превышения дальности."""
    def __init__(self, owner, target_pos, speed=12, damage=5):
        """
                Инициализирует топор с вращением и звуками полёта и удара.

                Args:
                    owner (pygame.sprite.Sprite): Владелец топора (персонаж).
                    target_pos (tuple): Целевая позиция.
                    speed (float, optional): Скорость полёта. По умолчанию 12.
                    damage (int, optional): Урон топора. По умолчанию 5.
        """
        super().__init__(
            image_path=os.path.join(ASSETS_DIR, 'Tank/axe2.png'),
            size=(50, 50),
            start_pos=owner.rect.center,
            target_pos=target_pos,
            speed=speed,
            damage=4
        )
        self.original_image = pygame.image.load(os.path.join(ASSETS_DIR, 'Tank/axe2.png')).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))

        self.fly_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds/proletayuschiy-obyekt-v-vozduhe.mp3'))
        self.fly_sound.set_volume(0.1)

        self.hitting_the_wall = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds/udar-jeleznyim-mechom.mp3'))
        self.hitting_the_wall.set_volume(0.8)

        self.owner = owner  # Ссылка на персонажа
        self.rotation_angle = 0 # Текущий угол поворота (градусы)
        self.rotation_speed = 25 # Скорость вращения (градусов за кадр)
        self.is_returning = False # Флаг возврата к владельцу
        self.range = 500

    def update(self, walls):
        """
                Обновляет позицию и вращение топора, обрабатывает столкновения и возврат к владельцу.

                Args:
                    walls (pygame.sprite.Group): Группа стен для проверки коллизий.
        """
        # Движение вперед/назад
        if not self.is_returning:
            self.rect.center += self.velocity
            self.fly_sound.play()
        else:
            return_dir = (self.owner.rect.center - pygame.math.Vector2(self.rect.center)).normalize()
            self.rect.centerx += return_dir.x * 5 * 2.5
            self.rect.centery += return_dir.y * 5 * 2.5
            self.fly_sound.play()

        # Вращение
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, -self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Коллизии
        if pygame.sprite.spritecollide(self, walls, False):
            self.is_returning = True

        distance = pygame.math.Vector2(self.rect.center).distance_to(self.start_pos) #если дистанция не позволяет - возвращение
        if distance > self.range:
            self.is_returning = True

        # Возврат к персонажу
        if self.is_returning and self.rect.collidepoint(self.owner.rect.center):
            self.kill()



