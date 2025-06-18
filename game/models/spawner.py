import pygame
from game.models.monsters import Kusaka, Pluvaka
import random


class MonsterSpawner:
    """Класс для управления появлением монстров в игре."""
    def __init__(self, spawn_points, spawn_delay=2000, max_monsters=3):
        """
                Инициализирует спавнер с заданными точками появления и параметрами.

                Args:
                    spawn_points (list): Список координат (x, y) для появления монстров.
                    spawn_delay (int, optional): Задержка между появлениями в мс. По умолчанию 2000.
                    max_monsters (int, optional): Максимальное число монстров. По умолчанию 3.
        """
        self.spawn_points = spawn_points
        self.spawn_delay = spawn_delay
        self.max_monsters = max_monsters
        self.last_spawn_time = pygame.time.get_ticks()
        self.monsters = pygame.sprite.Group()
        self.all_monster_bullets = pygame.sprite.Group()

    def update(self, target, walls, bullets, screen, camera, waters):
        """
                Обновляет состояние спавнера: при необходимости создаёт новых монстров,
                обновляет их и их пули.

                Args:
                    target: Цель монстров (обычно игрок).
                    walls (pygame.sprite.Group): Группа стен для проверки коллизий.
                    bullets (pygame.sprite.Group): Группа пуль игрока.
                    screen (pygame.Surface): Поверхность для отрисовки.
                    camera: Объект камеры для преобразования координат.
                    waters (pygame.sprite.Group): Группа водных препятствий.
        """
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_spawn_time > self.spawn_delay
                and len(self.monsters) < self.max_monsters):
            spawn_pos = random.choice(self.spawn_points)
            new_monster = random.choice([Kusaka(), Pluvaka()])
            new_monster.rect.center = spawn_pos
            new_monster.target = target
            self.monsters.add(new_monster)
            self.last_spawn_time = current_time

        for monster in self.monsters:
            monster.update(target.rect, walls, bullets, waters)
            if isinstance(monster, Pluvaka):
                monster.draw_bullets(screen, camera)  # Камеру передавайте при необходимости

                self.all_monster_bullets.add(monster.monster_bullets)

                # Обновляем все пули монстров
            self.all_monster_bullets.update(walls, target, waters)


