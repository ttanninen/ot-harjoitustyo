from services.sequencer import Sequence, Track
from services.audioengine import AudioEngine

class App:
    def __init__(self):
        self.engine = AudioEngine()
        self.sequence = Sequence(bpm=120, steps_per_beat=4, engine=self.engine)

    def start(self):
        self.engine.start()

    def stop(self):
        self.sequence.stop()
        self.engine.stop()

    def add_track(self, filename, name, pattern: list | None=None):
        track = Track(filename, name, pattern)
        track.set_length(self.sequence.length() or 16)
        self.sequence.add_track(track)
        return track
    
    def remove_track(self, track):
        self.sequence.tracks.remove(track)

    def set_bpm(self, bpm):
        self.sequence.bpm = bpm

    
