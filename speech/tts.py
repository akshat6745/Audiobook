import asyncio
import edge_tts
from PyQt6.QtCore import QThread, pyqtSignal
import simpleaudio as sa
from pydub import AudioSegment
import os
import subprocess

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
        
    async def speak_chunk(self, chunk, index):
        """Generates and plays speech for a single chunk."""
        self.chunk_started.emit(index)  # Emit signal when chunk starts playing
        if(chunk.strip() == "***"):
            chunk = "Asterisk Asterisk Asterisk"
        tts = edge_tts.Communicate(chunk, self.voice)
        temp_output = f"temp_chunk_{index}.mp3"
        await tts.save(temp_output)
        
        # Convert MP3 to WAV
        audio = AudioSegment.from_file(temp_output, format="mp3")
        wav_output = f"temp_chunk_{index}.wav"
        audio.export(wav_output, format="wav")
        
        # Play the WAV file
        # wave_obj = sa.WaveObject.from_wave_file(wav_output)
        # play_obj = wave_obj.play()
        # play_obj.wait_done()
        subprocess.run(["ffplay", "-nodisp", "-autoexit", wav_output], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Emit signal for highlighting
        self.word_spoken.emit(index)
        
        # Cleanup
        os.remove(temp_output)
        os.remove(wav_output)
    
    async def process_chunks(self):
        """Processes each text chunk dynamically in sequence."""
        for index, chunk in enumerate(self.text_chunks):
            if not self.running:
                break
            await self.speak_chunk(chunk, index)  # Process each chunk sequentially
        self.finished.emit()  # Notify when all chunks are spoken
        print("Finished speaking.")

    def run(self):
        """Starts processing text chunks asynchronously."""
        asyncio.new_event_loop().run_until_complete(self.process_chunks())

    def stop(self):
        self.running = False
