from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QFont
from ui.play_box import PlayBox
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

        # Chapter list
        self.text_reader = TextReader()
        self.chapter_list = ChapterList(self.chapters.keys())  # Pass chapter titles
        self.chapter_list.chapter_selected.connect(self.load_chapter)
        
        #Current playing chapter box
        self.play_box = PlayBox()
        self.play_box.play_pause_clicked.connect(self.toggle_playback)
        self.play_box.next_paragraph_clicked.connect(self.next_paragraph)
        self.play_box.prev_paragraph_clicked.connect(self.prev_paragraph)
        self.play_box.next_chapter_clicked.connect(self.next_chapter)
        self.play_box.prev_chapter_clicked.connect(self.prev_chapter)
        
        self.playing_index = None
        
        self.tts_thread = None
        self.current_paragraph_index = 0
        
        # Play/Stop buttons
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
        main_layout.addWidget(self.play_box, 3)
        
        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addLayout(button_layout)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def load_chapter(self, chapter_title):
        """Loads and displays the selected chapter's text."""
        chapter_text = self.chapters_html.get(chapter_title, "Chapter not found.")
        paragraphs = chapter_text.find_all('p')
        self.text_chunks = [p.get_text() for p in paragraphs]

        self.selected_chapter = chapter_title

        # chapter_text = self.chapters.get(chapter_title, "Chapter not found.")
        # self.text_reader.display_text(chapter_text)
        self.text_reader.display_text_chunks(chapter_title, self.text_chunks)
        
        
    def start_playback(self):
        self.tts_thread = TTS(self.text_chunks)
        # Connect Signals
        self.tts_thread.chunk_started.connect(self.set_playing_index)
        
        self.tts_thread.start()
        
        self.play_box.initialize_text_chunks(self.text_chunks, self.selected_chapter)
    
    def set_playing_index(self, index):
        self.playing_index = index
        if self.selected_chapter == self.play_box.current_playing_chapter:
            self.text_reader.highlight_paragraph(index)
        self.play_box.update_paragraph_index(index)
        
    def stop_playback(self):
        if self.tts_thread:
            self.tts_thread.stop()
            self.text_reader.unhighlight_paragraph_all()

    def toggle_playback(self):
        """Starts or pauses playback."""
        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.stop()
            self.play_box.toggle_play_pause(False)
        else:
            text_chunks = self.text_reader.get_text_chunks()
            self.tts_thread = TTS(text_chunks)
            self.tts_thread.word_spoken.connect(self.update_highlight)
            self.tts_thread.finished.connect(self.on_tts_finished)
            self.tts_thread.start()
            self.play_box.toggle_play_pause(True)
    
    def next_paragraph(self):
        """Moves to the next paragraph."""
        self.current_paragraph_index += 1
        self.text_reader.show_chunk(self.current_paragraph_index)
        self.play_box.update_paragraph(self.text_reader.get_current_paragraph())
    
    def prev_paragraph(self):
        """Moves to the previous paragraph."""
        if self.current_paragraph_index > 0:
            self.current_paragraph_index -= 1
            self.text_reader.show_chunk(self.current_paragraph_index)
            self.play_box.update_paragraph(self.text_reader.get_current_paragraph())
    
    def next_chapter(self):
        """Moves to the next chapter."""
        self.chapter_list.select_next_chapter()
    
    def prev_chapter(self):
        """Moves to the previous chapter."""
        self.chapter_list.select_previous_chapter()
