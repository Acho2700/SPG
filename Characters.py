import pygame
import utils
from Projectile import RifleBullet, FireBullet, Axe

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, pos=(0, 0), speed=5, health=100):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.original_image, utils.TILE_SIZE)
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)
        self.angle = 0  # Храним последний угол поворота
        self.health = health

        #для стрельбы
        self.bullets = pygame.sprite.Group()

    def update(self, keys_pressed, walls, monsters, monster_bullets):
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

        self.taking_damage(monsters, monster_bullets)
        print(self.health)
        if self.health <= 0:
            self.kill()
            return True  # Возвращаем True при смерти
        return False




    def move(self, dx, dy, walls):
        # Сохраняем старую позицию

        # Пробуем двигаться по X
        self.rect.x += dx
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= dx

        # Пробуем двигаться по Y
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y -= dy

    def taking_damage(self, monsters, monster_bullets):
        # Получение дамага от монстров
        if pygame.sprite.spritecollide(self, monsters, False):
            damage = monsters.sprites()[0].damage  # урон монстра
            self.health -= damage
        collided_bullets = pygame.sprite.spritecollide(self, monster_bullets, True)
        for bullet in collided_bullets:
            self.health -= bullet.damage


# Дочерние классы персонажей

class Tank(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Tank/game_model_t_axe.png', pos, speed=5, health=100)
        self.image_with_axe = pygame.image.load('tempelates/Tank/game_model_t-Photoroom.png').convert_alpha()
        self.image_with_axe = pygame.transform.scale(self.image_with_axe, self.rect.size)
        self.original_image = self.image

        self.throw_cooldown = 0
        self.throw_delay = 60
        self.bullets = pygame.sprite.Group()
        self.health = 200

    def handle_shooting(self, target_pos, mouse_click, walls):
        # Удаляем мертвые пули
        self.bullets = pygame.sprite.Group([b for b in self.bullets if b.alive()])

        # Определяем состояние топора
        has_axe = len(self.bullets) > 0

        # Переключаем изображение
        if has_axe:
            self.image = self.image_with_axe
        else:
            self.image = self.original_image

        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

        # Бросок при условии
        if mouse_click[0] and len(self.bullets) == 0 and self.throw_cooldown <= 0:
            new_axe = Axe(owner=self, target_pos=target_pos)
            self.bullets.add(new_axe)
            self.throw_cooldown = self.throw_delay

        # Кулдаун
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

        self.bullets.update(walls)


class Engineer(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Engineer/game_model_e.png', pos, speed=5, health=100)
        self.burst_count = 0  # Текущий счётчик очереди
        self.burst_size = 30  # Размер очереди
        self.burst_delay = 2 # Задержка между пулями
        self.shoot_cooldown = 0  # Таймер задержки
        self.bullets = pygame.sprite.Group()
        self.health = 100


    def handle_shooting(self, target_pos, mouse_click, walls):
        """
        Обработка стрельбы по мышке
        :param target_pos: позиция курсора
        :param mouse_click: состояние кнопки мыши
        :param walls: группа стен для коллизий
        """
        if mouse_click[0] and self.burst_count == 0 and self.shoot_cooldown <= 0:
            self.burst_count = self.burst_size
            self.shoot_cooldown = 60

        if self.burst_count > 0 and self.shoot_cooldown <= 0:
            bullet = FireBullet(
                start_pos=self.rect.center,
                target_pos=target_pos,
            )
            self.bullets.add(bullet)
            self.burst_count -= 1
            self.shoot_cooldown = self.burst_delay

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.bullets.update(walls)


class Stormtrooper(Character):
    def __init__(self, pos=(0, 0)):
        super().__init__('tempelates/Stormtrooper/game_model_s.png', pos, speed=5, health=100)
        self.burst_count = 0  # Текущий счётчик очереди
        self.burst_size = 3  # Размер очереди
        self.burst_delay = 7  # Задержка между пулями
        self.shoot_cooldown = 0  # Таймер задержки
        self.bullets = pygame.sprite.Group()
        self.health = 150


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

