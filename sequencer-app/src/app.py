import os

from services.audioengine import AudioEngine
from services.files import load_sequence

dirname = os.path.dirname(__file__)
default = os.path.join(dirname, "projects", "default.seqjson")

class App:
    def __init__(self):
        """This is the context manager of the application. 
    It hosts the instances of audio engine and the sequence.
        """
        self.engine = AudioEngine()
        self.sequence = load_sequence(self.engine, default)

    def start(self):
        self.engine.start()

    def stop(self):
        self.sequence.stop()
        self.engine.stop()
