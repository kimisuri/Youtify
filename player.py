import pyglet.media
from pyglet.media import load
from pyglet.media.player import Player as p
from typing import Union, List


class Player:
    volume: float
    music_list: List[p]
    current_music: p

    def __init__(self):
        self.music_list = []
        self.current_music = None
        self.current_index = -1
        self.is_playing = False
        self._volume = 1

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        for player in self.music_list:
            player.volume = value

    def get_player_from_path(self, path: str) -> p:
        """
        Этот метод возвращает настроенный плеер Pyglet
        :param path: путь до песни
        :return: объект класса Player
        """
        player = load(path).play()
        player.pause()
        player.seek(0)
        player.volume = self._volume

        def on_eos_action(pla: pyglet.media.Player, path: str, my_player: Player):
            print("ПУПУПУ")
            my_player.next()
            pla.queue(load(path))

        @player.event
        def on_player_eos():
            on_eos_action(player, path, self)

        return player

    def queue(self, music_path: Union[str, List[str]]):
        """
        Создаёт или добавляет песни в очередь воспроизведения
        :param music_path: путь/пути до треков
        :return: None
        """
        if not music_path:
            raise ValueError("Список должен быть заполнен!")

        if isinstance(music_path, str):
            self.music_list.append(self.get_player_from_path(music_path))
        else:
            for path in music_path:
                self.music_list.append(self.get_player_from_path(path))

        if self.current_index == -1:
            self.current_index = 0

    def play(self):
        if self.current_index != -1:
            self.current_music = self.music_list[self.current_index]
            self.current_music.play()
            self.is_playing = True


    def next(self):
        if self.current_music:
            self.current_music.seek(0)
            self.current_index = (self.current_index + 1) % len(self.music_list)
            self.continue_after()
            # self.music_list.editItem(self.music_list.item(self.current_index).setSelected())

    def pause(self):
        if self.current_music:
            self.current_music.pause()
            self.is_playing = False

    def previous(self):
        if self.current_music:
            self.current_music.seek(0)
            self.current_index = (self.current_index - 1) % len(self.music_list)
            self.continue_after()

    def continue_after(self):
        """
        Метод обрабатывает переключение песни
        :return:
        """
        if self.is_playing:
            self.current_music.pause()
            self.current_music.seek(0)
            self.play()
        else:
            self.current_music.seek(0)
            self.current_music = self.music_list[self.current_index]

    def remove_track(self, index):
        if self.current_index == index:
            self.previous()
        if self.music_list:
            del self.music_list[index]
        if not self.music_list:
            if self.current_music:
                self.current_music.pause()
            self.current_music = None
            self.current_index = -1

    def get_duration(self) -> float:
        if self.current_music.playing:
            return self.current_music.time / self.current_music.source.duration * 10000
        return 0

    def clear(self):
        if self.current_music:
            self.current_music.pause()
        self.music_list.clear()
        self.current_music = None
        self.current_index = -1
        self.is_playing = False

    def destroy(self):
        self.pause()
        for elem in self.music_list:
            elem.delete()

    def set_music(self, index: int):
        """
        Устанавливает песню по индексу из списка
        :param index: индекс песни в списке
        :return:
        """
        if not index or index not in range(len(self.music_list)):
            print("Индекс должен находиться в пределах длины списка")
            return
        self.current_music.seek(0)
        self.current_index = index
        self.continue_after()


if __name__ == "__main__":
    player = Player()
    player.queue(["music/Radio_Tapok_-_Cusima.mp3", "music/Radio_Tapok_-_Bismarck_71707937.mp3"])
    player.play()
    a = input()
    while a != "stop":
        if a == "n":
            player.next()
        elif a == "p":
            player.previous()
        elif a == "pa":
            player.pause()
        elif a == "pl":
            player.play()
        elif a == 's':
            player.current_music.next_source()
        a = input()
