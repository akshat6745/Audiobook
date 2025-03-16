from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import pyqtSignal

class ChapterList(QListWidget):
    chapter_selected = pyqtSignal(str)  # Signal emitted when a chapter is selected

    def __init__(self, chapters, parent=None):
        super().__init__(parent)
        self.chapters = chapters
        self.populate_list()
        self.setStyleSheet("background-color: #252525; color: #FFFFFF; font-size: 16px; border: none;")
        self.itemClicked.connect(self.emit_selected_chapter)  # Connect item click to signal

    def populate_list(self):
        for chapter_title in self.chapters:
            self.addItem(chapter_title)

    def emit_selected_chapter(self, item):
        """Emits the selected chapter title when a user clicks on it."""
        self.chapter_selected.emit(item.text())
