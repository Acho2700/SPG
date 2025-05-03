import pygame
import sys
from Camera import Camera
from select import select

import utils
from Select_sreen import CharacterSelectScreen
from level import Level
from level_map import *
from Spawner import MonsterSpawner
from Monsters import Pluvaka

# Импортируем классы персонажей
from Characters import Tank, Engineer, Stormtrooper

def draw_with_camera(group, surface, camera):
    for sprite in group:
        surface.blit(sprite.image, camera.apply(sprite))

def main():
    pygame.init()

    screen = pygame.display.set_mode((utils.WIDTH, utils.HEIGHT))
    pygame.display.set_caption("p.s.g")
    bg_image = pygame.image.load('tempelates/background_game.png').convert()
    background = pygame.transform.scale(bg_image, (utils.WIDTH, utils.HEIGHT))
    level = Level(map2)  # Создаём уровень
    camera = Camera(level.level_pixel_width, level.level_pixel_height)  # Инициализируем камеру после создания уровня
    running = True
    clock = pygame.time.Clock()
    character_select_screen = CharacterSelectScreen()  # объявление экарна выбора персонажа
    game_started = False

    player = None  # Переменная для выбранного персонажа

    spawner = MonsterSpawner(
        spawn_points=level.spawn_monster,
        spawn_delay=2000, #Милисекунды
        max_monsters=1
    )

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_started:
                character_select_screen.handle_event(event)

        # --- Меню ---
        if not game_started:
            character_select_screen.draw(screen)

            if character_select_screen.is_ready():
                selected = character_select_screen.characters[character_select_screen.selected_character]
                name = selected['name']

                if name == "TANK":
                    player = Tank(pos=level.spawn_point)
                elif name == "ENGINEER":
                    player = Engineer(pos=level.spawn_point)
                elif name == "STORMTROOPER":
                    player = Stormtrooper(pos=level.spawn_point)

                game_started = True
                level.initialized = False

        # --- Игра ---
        else:


            # Игровая логика
            if not hasattr(level, 'initialized'):
                player.rect.center = level.spawn_point
                level.initialized = True

            world_mouse_pos = (mouse_pos[0] + camera.offset.x, mouse_pos[1] + camera.offset.y)
            player.handle_shooting(world_mouse_pos, mouse_click, level.walls)

            keys = pygame.key.get_pressed()
            player_dead = player.update(keys, level.walls, spawner.monsters, spawner.all_monster_bullets)
            #Смерть и выход в меню выбора
            if player_dead:
                game_started = False
                player = None
                spawner.monsters.empty()
                character_select_screen.reset()  # Сбрасываем выбор персонажа
                continue

            spawner.update(player, level.walls, player.bullets, screen, camera)
            spawner.all_monster_bullets.update(level.walls, player)

            # Отрисовка
            camera.update(player)
            screen.blit(background, (0, 0))

            collided_bullets = pygame.sprite.spritecollide(player, spawner.all_monster_bullets, True)
            for bullet in collided_bullets:
                player.health -= bullet.damage

            for floor in level.floors:
                screen.blit(floor.image, camera.apply(floor))
            for wall in level.walls:
                screen.blit(wall.image, camera.apply(wall))

            draw_with_camera(spawner.monsters, screen, camera)

            for bullet in spawner.all_monster_bullets:
                print('bullet')
                screen.blit(bullet.image, camera.apply(bullet))

            for bullet in player.bullets:
                screen.blit(bullet.image, camera.apply(bullet))

            screen.blit(player.image, camera.apply(player))

        pygame.display.flip()
        clock.tick(60)

