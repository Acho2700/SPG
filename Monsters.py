import pygame, utils
import math
from pygame.math import Vector2
from music import MusicPlayer


class Monster(pygame.sprite.Sprite):
    def __init__(self, frames, speed=2, health=10, damage=10):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.scaled_image = self.frames[self.current_frame]
        self.image = self.scaled_image
        self.rect = self.image.get_rect()

        self.animation_speed = 0.1
        self.animation_timer = 0

        self.sound_radius = 1000
        self.sound = pygame.mixer.Sound('tempelates/sounds/beg-monstra-v-peschere.mp3')
        self.sound.set_volume(0.1)
        self.is_running_sound_playing = False

        self.speed = speed
        self.health = health
        self.damage = damage
        self.target = None  # Цель (игрок)
        self.angle = 0
        self.bullets = pygame.sprite.Group()

    def update(self, player_rect, walls, bullets, waters):

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
            damage=0.3
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
        self.spit_sound = pygame.mixer.Sound('tempelates/sounds/plevok-verblyuda.mp3')
        self.spit_sound.set_volume(0.1)

    def update(self, player_rect, walls, bullets, waters):
        super().update(player_rect, walls, bullets, waters)

        # Стрельба по таймеру
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > 3000:  # 3 секунды
            self.shoot(player_rect.center)
            self.last_shot_time = now

        # Обновление пуль
        self.monster_bullets.update(walls, self.target, waters)

    def shoot(self, target_pos):
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
        for bullet in self.monster_bullets:
            surface.blit(bullet.image, camera.apply(bullet))


class ToxicBullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, speed=4, damage=30):
        super().__init__()
        self.original_image = pygame.image.load('tempelates/monsters/toxic_ball.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (24, 24))
        self.rect = self.image.get_rect(center=start_pos)

        # Параметры движения
        self.direction = Vector2(target_pos) - Vector2(start_pos)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        self.speed = speed
        self.damage = damage

    def update(self, walls, player, waters):
        # Движение
        self.rect.center += self.direction * self.speed

        # Коллизия со стенами
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()


