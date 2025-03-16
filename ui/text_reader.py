from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from PyQt6 import QtGui
from PyQt6.QtGui import QTextCursor

class TextReader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("background-color: #222; color: #ddd; font-size: 16px;")
                
        layout = QVBoxLayout()
        layout.addWidget(self.text_display)
        self.setLayout(layout)

   
    def display_text(self, text):
        """Displays chapter content with paragraph formatting."""
        
        # Replace multiple newlines with proper paragraph breaks
        formatted_text = text.replace("\n", "<br><br>")  # Preserve paragraph spacing
        
        self.text_display.clear()
        self.text_display.setHtml(f"<div style='font-size: 16px; line-height: 1.6;'>{formatted_text}</div>")

        # Move cursor to the top of the chapter
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        # self.text_display.setTextCursor(cursor)

    def display_text_chunks(self, chapter_title, text_chunks):
        """Displays chapter content using text chunks."""
        
        self.text_display.clear()
        
        cursor = self.text_display.textCursor()
        cursor.insertHtml(f"<h2 style='font-size: 20px; color: #fff;'>{chapter_title}</h2>")
        for chunk in text_chunks:
            formatted_chunk = f"<br><div style='font-size: 16px; line-height: 1.6;'>{chunk}</div>"
            cursor.insertHtml(formatted_chunk)
        
        # Move cursor to the top of the chapter
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.text_display.setTextCursor(cursor)

        # Start highlighting words for speech synchronization
    def highlight_paragraph(self, index):
        """Highlights the paragraph with the given index."""
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        
        for i in range(index):
            cursor.movePosition(QTextCursor.MoveOperation.NextBlock)

        cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
        cursor.setCharFormat(self.get_normalized_text_format())
        cursor.movePosition(QTextCursor.MoveOperation.NextBlock)
        cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
        cursor.setCharFormat(self.get_highlight_format())
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        self.text_display.setTextCursor(cursor)

    def get_highlight_format(self):
        """Returns the text format for highlighting."""
        format = QTextCursor().charFormat()
        format.setBackground(QtGui.QColor("green"))
        return format
    def get_normalized_text_format(self):
        """Returns the text format for highlighting."""
        format = QTextCursor().charFormat()
        format.setBackground(QtGui.QColor("transparent"))
        return format
    