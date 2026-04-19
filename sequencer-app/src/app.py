from services.sequencer import Sequence, Track
from services.audioengine import AudioEngine


class App:
    '''
    This is the context manager of the application. It hosts the instances of audio engine and main sequence
    '''

    def __init__(self):
        self.engine = AudioEngine()
        self.sequence = Sequence(bpm=120, steps_per_beat=4, engine=self.engine)

    def start(self):
        self.engine.start()

    def stop(self):
        self.sequence.stop()
        self.engine.stop()

    # Controls for adding initial pattern
    def add_track(self, filename, name, pattern: list | None = None):
        track = Track(filename, name, pattern)
        if pattern is None:
            track.set_length(self.sequence.length() or 16)
        self.sequence.add_track(track)
        return track