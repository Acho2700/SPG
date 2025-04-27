import pygame, utils


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_path, size, start_pos, target_pos, speed, damage):
        super().__init__()

        # Загрузка и масштабирование изображения
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, size)

        # Направление и поворот
        direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(start_pos)
        if direction.length() > 0:
            direction = direction.normalize()

        # Угол поворота (градусы)
        angle = direction.angle_to(pygame.math.Vector2(1, 0))

        # Поворот изображения
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=start_pos)

        self.velocity = direction * speed
        self.damage = damage
        self.start_pos = pygame.math.Vector2(start_pos)


class RifleBullet(Bullet):
    def __init__(self, start_pos, target_pos, speed=15, damage=5):
        super().__init__(
            image_path='tempelates/Stormtrooper/ak_patron.png',
            size=(32, 32),  # Размер пули
            start_pos=start_pos,
            target_pos=target_pos,
            speed=speed,
            damage=damage
        )

    def update(self, walls):
        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

        if pygame.sprite.spritecollide(self, walls, False):
            self.kill()


class FireBullet(Bullet):
    def __init__(self, start_pos, target_pos, speed=12, damage=3):
        super().__init__(
            image_path='tempelates/Engineer/fire_patron.png',
            size=(42, 42),  # Увеличиваем размер для эффекта "пламени"
            start_pos=start_pos,
            target_pos=target_pos,
            speed=speed,
            damage=damage
        )
        self.range = 500
        self.start_pos = pygame.math.Vector2(start_pos)

    def update(self, walls):
        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

        distance = pygame.math.Vector2(self.rect.center).distance_to(self.start_pos)
        if pygame.sprite.spritecollide(self, walls, False) or distance > self.range:
            self.kill()


