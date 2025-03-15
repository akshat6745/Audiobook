from PyQt6.QtGui import QTextCharFormat, QColor
from PyQt6.QtCore import QThread, pyqtSignal

class Highlighter(QThread):
    highlight_signal = pyqtSignal(int)

    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit  # Corrected reference
        self.format = QTextCharFormat()
        self.format.setBackground(QColor("#444444"))  # Highlight color
        self.words = []
        self.index = 0
        self.running = False
        self.highlight_signal.connect(self.apply_highlight)

    def highlight_words(self, text):
        """Starts highlighting words in the given text."""
        self.words = text.split()
        self.index = 0
        self.running = True
        self.start()

    def run(self):
        """Iterates over words and emits highlight signal."""
        while self.index < len(self.words) and self.running:
            self.highlight_signal.emit(self.index)
            self.msleep(500)  # Adjust speed as needed
            self.index += 1

    def apply_highlight(self, index):
        """Applies highlighting to the given word index."""
        try:
            index = int(index)  # Ensure index is an integer
        except ValueError:
            print(f"Warning: Received invalid index '{index}', skipping highlight.")
            return
        
        if index < 0 or index >= len(self.words):
            print(f"Warning: Index {index} out of range, skipping highlight.")
            return
        
        cursor = self.text_edit.textCursor()  # 🔥 FIX: Use self.text_edit instead of self.text_display

        # Move cursor to the start of the word
        for _ in range(index):  # Now index is an integer
            cursor.movePosition(cursor.MoveOperation.NextWord)
        
        cursor.movePosition(cursor.MoveOperation.NextWord, cursor.MoveMode.KeepAnchor)
        cursor.mergeCharFormat(self.format)  # 🔥 FIX: Use self.format instead of self.highlight_format

        self.text_edit.setTextCursor(cursor)  # 🔥 FIX: Use self.text_edit

    def stop(self):
        """Stops highlighting."""
        self.running = False
