import pyttsx3


class voice_constructor():

    def __init__(self):
        self.engine = pyttsx3.init()  # object creation
        self.rate = self.engine.getProperty('rate')
        self.volume = self.engine.getProperty('volume')
        self.voices = self.engine.getProperty('voices')
        self.shutdown = False

    def set_rate(self, rate: int = 125):
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float = 1.0):
        self.engine.setProperty('volume', volume)

    def set_voice(self, voice_index: int = 0):
        self.engine.setProperty('voice', self.voices[voice_index].id)

    def print_voices(self):
        print([voice.id for voice in self.voices])

    def loop(self):
        self.engine.startLoop(False)
        while not self.shutdown:
            self.engine.iterate()
        self.engine.endLoop()
