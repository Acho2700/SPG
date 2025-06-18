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