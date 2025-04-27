import pygame
import utils
from Projectile import RifleBullet

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, pos=(0, 0), speed=5):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.original_image, utils.TILE_SIZE)
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)
        self.angle = 0  # Храним последний угол поворота

        #для стрельбы
        self.bullets = pygame.sprite.Group()
        self.shoot_cooldown = 0
        self.shoot_delay = 0

    def update(self, keys_pressed, walls):
        dx = dy = 0
        if keys_pressed[pygame.K_w]: dy -= self.speed
        if keys_pressed[pygame.K_s]: dy += self.speed
        if keys_pressed[pygame.K_a]: dx -= self.speed
        if keys_pressed[pygame.K_d]: dx += self.speed

        # Обновляем направление для поворота (если нужно)
        direction = pygame.math.Vector2(dx, dy)
        if direction.length() != 0:
            direction = direction.normalize()
            self.angle = direction.angle_to(pygame.math.Vector2(0, -1))

        # Двигаем персонажа с учётом коллизий
        self.move(dx, dy, walls)

        # Поворачиваем изображение под угол
        self.image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, dx, dy, walls):
        # Сохраняем старую позицию
        old_pos = self.rect.copy()

        # Пробуем двигаться по X
        self.rect.x += dx
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x = old_pos.x

        # Пробуем двигаться по Y
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y = old_pos.y


# Дочерние классы персонажей

class Tank(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Tank/game_model_t-Photoroom.png', pos, speed=5)  # Можно задать уникальную скорость


class Engineer(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Engineer/game_model_e.png', pos, speed=5)


class Stormtrooper(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Stormtrooper/game_model_s.png', pos, speed=5)
        self.burst_count = 0  # Текущий счётчик очереди
        self.burst_size = 3  # Размер очереди
        self.burst_delay = 7  # Задержка между пулями
        self.shoot_cooldown = 0  # Таймер задержки
        self.bullets = pygame.sprite.Group()

    def handle_shooting(self, target_pos, mouse_click, walls):
        """
        Обработка стрельбы по мышке
        :param target_pos: позиция курсора
        :param mouse_click: состояние кнопки мыши
        :param walls: группа стен для коллизий
        """
        if mouse_click[0] and self.burst_count == 0 and self.shoot_cooldown <= 0:
            self.burst_count = self.burst_size
            self.shoot_cooldown = 20

        if self.burst_count > 0 and self.shoot_cooldown <= 0:
            bullet = RifleBullet(
                start_pos=self.rect.center,
                target_pos=target_pos
            )
            self.bullets.add(bullet)
            self.burst_count -= 1
            self.shoot_cooldown = self.burst_delay

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


        self.bullets.update(walls)

