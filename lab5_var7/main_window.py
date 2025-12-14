import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PyQt5.QtCore import Qt

from iterator import ImageIterator


class ImageViewer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle("Просмотр изображений")
        self.setGeometry(550, 200, 800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        buttons = QHBoxLayout()
        btn_folder = QPushButton("Выбрать папку")
        buttons.addWidget(btn_folder)
        
        btn_csv = QPushButton("Выбрать CSV")
        buttons.addWidget(btn_csv)
        
        buttons.addStretch()
        layout.addLayout(buttons)

        self.info = QLabel("Выберите папку или CSV")
        self.info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info)

        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMinimumSize(600, 500)
        self.image.setText("Изображение")
        self.image.setStyleSheet("border: 5px solid gray; background: #f0f0f0;")
        layout.addWidget(self.image)

        nav = QHBoxLayout()
        self.btn_prev = QPushButton("Назад")
        self.btn_prev.setEnabled(False)
        nav.addWidget(self.btn_prev)
        
        self.btn_next = QPushButton("Вперед")
        self.btn_next.setEnabled(False)
        nav.addWidget(self.btn_next)
        
        nav.addStretch()
        layout.addLayout(nav)


def main() -> None:
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()