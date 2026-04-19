import threading
import time
import numpy as np

from services.audioengine import AudioEngine, load_sound


class Track:
    def __init__(self, filename, name, pattern: list | None=None):
        self.filename = filename
        self.name = name
        self.pattern = np.array(pattern if pattern is not None else [])
        self.volume = 1.0
        self.pan = 0.0
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

    # Track management
    @property
    def is_playing(self):
        return self._playing
    
    @property
    def current_step(self):
        return self._current_step

    def add_track(self, track: Track):
        self.tracks.append(track)

    def move_track_up(self, track):
        i = self.tracks.index(track)
        if i > 0:
            self.tracks[i], self.tracks[i - 1] = self.tracks[i - 1], self.tracks[i]

    def move_track_down(self, track):
        i = self.tracks.index(track)
        if i < len(self.tracks) - 1:
            self.tracks[i], self.tracks[i + 1] = self.tracks[i + 1], self.tracks[i] 


    def length(self):
        if not self.tracks:
            return 0
        return max([len(track.pattern) for track in self.tracks])

    # Track timing

    def step_duration(self):
        return (60 / self.bpm) / self.steps_per_beat

    # Playback controls

    def play(self):
        if self._playing:  # If already playing, do nothing
            return

        if self._paused:  # If paused, resume
            self._paused = False

        else:  # Play from the beginning
            self._current_step = 0

        self._playing = True

        # Run audio playback in separate thread
        self._thread = threading.Thread(target=self._play_loop, daemon=True)
        self._thread.start()

    def pause(self):
        if self._playing:
            self._playing = False
            self._paused = True
            if self._thread is not None:
                self._thread.join()
                self._thread = None

    def stop(self):
        self._playing = False
        self._current_step = 0
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def clear_pattern(self):
        for track in self.tracks:
            track.set_length(len(track.pattern))

    # Internal loop controls

    def _trigger_step(self, step):
        for track in self.tracks:
            if step < len(track.pattern) and track.pattern[step] == 1:
                self.engine.play(track.data, volume=track.volume, pan=track.pan)

    def _play_loop(self):
        next_step_time = time.perf_counter()

        while self._playing:
            if not self.tracks:
                self._playing = False
                break
            self._trigger_step(self._current_step)
            self._current_step = (self._current_step + 1) % self.length()
            next_step_time += self.step_duration()

            sleep_for = next_step_time - time.perf_counter()
            if sleep_for > 0:
                time.sleep(sleep_for)
