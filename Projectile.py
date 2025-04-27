import pygame, utils


class RifleBullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, speed=15, damage=5):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.image.fill(pygame.Color('yellow'))
        self.rect = self.image.get_rect(center=start_pos)

        # Рассчитываем направление к цели
        direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(start_pos)
        if direction.length() > 0:
            direction = direction.normalize()

        # Поворачиваем спрайт
        angle = direction.angle_to(pygame.math.Vector2(1, 0))  # Угол относительно горизонта
        self.image = pygame.transform.rotate(self.image, -angle)  # Отрицательный угол для корректного поворота

        self.rect = self.image.get_rect(center=start_pos)

        self.velocity = direction * speed
        self.damage = damage

    def update(self, walls):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Уничтожаем при столкновении со стенами
        if pygame.sprite.spritecollide(self, walls, False):
            self.kill()


