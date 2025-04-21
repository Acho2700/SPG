import pygame
import utils

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

    def update(self, keys_pressed, walls):
        dx = 0
        dy = 0

        if keys_pressed[pygame.K_w]:
            dy = -self.speed
        if keys_pressed[pygame.K_s]:
            dy = self.speed
        if keys_pressed[pygame.K_a]:
            dx = -self.speed
        if keys_pressed[pygame.K_d]:
            dx = self.speed

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
        # Двигаемся по оси X
        self.rect.x += dx
        # Проверяем коллизии по X
        collided_walls = pygame.sprite.spritecollide(self, walls, False)
        for wall in collided_walls:
            if dx > 0:  # Движение вправо
                self.rect.right = wall.rect.left
            elif dx < 0:  # Движение влево
                self.rect.left = wall.rect.right

        # Двигаемся по оси Y
        self.rect.y += dy
        # Проверяем коллизии по Y
        collided_walls = pygame.sprite.spritecollide(self, walls, False)
        for wall in collided_walls:
            if dy > 0:  # Движение вниз
                self.rect.bottom = wall.rect.top
            elif dy < 0:  # Движение вверх
                self.rect.top = wall.rect.bottom


# Дочерние классы персонажей

class Tank(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Tank/game_model_t-Photoroom.png', pos, speed=50)  # Можно задать уникальную скорость


class Engineer(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Engineer/game_model_e.png', pos, speed=3)


class Stormtrooper(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Stormtrooper/game_model_s.png', pos, speed=3)
