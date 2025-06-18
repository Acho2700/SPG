import pygame, os,sys
from paths import *

class Button:
    """Класс кнопки"""
    def __init__(self, rect, text, font, image=None, text_color=(152,106,71), text_color_pressed=(82, 56, 36)):
        """
                Инициализирует кнопку с заданными параметрами.

                Args:
                    rect (tuple): Координаты и размеры кнопки (x, y, width, height).
                    text (str): Текст кнопки.
                    font (pygame.font.Font): Шрифт для текста.
                    image (pygame.Surface, optional): Изображение кнопки. По умолчанию None.
                    text_color (tuple, optional): Цвет текста в обычном состоянии. По умолчанию (152,106,71).
                    text_color_pressed (tuple, optional): Цвет текста при нажатии. По умолчанию (82, 56, 36).
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.image = image  # pygame.Surface с картинкой кнопки или None
        self.text_color = text_color
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)
        self.text_color_pressed = text_color_pressed
        self.pressed = False  # состояние нажатия

        self.sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'sounds/sound_button.mp3'))
        self.sound.set_volume(0.1)

        self.render_text()

    def render_text(self):
        """Перерисовывает текст кнопки с учётом текущего состояния (нажата/не нажата)."""
        color = self.text_color_pressed if self.pressed else self.text_color
        self.rendered_text = self.font.render(self.text, True, color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, surface):
        """
                Отрисовывает кнопку на заданной поверхности.

                Args:
                    surface (pygame.Surface): Поверхность, на которой будет отрисована кнопка.
        """
        if self.image:
            img = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            surface.blit(img, self.rect)
        else:
            pygame.draw.rect(surface, (70, 130, 180), self.rect)
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, mouse_pos):
        """Проверяет, находится ли курсор мыши в пределах кнопки."""
        return self.rect.collidepoint(mouse_pos)

    def set_pressed(self, pressed):
        """
                Устанавливает состояние нажатия кнопки и обновляет её внешний вид.

                Args:
                    pressed (bool): Новое состояние кнопки (True — нажата, False — не нажата).
        """
        self.pressed = pressed
        self.render_text()

def pause_menu(screen, clock, character_select_screen):
    """
        Отображает меню паузы с кнопками управления и обрабатывает пользовательский ввод.

        Args:
            screen (pygame.Surface): Основная поверхность игры для отображения меню.
            clock (pygame.time.Clock): Объект для управления частотой кадров.
            character_select_screen (callable): Функция или объект для перехода к экрану выбора персонажа.

        Returns:
            str: 'resume' для продолжения игры, 'select_screen' для перехода к выбору персонажа.
            Прерывает выполнение программы при выборе выхода.
    """
    pygame.mouse.set_visible(True)
    font = pygame.font.Font(os.path.join(ASSETS_DIR, 'alagard-12px-unicode.ttf'), 32)
    width, height = screen.get_size()

    btn_width, btn_height = 450, 110
    spacing = 20
    start_y = height // 2 - (btn_height * 3 + spacing * 2) // 2

    button_image = pygame.image.load(os.path.join(ASSETS_DIR, 'pauce_button.png')).convert_alpha()

    buttons = [
        Button((width // 2 - btn_width // 2, start_y, btn_width, btn_height), "Вернуться к игре", font, button_image),
        Button((width // 2 - btn_width // 2, start_y + btn_height + spacing, btn_width, btn_height),
               "Меню выбора", font, button_image),
        Button((width // 2 - btn_width // 2, start_y + 2 * (btn_height + spacing), btn_width, btn_height),
               "Выйти из игры", font, button_image),
    ]

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for btn in buttons:
                    btn.set_pressed(btn.is_clicked(mouse_pos))

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.is_clicked(mouse_pos) and btn.pressed:
                        btn.sound.play()
                        if btn == buttons[0]:
                            paused = False
                        elif btn == buttons[1]:
                            paused = False
                            return 'select_screen'
                        elif btn == buttons[2]:
                            pygame.quit()
                            sys.exit()

                    btn.set_pressed(False)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False  # Вернуться к игре по ESC

        screen.fill((30, 30, 30))  # фон меню
        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    return 'resume'

