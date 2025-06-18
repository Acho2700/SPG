from PIL import Image
from paths import *
import os
# Сопоставление цвета (R,G,B) к символу карты

COLOR_TO_CHAR = {
    (255, 0, 0): '#',    # Красный - стена
    (0, 0, 0): '.',      # Чёрный - пол
    (0, 0, 255): '-',    # Синий - вода
    (0, 255, 0): '$',    # Зелёный - спавн игрока
    (255, 255, 0): '*',  # Жёлтый - спавнеры монстров
    (255, 255, 255): ' ',# Белый - пустоты
}
def image_to_map_txt(image_path, output_txt_path):
    """
            Метод считывет пиксели из изображения в формате PNG и создает файл формата TXT с заменной пикселей на символы
            для генерации карты

            Args:
                    image_path: PNG изображение.
                    output_txt_path: TXT файл для сохранения карты.
    """
    img = Image.open(image_path).convert('RGB')
    width, height = img.size

    map_rows = []
    for y in range(height):
        row_chars = []
        for x in range(width):
            pixel = img.getpixel((x, y))
            char = COLOR_TO_CHAR.get(pixel, '.')  # По умолчанию пол
            row_chars.append(char)
        map_rows.append(''.join(row_chars))

    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for row in map_rows:
            f.write(row + '\n')

    print(f"Карта успешно сохранена в {output_txt_path}")


img = input('Введите название файла с изображением карты: ')
txt = input('Введите название для созданного файла: ')
image_to_map_txt(os.path.join(DATA_DIR, img), os.path.join(DATA_DIR, txt))
