import pygame, sys, utils, os
from camera import Camera
from select_sreen import CharacterSelectScreen
from level import Level
from spawner import MonsterSpawner
from monsters import Pluvaka
from characters import Tank, Engineer, Stormtrooper
from popup_screen import death_or_victory_screen
from healthbar import HealthBar
from music import MusicPlayer
from pause_screen import pause_menu
from paths import *


def draw_with_camera(group, surface, camera):
    '''
    Метод отрисовки с учетом камеры
    :param group:
    :param surface:
    :param camera:
    :return:
    '''
    for sprite in group:
        surface.blit(sprite.image, camera.apply(sprite))

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((utils.WIDTH, utils.HEIGHT))           # Игровое окно
    pygame.display.set_caption("p.s.g")
    bg_image = pygame.image.load(os.path.join(ASSETS_DIR, 'background_game.png')).convert()
    background = pygame.transform.scale(bg_image, (utils.WIDTH, utils.HEIGHT))

    death_image = pygame.image.load(os.path.join(ASSETS_DIR, 'screen_dead_scull.png'))
    death_image = pygame.transform.scale(death_image, (300, 300))

    victory_image = pygame.image.load(os.path.join(ASSETS_DIR, 'screen_victory.png'))
    victory_image = pygame.transform.scale(victory_image, (300, 400))

    clock = pygame.time.Clock()
    character_select_screen = CharacterSelectScreen()                       # Объявление экарна выбора персонажа

    menu_tracks = [
        os.path.join(ASSETS_DIR, 'sounds/music/stuart-chatwood-the-hamlet.mp3'),
    ]

    game_tracks = [
        os.path.join(ASSETS_DIR, 'sounds/music/stuart-chatwood-explore-the-ruins.mp3'),
    ]

    music_player = MusicPlayer(menu_tracks, game_tracks, volume=0.1)

    LEVELS = ['lvl_1.txt', 'lvl_2.txt']  # по порядку
    current_level_index = 0

    running = True
    player = None                                                           # Переменная для выбранного персонажа
    game_state = 'character_select'



    while running:                                                          # Основной игровой цикл

        for event in pygame.event.get():                                    # Обработка событий
            if event.type == pygame.QUIT:
                running = False

            if game_state == 'character_select':
                character_select_screen.handle_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Вызов меню паузы
                result = pause_menu(screen, clock, character_select_screen)
                if result == 'select_screen':
                    game_state = 'character_select'
                    player = None
                    spawner.monsters.empty()
                    character_select_screen.reset()  # Сбрасываем выбор персонажа
                    continue

                                                                            # --- Меню выбора персонажа ---
        if game_state == 'character_select':
            character_select_screen.draw(screen)
            music_player.switch_to_menu()

            if character_select_screen.is_ready():
                selected = character_select_screen.characters[character_select_screen.selected_character]
                name = selected['name']
                # -- Инициализация уровня в окне выбора --
                level = Level(open(os.path.join(DATA_DIR, LEVELS[0])))  # Создание уровня
                camera = Camera(level.level_pixel_width, level.level_pixel_height)  # Инициализация камеры

                spawner = MonsterSpawner(  # Объявление спавнера
                    spawn_points=level.spawn_monster,
                    spawn_delay=3000,  # Милисекунды
                    max_monsters=30
                )

                if name == "TANK":                                          # Выбор персонажа
                    player = Tank(pos=level.spawn_point)
                    health_bar = HealthBar(max_health=player.health, image=os.path.join(ASSETS_DIR, 'health/main_model_t.png'))
                elif name == "ENGINEER":
                    player = Engineer(pos=level.spawn_point)
                    health_bar = HealthBar(max_health=player.health, image=os.path.join(ASSETS_DIR, 'health/main_model_e.png'))
                elif name == "STORMTROOPER":
                    player = Stormtrooper(pos=level.spawn_point)
                    health_bar = HealthBar(max_health=player.health, image=os.path.join(ASSETS_DIR, 'health/main_model_s.png'))
                level.set_player(player)

                level.initialized = False
                game_state = 'game'

                                                                            # --- Игра ---
        elif game_state == 'game':
            music_player.switch_to_game()

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

                                                                            # Игровая логика
            if not hasattr(level, 'initialized'):
                player.rect.center = level.spawn_point
                level.initialized = True
                                                                            # Вычисление положения указателя мыши с учетом камеры
            world_mouse_pos = (mouse_pos[0] + camera.offset.x, mouse_pos[1] + camera.offset.y)
            player.handle_shooting(world_mouse_pos, mouse_click, level.walls) # Метод стрельбы


            keys = pygame.key.get_pressed()                                   # Последовательность логических значений, представляющих состояние каждой клавиши на клавиатуре
            player_dead = player.update(keys, level.walls, spawner.monsters, spawner.all_monster_bullets, level.waters, level.portals) # Обновление игрока

            if player.next_level:
                current_level_index += 1
                if current_level_index < len(LEVELS):
                    level = Level(open(os.path.join(DATA_DIR, LEVELS[current_level_index])))
                    camera = Camera(level.level_pixel_width, level.level_pixel_height)
                    player.rect.center = level.spawn_point
                    player.next_level = False  # сбрасываем флаг!

                    spawner = MonsterSpawner(
                        spawn_points=level.spawn_monster,
                        spawn_delay=3000,
                        max_monsters=30
                    )
                    level.set_player(player)
                else:
                    death_or_victory_screen(screen, victory_image, "you victory", (0, 0, 255))
                    player = None
                    spawner.monsters.empty()
                    current_level_index = 0
                    character_select_screen.reset()  # Сбрасываем выбор персонажа
                    game_state = 'character_select'
                    continue

            #Смерть и выход в меню выбора
            if player_dead:
                death_or_victory_screen(screen, death_image, "you died", (255, 0, 0))
                player = None
                spawner.monsters.empty()
                current_level_index = 0
                character_select_screen.reset()  # Сбрасываем выбор персонажа
                game_state = 'character_select'
                continue

            spawner.update(player, level.walls, player.bullets, screen, camera, level.waters)     # Обновление спавнера
            spawner.all_monster_bullets.update(level.walls, player, level.waters)                 #Обновление токсичного шара



            camera.update(player)                                                                 # Обновление камеры
            screen.blit(background, (0, 0))                                                  # Отрисовка заднего фона

            collided_bullets = pygame.sprite.spritecollide(player, spawner.all_monster_bullets, True)
            current_time = pygame.time.get_ticks()

            level.chests.update(player.rect)
            level.potions.update(player.rect)

            for water_tile in level.waters:                               # Анимация воды
                water_tile.animation(current_time)
            for portal_tile in level.portals:                             # Анимация портала
                portal_tile.animation(current_time)
            for bullet in collided_bullets:                               # Попадание в игрока токсичным шаром
                player.health -= bullet.damage
            for chest in level.chests:
                chest.update(player.rect)


            draw_with_camera(level.waters, screen, camera)                # Отрисовка воды
            draw_with_camera(level.floors, screen, camera)                # Отрисовка пола
            draw_with_camera(level.walls, screen, camera)                 # Отрисовка стен
            draw_with_camera(level.portals, screen, camera)               # Отрисовка порталов
            draw_with_camera(spawner.monsters, screen, camera)            # Отрисовка монстров
            draw_with_camera(spawner.all_monster_bullets, screen, camera) # Отрисовка токсичных шаров
            draw_with_camera(player.bullets, screen, camera)              # Отрисовка снарядов игрока
            screen.blit(player.image, camera.apply(player))               # Отрисовка игрока

            for potion in level.potions:
                screen.blit(potion.image, camera.apply(potion))

            health_bar.update(player.health)
            health_bar.draw(screen)


        music_player.update()
        pygame.display.flip()
        clock.tick(60)

