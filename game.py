import pygame, sys, utils
from Camera import Camera
from Select_sreen import CharacterSelectScreen
from level import Level
from Spawner import MonsterSpawner
from Monsters import Pluvaka
from Characters import Tank, Engineer, Stormtrooper
from Death_screen import death_screen
from healthbar import HealthBar
from music import MusicPlayer

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
    bg_image = pygame.image.load('tempelates/background_game.png').convert()
    background = pygame.transform.scale(bg_image, (utils.WIDTH, utils.HEIGHT))

    level = Level(open(r'map.txt'))                                         # Создание уровня
    camera = Camera(level.level_pixel_width, level.level_pixel_height)      # Инициализация камеры

    skull_image = pygame.image.load('tempelates/screen_dead_scull.png')
    skull_image = pygame.transform.scale(skull_image, (300, 300))

    clock = pygame.time.Clock()
    character_select_screen = CharacterSelectScreen()                       # Объявление экарна выбора персонажа

    menu_tracks = [
        # 'tempelates/sounds/music/stuart-chatwood-explore-the-ruins.mp3',
        'tempelates/sounds/music/stuart-chatwood-the-hamlet.mp3',
    ]

    game_tracks = [
        'tempelates/sounds/music/stuart-chatwood-explore-the-ruins.mp3',
        # 'tempelates/sounds/music/stuart-chatwood-the-hamlet.mp3',
    ]

    music_player = MusicPlayer(menu_tracks, game_tracks, volume=0.1)

    game_started = False
    running = True
    player = None                                                           # Переменная для выбранного персонажа

    spawner = MonsterSpawner(                                               # Объявление спавнера
        spawn_points=level.spawn_monster,
        spawn_delay=2000, # Милисекунды
        max_monsters=1
    )

    while running:                                                          # Основной игровой цикл

        for event in pygame.event.get():                                    # Обработка событий
            if event.type == pygame.QUIT:
                running = False

            if not game_started:
                character_select_screen.handle_event(event)

                                                                            # --- Меню ---
        if not game_started:
            character_select_screen.draw(screen)
            music_player.switch_to_menu()

            if character_select_screen.is_ready():
                selected = character_select_screen.characters[character_select_screen.selected_character]
                name = selected['name']

                if name == "TANK":                                          # Выбор персонажа
                    player = Tank(pos=level.spawn_point)
                    health_bar = HealthBar(max_health=player.health, image='tempelates/health/main_model_t.png')
                elif name == "ENGINEER":
                    player = Engineer(pos=level.spawn_point)
                    health_bar = HealthBar(max_health=player.health, image='tempelates/health/main_model_e.png')
                elif name == "STORMTROOPER":
                    player = Stormtrooper(pos=level.spawn_point)
                    health_bar = HealthBar(max_health=player.health, image='tempelates/health/main_model_s.png')

                game_started = True
                level.initialized = False

                                                                            # --- Игра ---
        else:
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
            player_dead = player.update(keys, level.walls, spawner.monsters, spawner.all_monster_bullets, level.waters) # Обновление игрока

            #Смерть и выход в меню выбора
            if player_dead:
                death_screen(screen, skull_image)
                game_started = False
                player = None
                spawner.monsters.empty()
                character_select_screen.reset()  # Сбрасываем выбор персонажа
                continue

            spawner.update(player, level.walls, player.bullets, screen, camera, level.waters)     # Обновление спавнера
            spawner.all_monster_bullets.update(level.walls, player, level.waters)                 #Обновление токсичного шара


            camera.update(player)                                                                 # Обновление камеры
            screen.blit(background, (0, 0))                                                  # Отрисовка заднего фона

            collided_bullets = pygame.sprite.spritecollide(player, spawner.all_monster_bullets, True)
            current_time = pygame.time.get_ticks()

            for water_tile in level.waters:                               # Анимация воды
                water_tile.water_animation(current_time)
            for bullet in collided_bullets:                               # Попадание в игрока токсичным шаром
                player.health -= bullet.damage

            draw_with_camera(level.waters, screen, camera)                # Отрисовка воды
            draw_with_camera(level.floors, screen, camera)                # Отрисовка пола
            draw_with_camera(level.walls, screen, camera)                 # Отрисовка стен
            draw_with_camera(spawner.monsters, screen, camera)            # Отрисовка монстров
            draw_with_camera(spawner.all_monster_bullets, screen, camera) # Отрисовка токсичных шаров
            draw_with_camera(player.bullets, screen, camera)              # Отрисовка снарядов игрока
            screen.blit(player.image, camera.apply(player))               # Отрисовка игрока

            health_bar.update(player.health)
            health_bar.draw(screen)

        music_player.update()
        pygame.display.flip()
        clock.tick(60)

