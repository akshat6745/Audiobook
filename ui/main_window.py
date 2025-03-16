from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QFont
from ui.text_reader import TextReader
from ui.chapter_list import ChapterList
from speech.tts import TTS
from epub_parser.parser import extract_chapters, extract_chapters_html

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audiobook App")
        self.setGeometry(100, 100, 1000, 700)
        
        # Load EPUB chapters
        epub_path = "The_Villain_Wants_to_Live_final.epub"  # Change this path
        self.chapters = extract_chapters(epub_path)
        self.chapters_html = extract_chapters_html(epub_path)

        self.text_reader = TextReader()
        self.chapter_list = ChapterList(self.chapters.keys())  # Pass chapter titles
        self.chapter_list.chapter_selected.connect(self.load_chapter)
        
        self.tts_thread = None
        
        self.play_button = QPushButton("▶ Play")
        self.play_button.setFont(QFont("Arial", 12))
        self.play_button.setStyleSheet("padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px;")
        self.play_button.clicked.connect(self.start_playback)
        
        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.setFont(QFont("Arial", 12))
        self.stop_button.setStyleSheet("padding: 10px; background-color: #f44336; color: white; border-radius: 5px;")
        self.stop_button.clicked.connect(self.stop_playback)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)
        
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.chapter_list, 2)
        main_layout.addWidget(self.text_reader, 5)
        
        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addLayout(button_layout)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def load_chapter(self, chapter_title):
        """Loads and displays the selected chapter's text."""
        self.selected_chapter = chapter_title
        chapter_text = self.chapters.get(chapter_title, "Chapter not found.")
        self.text_reader.display_text(chapter_text)
        
    def start_playback(self):
        text = self.text_reader.text_display.toPlainText()
        # print(self.selected_chapter)
        chapter_text = self.chapters_html.get(self.selected_chapter, "Chapter not found.")
        # print(chapter_text)
        words = text.split()
        
        self.tts_thread = TTS(chapter_text)
        self.tts_thread.word_spoken.connect(self.text_reader.highlighter.apply_highlight)
        self.tts_thread.start()
        
    def stop_playback(self):
        if self.tts_thread:
            self.tts_thread.stop()
        self.text_reader.stop_highlighting()
