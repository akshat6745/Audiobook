from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from speech.highlighter import Highlighter

class TextReader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("background-color: #222; color: #ddd; font-size: 16px;")
        
        self.highlighter = Highlighter(self.text_display)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_display)
        self.setLayout(layout)

    def display_text(self, text):
        self.text_display.setText(text)
        self.highlighter.highlight_words(text)
    
    def stop_highlighting(self):
        self.highlighter.stop()
