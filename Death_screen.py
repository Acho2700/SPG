import pygame
import time

def death_screen(screen, skull_image):
    """
    Показывает заставку смерти с черепом и надписью "your dead" на 2 секунды.
    """
    start_time = pygame.time.get_ticks()
    duration = 3000  # миллисекунды (2 секунды)
    font = pygame.font.Font('tempelates/alagard-12px-unicode.ttf', 90)

    death_sound = pygame.mixer.Sound('tempelates/sounds/Death.mp3')

    while pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))  # Черный фон
        death_sound.play()
        # Рисуем череп по центру
        skull_rect = skull_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 70))
        screen.blit(skull_image, skull_rect)

        # Рисуем текст под черепом
        text_surface = font.render("you died", True, (255, 0, 0))  # Красный цвет, например
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 80))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Ограничение до 60 FPS

# В вашем основном игровом цикле замените участок смерти на:

