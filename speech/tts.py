import asyncio
import edge_tts
from PyQt6.QtCore import QThread, pyqtSignal
import simpleaudio as sa
from pydub import AudioSegment
import os
from pydub.playback import _play_with_simpleaudio
import io
import pygame

class TTS(QThread):
    word_spoken = pyqtSignal(int)  # Signal for highlighting
    finished = pyqtSignal()  # Signal when TTS is done
    chunk_started = pyqtSignal(int)  # New signal for updating playing index

    def __init__(self, text_chunks, voice="en-US-JennyNeural"):
        super().__init__()
        # self.chapter_html_text = chapter_html_text
        self.voice = voice
        self.running = True
        # paragraphs = chapter_html_text.find_all('p')
        self.text_chunks = text_chunks
        self.current_process = None
        # super().__init__()
        # self.voice = voice
        # self.running = True
        # self.text_chunks = text_chunks
        self.paused = False
        pygame.mixer.init()
        
    async def speak_chunk(self, chunk, index):
        """Generates and plays speech for a single chunk with pause/resume support."""
        self.chunk_started.emit(index)

        if not chunk.strip():
            self.word_spoken.emit(index)
            return

        if chunk.strip() == "***":
            chunk = "Asterisk Asterisk Asterisk"

        try:
            tts = edge_tts.Communicate(chunk, self.voice)
            mp3_data = io.BytesIO()
            
            async for message in tts.stream():
                if message["type"] == "audio":
                    mp3_data.write(message["data"])
            
            mp3_data.seek(0)

            # Convert MP3 to WAV for pygame
            audio = AudioSegment.from_file(mp3_data, format="mp3")
            wav_data = io.BytesIO()
            audio.export(wav_data, format="wav")
            wav_data.seek(0)

            # Load into pygame.mixer and play
            pygame.mixer.music.load(wav_data)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if self.paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                await asyncio.sleep(0.1)

            self.word_spoken.emit(index)

        except Exception as e:
            print(f"Error during playback: {e}")
            self.word_spoken.emit(index)

        
    def pause(self):
        """Pauses the audio playback."""
        self.running = False
        if self.current_process:
            self.current_process.pause()  # Pause audio

    def resume(self):
        """Resumes the audio playback."""
        self.running = True
        if self.current_process:
            self.current_process.play()  # Resume audio

    def stop(self):
        """Stops the TTS thread and any ongoing audio playback."""
        self.running = False
        if self.current_process:
            self.current_process.stop()
    
    async def process_chunks(self):
        """Processes each text chunk dynamically in sequence."""
        for index, chunk in enumerate(self.text_chunks):
            if not self.running:
                break
            await self.speak_chunk(chunk, index)  # Process each chunk sequentially
            print(index)
        self.finished.emit()  # Notify when all chunks are spoken
        print("Finished speaking.")

    def run(self):
        """Starts processing text chunks asynchronously."""
        asyncio.new_event_loop().run_until_complete(self.process_chunks())
        
