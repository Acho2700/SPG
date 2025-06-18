import pygame, os, sys
import time
from paths import *

def death_or_victory_screen(screen, image, text, color=(255, 0, 0)):
    """Показывает заставку проигрыша или победы/"""
    start_time = pygame.time.get_ticks()
    duration = 3000  # миллисекунды (2 секунды)
    font = pygame.font.Font(os.path.join(ASSETS_DIR, 'alagard-12px-unicode.ttf'), 90)

    death_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds/Death.mp3'))

    while pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        screen.fill((0, 0, 0))  # Черный фон
        death_sound.play()
        # Рисуем череп по центру
        skull_rect = image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 70))
        screen.blit(image, skull_rect)

        # Рисуем текст под черепом
        text_surface = font.render(text, True, color)  # Красный цвет, например
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 80))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Ограничение до 60 FPS






