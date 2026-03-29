import numpy as np
import audioengine as audio
import clock

class Track:
    def __init__(self, filename, name, pattern=None):
        self.filename = filename
        self.name = name
        self.pattern = np.array(pattern if pattern is not None else [])

    def replace_pattern(self, new_pattern):
        self.pattern = np.array(new_pattern)

class Sequence:
    def __init__(self, bpm, steps_per_beat, tracklist=None):
        self.bpm = bpm
        self.steps_per_beat = steps_per_beat
        self.tracklist = tracklist if tracklist is not None else []
        self.playing = False

    def step_duration(self):
        return (60 / self.bpm) /self.steps_per_beat * 1000

    def add_track(self, Track):
        self.tracklist.append(Track)

    def play(self):
        current_step = 0
        last_step_time = clock.get_ticks()
        
        self.playing = True

        while self.playing is True:
            now = clock.get_ticks()
            if now - last_step_time >= self.step_duration():
                if self.tracklist[0].pattern[current_step] == 1:
                    audio.play(self.tracklist[0].filename)

                current_step = (current_step + 1) % self.length()
                last_step_time = now
            clock.tick()

    def stop(self):
        self.playing = False

    def length(self):
        return max([len(track.pattern) for track in self.tracklist])
