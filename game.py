import pygame
import sys

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

    running = True
    clock = pygame.time.Clock()

    character_select_screen = CharacterSelectScreen()
    game_started = False

    player = None  # Переменная для выбранного персонажа
    level = None   # Переменная для уровня

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_started:
                character_select_screen.handle_event(event)

        if not game_started:
            character_select_screen.draw(screen)
            if character_select_screen.is_ready():
                game_started = True
                selected = character_select_screen.characters[character_select_screen.selected_character]
                print(selected)
                name = selected['name']
                print("Игра началась с персонажем:", name)

                start_pos = (utils.WIDTH // 2, utils.HEIGHT // 2)

                # Создаём объект выбранного персонажа
                if name == "TANK":
                    player = Tank(pos=start_pos)
                elif name == "ENGINEER":
                    player = Engineer(pos=start_pos)
                elif name == "STORMTROOPER":
                    player = Stormtrooper(pos=start_pos)
                else:
                    player = Tank(pos=start_pos)

                # Создаём уровень (пример с map2)
                level = Level(map1)

        else:
            screen.blit(background, (0, 0))
            level.draw(screen)

            keys = pygame.key.get_pressed()
            player.update(keys, level.walls)
            screen.blit(player.image, player.rect)  # Рисуем игрока

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
