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
            size=(16, 8),  # Размер пули
            start_pos=start_pos,
            target_pos=target_pos,
            speed=speed,
            damage=4
        )

    def update(self, walls):
        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

        if pygame.sprite.spritecollide(self, walls, False):
            self.kill()


class FireBullet(Bullet):
    def __init__(self, start_pos, target_pos, speed=12, damage=5):
        super().__init__(
            image_path='tempelates/Engineer/fire_patron.png',
            size=(32, 32),  # Увеличиваем размер для эффекта "пламени"
            start_pos=start_pos,
            target_pos=target_pos,
            speed=speed,
            damage=1
        )
        self.range = 500
        self.start_pos = pygame.math.Vector2(start_pos)

    def update(self, walls):
        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

        distance = pygame.math.Vector2(self.rect.center).distance_to(self.start_pos)
        if pygame.sprite.spritecollide(self, walls, False) or distance > self.range:
            self.kill()




class Axe(Bullet):
    def __init__(self, owner, target_pos, speed=12, damage=5):
        super().__init__(
            image_path='tempelates/Tank/axe2.png',
            size=(50, 50),
            start_pos=owner.rect.center,
            target_pos=target_pos,
            speed=speed,
            damage=4
        )
        self.owner = owner  # Ссылка на персонажа
        self.rotation_angle = 0 # Текущий угол поворота (градусы)
        self.rotation_speed = 25 # Скорость вращения (градусов за кадр)
        self.is_returning = False # Флаг возврата к владельцу
        self.original_image = pygame.image.load('tempelates/Tank/axe2.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.range = 500

    def update(self, walls):
        # Движение вперед/назад
        if not self.is_returning:
            self.rect.center += self.velocity
        else:
            return_dir = (self.owner.rect.center - pygame.math.Vector2(self.rect.center)).normalize()
            self.rect.centerx += return_dir.x * 5 * 2.5
            self.rect.centery += return_dir.y * 5 * 2.5

        # Вращение
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, -self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Коллизии
        if pygame.sprite.spritecollide(self, walls, False):
            self.is_returning = True

        distance = pygame.math.Vector2(self.rect.center).distance_to(self.start_pos) #если дистанция не позволяет возврат
        if distance > self.range:
            self.is_returning = True


        # Возврат к персонажу
        if self.is_returning and self.rect.collidepoint(self.owner.rect.center):
            self.kill()



