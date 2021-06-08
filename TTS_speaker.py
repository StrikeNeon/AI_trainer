import pyttsx3
import threading
from time import sleep


class voice_constructor():

    def __init__(self):
        self.engine = pyttsx3.init()  # object creation
        self.rate = self.engine.getProperty('rate')
        self.volume = self.engine.getProperty('volume')
        self.voices = self.engine.getProperty('voices')
        self.engine.connect('started-utterance', self.onStart)
        self.engine.connect('finished-utterance', self.onEnd)
        self.busy = False

    def set_rate(self, rate: int = 125):
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float = 1.0):
        self.engine.setProperty('volume', volume)

    def set_voice(self, voice_index: int = 0):
        self.engine.setProperty('voice', self.voices[voice_index].id)

    def onStart(self, name):
        self.busy = True

    def onEnd(self, name, completed):
        self.busy = False

    def print_voices(self):
        print([voice.id for voice in self.voices])

    def say_task(self, text):
        while self.busy:
            sleep(0.10)
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()
        return

    def say_command(self, text):
        threading.Thread(
                target=self.say_task, args=(text,), daemon=True
                ).start()
