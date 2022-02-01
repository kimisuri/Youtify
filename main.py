import os
import sys
import time
from threading import Thread

import pyglet.app
import spotipy
import yt_dlp
from PyQt5.QtWidgets import QMainWindow, QApplication
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from utils.text_dialog import InputText
from utils.combo_dialog import InputCombo

from designs import player_gui
from json_reader import Json
from music_dialog import MusicDialog
from passwords import *
from player import *
import tkinter as tk
import tkinter.filedialog as fd

updating = True


class MainWindow(QMainWindow, player_gui.Ui_MainWindow):
    current_playlist: Json

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setFixedSize(1000, 800)
        self.setWindowTitle("YouTify")

        # Инициализация плеера
        self.player = Player()
        self.next_btn.clicked.connect(self.next_action)
        self.previous_btn.clicked.connect(self.previous_action)
        self.pause_btn.clicked.connect(self.player.pause)
        self.play_btn.clicked.connect(self.play_action)

        # Подгрузка треков
        self.playlists = Json("playlists.json", {"playlists": ["default"]})
        self.config = Json("config.json", {"last_playlist": "default"})
        self.load_tracks(self.config['last_playlist'])

        self.get_track.clicked.connect(self.get_track_action)
        self.add_from_youtube.triggered.connect(self.add_from_youtube_action)
        self.delete_track.triggered.connect(self.remove_track)
        self.change_playlist.triggered.connect(self.choose_playlist)
        self.delete_playlist.triggered.connect(self.delete_playlist_action)
        self.add_from_spoty.triggered.connect(self.get_track_action)
        self.create_file.triggered.connect(self.new_playlist)
        self.add_from_disk_3.triggered.connect(self.add_from_disk_action)

        self.update_music_list()
    def next_action(self):
        i = (self.player.current_index + 1) % len(self.player.music_list)
        self.music_list.setCurrentRow(i)
        self.player.next()

    def previous_action(self):
        i = (self.player.current_index - 1) % len(self.player.music_list)
        self.music_list.setCurrentRow(i)
        self.player.previous()

    def play_action(self):
        if self.player.current_index != -1:
            self.player.pause()
            self.player.current_index = int(self.music_list.currentRow())
            self.music_list.setCurrentRow(self.player.current_index)
            self.player.play()
        else:
            self.player.play()

    def get_track_action(self):
        ok, text = InputText().get_text('Поиск песни', 'Введите название песни или исполнителя:')
        if ok:
            results = sp.search(text, limit=20)
            ok, selected_items = MusicDialog(results["tracks"]["items"]).get_tracks()
            if ok:
                for i in selected_items:
                    thread = Thread(target=download_track, args=(i, self))
                    # Загрузка треков происходит параллельно работе всего проекта
                    thread.start()

    def load_tracks(self, name):
        self.config["last_playlist"] = name
        self.current_playlist = Json(f"playlists/{name}.json", {"tracks": {}})
        self.config.commit()
        self.player.clear()
        self.update_music_list()

        # Проверка на целостность треков
        temp = {"tracks": {}}
        for i, elem in enumerate(self.current_playlist["tracks"].items()):
            if os.path.exists(elem[1]):
                temp["tracks"][elem[0]] = elem[1]
        self.current_playlist.set(temp)
        self.current_playlist.commit()

        # Подгрузка в плеер
        if self.current_playlist["tracks"]:
            self.player.queue(self.current_playlist["tracks"].values())

    def update_music_list(self):
        self.music_list.clear()
        for elem in self.current_playlist["tracks"].keys():
            self.music_list.addItem(elem)

    def closeEvent(self, a0) -> None:
        global updating, sp

        updating = False
        self.player.destroy()
        pyglet.app.exit()
        del sp
        super().close()
        exit(0)

    def add_from_youtube_action(self):
        ok, name = InputText().get_text('Поиск песни', 'Введите имя песни:')
        if ok:
            ok, link = InputText().get_text('Поиск песни', 'Введите ссылку на ролик:')
            if ok:
                thread = Thread(target=download_from_youtube, args=(name, link, self))
                thread.start()

    def remove_track(self):
        current_track = self.music_list.currentItem()
        if current_track:
            del self.current_playlist["tracks"][current_track.text()]
            self.current_playlist.commit()
            self.player.remove_track(int(self.music_list.currentRow()))
            self.update_music_list()

    def new_playlist(self):
        ok, name = InputText().get_text("Создание плейлиста", "Введите имя плейлиста:")
        if ok:
            self.playlists["playlists"].append(name)
            self.playlists.commit()
            self.load_tracks(name)

    def choose_playlist(self):
        ok, name = InputCombo().get_combo("Выбор плейлиста", "Выберите плейлист:", self.playlists["playlists"])
        if ok:
            self.load_tracks(name)

    def delete_playlist_action(self):
        ok, name = InputCombo().get_combo("Выбор плейлиста", "Выберите плейлист:", self.playlists["playlists"])
        if ok:
            if name == "default":
                self.statusbar.showMessage("Нельзя удалять дефолтный плейлист")
            else:
                if name == self.config["last_playlist"]:
                    self.load_tracks("default")
                self.playlists["playlists"].remove(name)
                self.playlists.commit()
                os.remove(f"playlists/{name}.json")
                self.statusbar.showMessage("Плейлист удалён")

    def add_from_disk_action(self):
        ok, text = InputText().get_text("Название песни", "Введите название песни, которую хотите сохранить:")
        if ok:
            wind = tk.Tk()
            types = (("Audio", "*.mp3 *.wav"),)
            filename = fd.askopenfilename(title="Выбор файла", filetypes=types)
            if filename:
                self.current_playlist["tracks"][text] = filename
                self.current_playlist.commit()
                self.load_tracks(self.config["last_playlist"])
            wind.destroy()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def update_duration(window: MainWindow):
    while updating:
        if window.player.current_music and window.player.is_playing:
            window.music_duration.setValue(int(window.player.get_duration()))
        time.sleep(0.5)


def download_track(name: str, window: MainWindow):
    search = VideosSearch(name, limit=1, language="ru", region="RU").result()["result"][0]["link"]
    download_from_youtube(name, search, window)


def download_from_youtube(name, link, window):
    path = f"music/{name}.mp3"
    if os.path.exists(path):
        window.statusbar.showMessage("There is a file with the same name in folder music")
    else:
        options = {'format': 'bestaudio/best',
                   'postprocessors': [
                       {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192', }],
                   'outtmpl': path}
        with yt_dlp.YoutubeDL(options) as youtube:
            youtube.download([link])
    window.current_playlist["tracks"][name] = path
    window.current_playlist.commit()
    window.statusbar.showMessage(f"{name} был добавлен в папку music")
    window.update_music_list()
    window.player.queue(path)


if __name__ == "__main__":
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=APP_CLIENT_ID,
                                                               client_secret=APP_CLIENT_SECRET))

    app = QApplication(sys.argv)
    ex = MainWindow()
    thr = Thread(target=update_duration, args=(ex,))
    thr.start()
    sys.excepthook = except_hook
    ex.show()
    pyglet.app.run()
    sys.exit(app.exec_())
