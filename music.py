import pygame


class MusicPlayer:
    def __init__(self, menu_tracks, game_tracks, volume=0.5):
        """
        Инициализация плеера с двумя плейлистами.

        Args:
            menu_tracks (list): Список путей к трекам для меню.
            game_tracks (list): Список путей к трекам для игры.
            volume (float): Громкость музыки от 0.0 до 1.0.
        """
        self.menu_tracks = menu_tracks
        self.game_tracks = game_tracks
        self.volume = volume

        self.current_playlist = self.menu_tracks
        self.current_track_index = 0

        pygame.mixer.music.set_volume(self.volume)
        self.play_track(self.current_track_index)

    def play_track(self, index):
        """Загружает и запускает трек по индексу из текущего плейлиста."""
        pygame.mixer.music.load(self.current_playlist[index])
        pygame.mixer.music.play()
        print(f"Playing track: {self.current_playlist[index]}")

    def update(self):
        """
        Проверяет, закончился ли трек, и запускает следующий.
        """
        if not pygame.mixer.music.get_busy():
            self.current_track_index = (self.current_track_index + 1) % len(self.current_playlist)
            self.play_track(self.current_track_index)

    def switch_to_menu(self):
        """Переключает плейлист на меню и запускает первый трек."""
        if self.current_playlist != self.menu_tracks:
            self.current_playlist = self.menu_tracks
            self.current_track_index = 0
            self.play_track(self.current_track_index)

    def switch_to_game(self):
        """Переключает плейлист на игру и запускает первый трек."""
        if self.current_playlist != self.game_tracks:
            self.current_playlist = self.game_tracks
            self.current_track_index = 0
            self.play_track(self.current_track_index)

    def set_volume(self, volume):
        """Устанавливает громкость музыки (0.0 - 1.0)."""
        self.volume = max(0.0, min(volume, 1.0))
        pygame.mixer.music.set_volume(self.volume)

