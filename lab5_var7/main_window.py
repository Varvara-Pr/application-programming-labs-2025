import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtCore import Qt

from iterator import ImageIterator


class ImageViewer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.iterator = None
        self.current_path: str = ""
        self.current_index: int = 0
        self.setup_ui()
    
    def setup_ui(self) -> None:
        self.setWindowTitle("Просмотр изображений")
        self.setGeometry(550, 200, 800, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        buttons = QHBoxLayout()
        btn_folder = QPushButton("Выбрать папку")
        btn_folder.clicked.connect(self.select_folder)
        buttons.addWidget(btn_folder)
        
        btn_csv = QPushButton("Выбрать CSV")
        btn_csv.clicked.connect(self.select_csv)
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
        self.image.setStyleSheet("border: 5px solid #b0c4de; background: #D1EAF3;")
        layout.addWidget(self.image)
        
        nav = QHBoxLayout()
        self.btn_prev = QPushButton("Назад")
        self.btn_prev.clicked.connect(self.prev)
        self.btn_prev.setEnabled(False)
        nav.addWidget(self.btn_prev)
        
        self.btn_next = QPushButton("Вперед")
        self.btn_next.clicked.connect(self.next)
        self.btn_next.setEnabled(False)
        nav.addWidget(self.btn_next)
        
        nav.addStretch()
        layout.addLayout(nav)
    
    def select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.load(folder)
    
    def select_csv(self) -> None:
        csv_file, _ = QFileDialog.getOpenFileName(self, "Выберите CSV", "", "CSV (*.csv)")
        if csv_file:
            self.load(csv_file)
    
    def load(self, path: str) -> None:
        try:
            self.iterator = ImageIterator(path)
            self.current_index = 0
            
            if len(self.iterator) == 0:
                QMessageBox.warning(self, "Ошибка", "Нет изображений")
                return
            
            self.btn_prev.setEnabled(True)
            self.btn_next.setEnabled(True)
            self.show_image()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def show_image(self) -> None:
        if not self.iterator:
            return
        
        if self.current_index < 0:
            self.current_index = 0
        if self.current_index >= len(self.iterator):
            self.current_index = len(self.iterator) - 1
        
        try:
            self.current_path = self.iterator.data[self.current_index]
            pixmap = QPixmap(self.current_path)
            
            if pixmap.isNull():
                self.image.setText("Не загружается")
            else:
                self.image.resize(self.image.minimumSize())
                scaled = pixmap.scaled(self.image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image.setPixmap(scaled)
            
            folder = os.path.basename(os.path.dirname(self.current_path))
            self.info.setText(f"{self.current_index+1}/{len(self.iterator)} | Папка: {folder}")
            
        except StopIteration:
            self.info.setText("Конец")
    
    def next(self) -> None:
        if not self.iterator or self.current_index >= len(self.iterator) - 1:
            QMessageBox.information(self, "Информация", "Это последнее изображение")
            return
        
        self.current_index += 1
        self.show_image()
    
    def prev(self) -> None:
        if not self.iterator or self.current_index <= 0:
            QMessageBox.information(self, "Информация", "Это первое изображение")
            return
        
        self.current_index -= 1
        self.show_image()
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        if self.current_path:
            pixmap = QPixmap(self.current_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(self.image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image.setPixmap(scaled)


def main() -> None:
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()