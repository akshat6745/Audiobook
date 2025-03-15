from PyQt6.QtCore import QThread, pyqtSignal, QTimer
import pyttsx3

class TTS(QThread):
    word_spoken = pyqtSignal(str)  # Signal to highlight words

    def __init__(self, text, words, parent=None):
        super().__init__(parent)
        self.text = text
        self.words = words
        self.engine = pyttsx3.init()
        self._running = True

    def run(self):
        """Runs TTS processing in the main thread using QTimer."""
        QTimer.singleShot(0, self.speak)

    def speak(self):
        """Speak the text synchronously in the main thread."""
        if not self._running:
            return

        for word in self.words:
            if not self._running:
                break
            self.word_spoken.emit(word)  # Signal to highlight word
            self.engine.say(word)
        
        self.engine.runAndWait()

    def stop(self):
        """Stops the TTS playback."""
        self._running = False
        self.engine.stop()
