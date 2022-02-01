from typing import List

from designs.get_combo_dialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog


class InputCombo(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ok_btn.clicked.connect(self.ok_click)
        self.cancel_btn.clicked.connect(self.close)

        self.clicked = False

    def ok_click(self):
        self.clicked = True
        self.close()

    def get_combo(self, window_name: str, label_text: str, items: List[str]):
        self.combo_box.addItems(items)
        self.setWindowTitle(window_name)
        self.text.setText(label_text)
        self.exec_()
        return self.clicked, self.combo_box.currentText()
