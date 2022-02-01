from PyQt5.QtWidgets import QDialog, QListWidgetItem
from designs import get_music_dialog


class MusicDialog(QDialog, get_music_dialog.Ui_Dialog):
    def __init__(self, tracks_list: list):
        super().__init__()
        self.setupUi(self)

        for i, item in enumerate(tracks_list):
            list_item = QListWidgetItem()
            list_item.setText(f"{item['artists'][0]['name']} - {item['name']}")
            self.music_list.addItem(list_item)
            # print(item)

        self.ok_pressed = False

        self.ok_btn.clicked.connect(self.ok)
        self.cancel_btn.clicked.connect(self.close)

    def ok(self):
        self.ok_pressed = True
        self.close()

    def get_tracks(self):
        self.exec_()
        return self.ok_pressed, [i.text() for i in self.music_list.selectedItems()]
