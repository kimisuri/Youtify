from designs.get_text_dialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog


class InputText(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ok_btn.clicked.connect(self.ok_click)
        self.cancel_btn.clicked.connect(self.close)

        self.clicked = False

    def ok_click(self):
        self.clicked = True
        self.close()

    def get_text(self, window_name: str, label_text: str):
        self.text.setText(label_text)
        self.setWindowTitle(window_name)
        self.exec_()
        return self.clicked, self.lineEdit.text()
