import numpy as np
import audioengine as audio
import clock

class Track:
    def __init__(self, filename, name, pattern=[]):
        self.filename = filename
        self.name = name
        self.pattern = np.array([pattern])

    def add_pattern(self, new_pattern):
        self.pattern = np.array(new_pattern)

class Sequence:
    def __init__(self, bpm, steps_per_beat, tracklist):
        self.bpm = bpm
        self.steps_per_beat = steps_per_beat
        self.tracklist = tracklist

    def step_duration(self):
        return (60 / self.bpm) /self.steps_per_beat * 1000

    def add_track(self, Track):
        self.tracklist.append(Track)

    def play(self):
        current_step = 0
        last_step_time = clock.get_ticks()
        

    def stop(self):

    def length(self):
        return max([len(track.pattern) for track in self.tracklist])
