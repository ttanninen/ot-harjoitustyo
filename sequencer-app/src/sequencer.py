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
        
        self._playing = False
        self._paused = False
        self._current_step = 0
        self._thread = None

    ### Track management

    def add_track(self, Track):
        self.tracks.append(Track)

    def length(self):
        return max([len(track.pattern) for track in self.tracks])

    ### Track timing

    def step_duration(self):
        return (60 / self.bpm) /self.steps_per_beat * 1000

    ### Playback controls

    def play(self):
        if self._playing: # If already playing, do nothing
            return
        
        if self._paused: # If paused, resume
            self._paused == False

        else: # Play from the beginning
            self._current_step = 0

        self._playing = True
        
        # Run audio playback in separate thread
        self._thread = threading.Thread(target=self._play_loop, daemon=True)
        self._thread.start()

    def pause(self):
        if self._playing:
            self._playing = False
            self._paused = True
            
    def stop(self):
        self._playing = False


    ### Internal loop controls

    def _play_trigger(self, step):
        for track in self.tracks:
            if track.pattern[step] == 1:
                self.engine.play(track.data)

    def _play_loop(self):
        last_step_time = self.step_duration()

        while self._playing:
            now = clock.get_ticks()
            if now - last_step_time >= self.step_duration():
                self._play_trigger(self._current_step)
                self._current_step = (self._current_step + 1) % self.length()
                last_step_time = now

            clock.tick()


