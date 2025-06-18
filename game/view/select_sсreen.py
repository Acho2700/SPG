import pygame
import os
from game.models import utils
from game.controller.paths import *



class CharacterSelectScreen:
    """Класс экрана выбора персонажа с отображением доступных персонажей, их оружия и обработкой выбора."""
    def __init__(self):
        """Загружает изображения персонажей и оружия, масштабирует их, инициализирует звуки и прямоугольники для кликов."""
        STORMTROOPER = pygame.image.load(os.path.join(ASSETS_DIR,'Stormtrooper/main_model_s.png'))
        ENGINEER = pygame.image.load(os.path.join(ASSETS_DIR,'Engineer/main_model_e.png'))
        TANK = pygame.image.load(os.path.join(ASSETS_DIR,'Tank/main_model_t.png'))

        self.characters = [
            {"name": "STORMTROOPER", "image": pygame.transform.scale(STORMTROOPER, (128 * 2, 200 * 2))},
            {"name": "ENGINEER", "image": pygame.transform.scale(ENGINEER, (128 * 2, 200 * 2))},
            {"name": "TANK", "image": pygame.transform.scale(TANK, (128 * 2, 200 * 2))}
        ]

        GUN_STORMTROOPER = pygame.image.load(os.path.join(ASSETS_DIR,'Stormtrooper/ak-47.png'))
        GUN_ENGINEER = pygame.image.load(os.path.join(ASSETS_DIR,'Engineer/flamethrower.png'))
        GUN_TANK = pygame.image.load(os.path.join(ASSETS_DIR,'Tank/axe4.png'))

        self.guns = [
            {"text": "Описание оружия", "image": pygame.transform.scale(GUN_STORMTROOPER, (128 * 2, 100 * 2))},
            {"text": "Описание оружия", "image": pygame.transform.scale(GUN_ENGINEER, (128 * 2, 100 * 2))},
            {"text": "Описание оружия", "image": pygame.transform.scale(GUN_TANK, (128 * 2, 100 * 2))}
        ]

        self.selected_character = None

        self.sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR,'sounds/sound_button.mp3'))
        self.sound.set_volume(0.1)

        # Сохраняем координаты и размеры для каждого персонажа
        self.char_rects = []
        for i, character in enumerate(self.characters):
            x = 200 + i * 450
            y = 100
            w = character["image"].get_width()
            h = character["image"].get_height()
            self.char_rects.append(pygame.Rect(x, y, w, h))

    def draw(self, screen):
        """
                Отрисовывает фон, заголовок, персонажей, их оружие и имена на экране.

                Args:
                    screen (pygame.Surface): Поверхность для отрисовки.
        """
        # Задний фон
        bg_image = pygame.image.load(os.path.join(ASSETS_DIR,'background_select_characters.jpg')).convert()
        background = pygame.transform.scale(bg_image, (utils.WIDTH, utils.HEIGHT))
        screen.blit(background, (0, 0))

        # Текст на экране
        font = pygame.font.Font(os.path.join(ASSETS_DIR,'alagard-12px-unicode.ttf'), 64)
        text = font.render("SELECT CHARACTERS", True, (250, 250, 250))
        screen.blit(text, (utils.WIDTH // 2 - 350, 0))

        # Отрисовка изображений персонажей
        for i, character in enumerate(self.characters):
            rect = self.char_rects[i]
            screen.blit(character["image"], (rect.x, rect.y))
            pygame.draw.rect(screen, '#d3cece', rect, 7)

        # Отрисовка изображений оружия
        for i, gun in enumerate(self.guns):
            x = 200 + i * 450
            y = 550
            screen.blit(gun["image"], (x, y))
            rect = pygame.Rect(x, y, gun["image"].get_width(), gun["image"].get_height())
            pygame.draw.rect(screen, '#515151', rect, 7)

        # Отрисовка имен персонажей
        font_character = pygame.font.Font(os.path.join(ASSETS_DIR,'alagard-12px-unicode.ttf'), 30)
        text_s = font_character.render("STORMTROOPER", True, (250, 250, 250))
        screen.blit(text_s, (200 + 0 * 600, 500))
        text_e = font_character.render("ENGINEER", True, (250, 250, 250))
        screen.blit(text_e, (100 + 1 * 600, 500))
        text_t = font_character.render("TANK", True, (250, 250, 250))
        screen.blit(text_t, (70 + 2 * 560, 500))

    def handle_event(self, event):
        """
                Обрабатывает события мыши для выбора персонажа.

                Args:
                    event (pygame.event.Event): Событие Pygame.
        """
        if event.type == pygame.MOUSEBUTTONUP:
            for i, rect in enumerate(self.char_rects):
                if rect.collidepoint(event.pos):
                    self.sound.play()
                    self.selected_character = i

    def is_ready(self):
        """Проверяет, выбран ли персонаж."""
        return self.selected_character is not None

    def reset(self):
        """Сбрасывает выбор персонажа."""
        self.selected_character = None

