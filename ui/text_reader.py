from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from speech.highlighter import Highlighter
from PyQt6.QtGui import QTextCursor

class TextReader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("background-color: #222; color: #ddd; font-size: 16px;")
        
        # self.highlighter = Highlighter(self.text_display)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_display)
        self.setLayout(layout)

   
    def display_text(self, text):
        """Displays chapter content with paragraph formatting."""
        
        # Replace multiple newlines with proper paragraph breaks
        formatted_text = text.replace("\n", "<br><br>")  # Preserve paragraph spacing
        print(text)
        
        self.text_display.clear()
        self.text_display.setHtml(f"<div style='font-size: 16px; line-height: 1.6;'>{formatted_text}</div>")

        # Move cursor to the top of the chapter
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.text_display.setTextCursor(cursor)

        # Start highlighting words for speech synchronization
        # self.highlighter.highlight_words(text)
    
    def stop_highlighting(self):
        # self.highlighter.stop()
        pass