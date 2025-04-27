import pygame
import sys
from Camera import Camera
from select import select

import utils
from Select_sreen import CharacterSelectScreen
from level import Level
from level_map import *

# Импортируем классы персонажей
from Characters import Tank, Engineer, Stormtrooper

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

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_started:
                character_select_screen.handle_event(event)

        if not game_started: #МЕНЮ ВЫБОРА ПЕРСОНАЖА
            character_select_screen.draw(screen)

            if character_select_screen.is_ready():
                game_started = True
                selected = character_select_screen.characters[character_select_screen.selected_character]
                print(selected)
                name = selected['name']
                print("Игра началась с персонажем:", name)

                # Создаём объект выбранного персонажа
                if name == "TANK":
                    player = Tank(pos=level.spawn_point)
                elif name == "ENGINEER":
                    player = Engineer(pos=level.spawn_point)
                elif name == "STORMTROOPER":
                    player = Stormtrooper(pos=level.spawn_point)

                pygame.event.clear()
                pygame.mouse.get_rel()


        else:  # УРОВЕНЬ ИГРЫ

            mouse_click = pygame.mouse.get_pressed()
            if not hasattr(level, 'initialized'):
                # Обновляем позицию персонажа
                player.rect.center = level.spawn_point
                level.initialized = True

            # Преобразуем экранные координаты в мировые
            world_mouse_pos = (
                mouse_pos[0] + camera.offset.x,
                mouse_pos[1] + camera.offset.y
            )

            # if isinstance(player, Stormtrooper):
            player.handle_shooting(world_mouse_pos, mouse_click, level.walls)
            keys = pygame.key.get_pressed()
            player.update(keys, level.walls)

            camera.update(player)
            screen.blit(background, (0, 0))
            # Рисуем уровень с учётом камеры
            for wall in level.walls:
                screen.blit(wall.image, camera.apply(wall))
            for floor in level.floors:
                screen.blit(floor.image, camera.apply(floor))
            for bullet in player.bullets:
                screen.blit(bullet.image, camera.apply(bullet))
            screen.blit(player.image, camera.apply(player))


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
