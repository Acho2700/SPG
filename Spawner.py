import pygame
from Monsters import Kusaka
import random


class MonsterSpawner:
    def __init__(self, spawn_points, spawn_delay=2000, max_monsters=3):
        self.spawn_points = spawn_points
        self.spawn_delay = spawn_delay
        self.max_monsters = max_monsters
        self.last_spawn_time = pygame.time.get_ticks()
        self.monsters = pygame.sprite.Group()

    def update(self, target, walls, bullets):
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_spawn_time > self.spawn_delay
                and len(self.monsters) < self.max_monsters):
            spawn_pos = random.choice(self.spawn_points)
            print(f"[Спавн] Позиция: {spawn_pos}")

            new_monster = Kusaka()
            new_monster.rect.center = spawn_pos
            new_monster.target = target
            self.monsters.add(new_monster)
            self.last_spawn_time = current_time

        for monster in self.monsters:
            monster.update(target.rect, walls)
            monster.taking_damage(bullets)

