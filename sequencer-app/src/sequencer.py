import numpy as np
import threading
import clock
from audioengine import AudioEngine, load_sound

class Track:
    def __init__(self, filename, name, pattern=None):
        self.filename = filename
        self.name = name
        self.pattern = np.array(pattern if pattern is not None else [])
        self.data, self.samplerate = load_sound(filename)

    def replace_pattern(self, new_pattern):
        # Replace whole pattern
        self.pattern = np.array(new_pattern)

    def write_step(self, step):
        self.pattern[step] = 1

    def erase_step(self, step):
        self.pattern[step] = 0

    def set_length(self, number_of_steps):
        # Create an empty pattern of length n
        self.pattern = np.array([0 for s in range(number_of_steps)])


class Sequence:
    def __init__(self, bpm, steps_per_beat, engine: AudioEngine, tracks=None):
        self.bpm = bpm
        self.steps_per_beat = steps_per_beat
        self.engine = engine
        self.tracks = tracks if tracks is not None else []
        self.playing = False

    def step_duration(self):
        return (60 / self.bpm) /self.steps_per_beat * 1000

    def add_track(self, Track):
        self.tracks.append(Track)

    def play(self):
        if self.playing: # If already playing, do nothing
            return
        
        self.playing = True
        # Run audio playback in separate thread
        thread = threading.Thread(target=self.play_loop, daemon=True)
        thread.start()

    def play_trigger(self, step):
        for track in self.tracks:
            if track.pattern[step] == 1:
                self.engine.play(track.data)

    def play_loop(self):
        # Play from the beginning
        current_step = 0
        last_step_time = self.step_duration()

        while self.playing is True:
            now = clock.get_ticks()
            if now - last_step_time >= self.step_duration():
                self.play_trigger(current_step)
                current_step = (current_step + 1) % self.length()
                last_step_time = now

            clock.tick()

    def pause(self):
        # Add here pause functionality:
        # If playing, pause at current step/playhead state.
        # Pressing pause again or play, continue from that step
        # Pressing stop resets the playhead to beginning.
        pass
        
    def stop(self):
        self.playing = False

    def length(self):
        return max([len(track.pattern) for track in self.tracks])
