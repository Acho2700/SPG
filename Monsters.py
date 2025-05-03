import pygame, utils
import math
from pygame.math import Vector2


class Monster(pygame.sprite.Sprite):
    def __init__(self, frames, speed=2, health=10, damage=10):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.scaled_image = self.frames[self.current_frame]
        self.image = self.scaled_image
        self.rect = self.image.get_rect()

        self.speed = speed
        self.health = health
        self.damage = damage
        self.target = None  # Цель (игрок)
        self.angle = 0
        self.bullets = pygame.sprite.Group()

    def update(self, player_rect, walls, bullets):
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

            new_angle = direction.angle_to(pygame.math.Vector2(0, -1))
            if new_angle != self.angle:
                self.angle = new_angle
                self.image = pygame.transform.rotate(self.scaled_image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)

            # Движение
            self.rect.x += direction.x * self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x -= direction.x * self.speed

            self.rect.y += direction.y * self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.y -= direction.y * self.speed

        self.taking_damage(bullets)
        #Смерть
        if self.health <= 0:
            self.kill()

    def taking_damage(self, bullets):
        if pygame.sprite.spritecollide(self, bullets, False):
            damage = bullets.sprites()[0].damage #урон одного патрона
            self.health -= damage


class Kusaka(Monster):
    def __init__(self):
        frame1 = pygame.image.load('tempelates/monsters/kusaka_1.png')
        frame2 = pygame.image.load('tempelates/monsters/kusaka_2.png').convert_alpha()




        frames = [
            pygame.transform.scale(frame1, utils.TILE_SIZE),
            pygame.transform.scale(frame2, utils.TILE_SIZE)
        ]
        super().__init__(
            frames=frames,
            speed=5,
            health=100,
            damage=1
        )


class Pluvaka(Monster):
    def __init__(self):
        frame1 = pygame.image.load('tempelates/monsters/pluvaka_go_1.png').convert_alpha()
        frame2 = pygame.image.load('tempelates/monsters/pluvaka_go_2.png').convert_alpha()

        frames = [
            pygame.transform.scale(frame1, (80, 64)),
            pygame.transform.scale(frame2, (80, 64))
        ]
        super().__init__(
            frames=frames,
            speed=2,
            health=150,
            damage=1
        )

        self.monster_bullets = pygame.sprite.Group()
        self.last_shot_time = 0

    def update(self, player_rect, walls, bullets):
        super().update(player_rect, walls, bullets)

        # Стрельба каждые 3 секунды
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > 3000:  # 3 секунды
            self.shoot(player_rect.center)
            self.last_shot_time = now

        # Обновление пуль
        self.monster_bullets.update(walls, self.target)

    def shoot(self, target_pos):
        bullet = ToxicBullet(
            start_pos=self.rect.center,
            target_pos=target_pos,
            speed=3,
            damage=15
        )
        self.monster_bullets.add(bullet)
        # print(f"Создана пуля в {bullet.rect.center}, всего пуль: {len(self.monster_bullets)}")

    def draw_bullets(self, surface, camera):
        for bullet in self.monster_bullets:
            surface.blit(bullet.image, camera.apply(bullet))


class ToxicBullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, speed=3, damage=30):
        super().__init__()
        # Загрузка изображения
        self.original_image = pygame.image.load('tempelates/monsters/toxic_ball.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (24, 24))
        self.rect = self.image.get_rect(center=start_pos)

        # Параметры движения
        self.direction = Vector2(target_pos) - Vector2(start_pos)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        self.speed = speed
        self.damage = damage

    def update(self, walls, player):
        # Движение
        self.rect.center += self.direction * self.speed

        # Коллизия со стенами
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()
            # return

        # Коллизия с игроком
        # if self.rect.colliderect(player.rect):
        #     player.take_damage(self.damage)
        #     self.kill()

