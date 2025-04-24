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
        super().__init__('tempelates/Engineer/game_model_e.png', pos, speed=3)


class Stormtrooper(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Stormtrooper/game_model_s.png', pos, speed=3)
