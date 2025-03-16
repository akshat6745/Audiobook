import asyncio
import edge_tts
from PyQt6.QtCore import QThread, pyqtSignal
# from pydub import AudioSegment
# from pydub.playback import play
# from playsound import playsound
import simpleaudio as sa
from pydub import AudioSegment
import os

class TTS(QThread):
    word_spoken = pyqtSignal(int)  # Signal for highlighting
    finished = pyqtSignal()  # Signal when TTS is done

    def __init__(self, text, words, voice="en-US-JennyNeural"):
        super().__init__()
        self.text = text
        self.words = words
        self.voice = voice
        self.running = True
        self.output_file = "output.mp3"  # Temporary file for audio

    async def speak_async(self):
        """Generates speech and saves it as an audio file."""
        tts = edge_tts.Communicate(self.text, self.voice)
        await tts.save(self.output_file)  # Save the generated speech

    
    def run(self):
        """Runs the TTS function and plays the audio."""
        print("Generating TTS audio...")
        asyncio.run(self.speak_async())  # Generate TTS audio

        # Convert MP3 to WAV
        wav_output = "output.wav"
        audio = AudioSegment.from_file(self.output_file, format="mp3")
        audio.export(wav_output, format="wav")

        # Play the WAV file
        wave_obj = sa.WaveObject.from_wave_file(wav_output)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until playback is finished

        os.remove(wav_output)  # Clean up temporary file
        self.finished.emit()  # Notify when done

    def stop(self):
        self.running = False
