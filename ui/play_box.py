from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont, QPainter, QLinearGradient, QColor
from PyQt6.QtCore import pyqtSignal

class PlayBox(QWidget):
   play_pause_clicked = pyqtSignal()  # Signal for play/pause
   next_paragraph_clicked = pyqtSignal()
   prev_paragraph_clicked = pyqtSignal()
   next_chapter_clicked = pyqtSignal()
   prev_chapter_clicked = pyqtSignal()

   def __init__(self):
      super().__init__()
      self.init_ui()

   def initialize_text_chunks(self, text_chunks, chapter_title):
      self.text_chunks = text_chunks
      self.current_playing_chapter = chapter_title

   def init_ui(self):
      layout = QVBoxLayout()
      
      # Display currently playing paragraph
      self.paragraph_label = QLabel("")
      self.paragraph_label.setFont(QFont("Times New Roman,serif", 18))  # Fixed font setting
      self.paragraph_label.setWordWrap(True)
      
      
      self.paragraph_label.setStyleSheet("""
         color: white;
         padding: 10px;
         border-radius: 5px;
      """)

      layout.addWidget(self.paragraph_label)
      
      # Play/Pause button
      self.play_pause_button = QPushButton("▶ Play")
      self.play_pause_button.setStyleSheet("padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px;")
      self.play_pause_button.clicked.connect(self.play_pause_clicked.emit)
      layout.addWidget(self.play_pause_button)
      
      # Next/Previous paragraph buttons
      para_buttons = QHBoxLayout()
      self.prev_paragraph_button = QPushButton("⬅ Prev Paragraph")
      self.next_paragraph_button = QPushButton("Next Paragraph ➡")
      
      self.prev_paragraph_button.setStyleSheet("padding: 10px; background-color: #008CBA; color: white; border-radius: 5px;")
      self.next_paragraph_button.setStyleSheet("padding: 10px; background-color: #008CBA; color: white; border-radius: 5px;")
      
      self.prev_paragraph_button.clicked.connect(self.prev_paragraph_clicked.emit)
      self.next_paragraph_button.clicked.connect(self.next_paragraph_clicked.emit)
      
      para_buttons.addWidget(self.prev_paragraph_button)
      para_buttons.addWidget(self.next_paragraph_button)
      layout.addLayout(para_buttons)
      
      # Next/Previous chapter buttons
      chapter_buttons = QHBoxLayout()
      self.prev_chapter_button = QPushButton("⬅ Prev Chapter")
      self.next_chapter_button = QPushButton("Next Chapter ➡")
      
      self.prev_chapter_button.setStyleSheet("padding: 10px; background-color: #f44336; color: white; border-radius: 5px;")
      self.next_chapter_button.setStyleSheet("padding: 10px; background-color: #f44336; color: white; border-radius: 5px;")
      
      self.prev_chapter_button.clicked.connect(self.prev_chapter_clicked.emit)
      self.next_chapter_button.clicked.connect(self.next_chapter_clicked.emit)
      
      chapter_buttons.addWidget(self.prev_chapter_button)
      chapter_buttons.addWidget(self.next_chapter_button)
      layout.addLayout(chapter_buttons)
      
      self.setLayout(layout)
   def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#557ffc"))
        gradient.setColorAt(1, QColor("#80bfff"))
        painter.fillRect(self.rect(), gradient)
        super().paintEvent(event)
      
   def update_paragraph_index(self, index):
      """Updates the currently playing paragraph index."""
      self.update_paragraph(self.text_chunks[index])

   def update_paragraph(self, text):
      """Updates the currently playing paragraph."""
      self.paragraph_label.setText(text)

   def toggle_play_pause(self, is_playing):
      """Updates the play/pause button text."""
      self.play_pause_button.setText("⏸ Pause" if is_playing else "▶ Play")
