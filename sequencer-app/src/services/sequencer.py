import threading
import time
import numpy as np

from services.audioengine import AudioEngine, load_sound

class Track:
    '''
    Track class contains the pattern sequence in numpy array of 
    0's (=empty step) and 1's (=play sound at step). 
    Track audio sample is stored in track.data in raw format.
    Other parameters include the sample volume and panning.

    Track methods include writing pattern, writing steps, 
    erasing steps and creating a blank pattern of certain length.
    '''


    def __init__(self, filename: str, name: str, pattern: list | None = None):
        self.filename = filename
        self.name = name
        self.pattern = np.array(pattern if pattern is not None else [])
        self.volume = 1.0
        self.pan = 0.0
        self.data, self.samplerate = load_sound(filename)

    def replace_pattern(self, new_pattern: list):
        # Replace whole pattern
        self.pattern = np.array(new_pattern)

    def write_step(self, step: int):
        self.pattern[step] = 1

    def erase_step(self, step: int):
        self.pattern[step] = 0

    def set_length(self, number_of_steps: int):
        # Create an empty pattern of length n
        self.pattern = np.array([0 for s in range(number_of_steps)])


class Sequence:
    '''
    Sequence class contains the sequence settings: tempo and time division.
    Audio engine contains the information where the audio files are sent to be played.
    Sequence tracks are stored as a list which can be empty at the initialization.

    Sequence contains three types of methods: 
    - Track management
    - Playback controls
    - Internal loop and timing management

    The internal playing loop is run in its own thread.
    '''

    def __init__(self,
                 engine: AudioEngine,
                 bpm: int,
                 steps_per_beat: int = 4,
                 num_steps: int = 16,
                 tracks: list | None = None,
                 ):
        self.engine = engine
        self.bpm = bpm
        self.steps_per_beat = steps_per_beat
        self.num_steps = num_steps
        self.tracks = tracks if tracks is not None else []

        self._playing = False
        self._paused = False
        self._current_step = 0
        self._thread = None

    # Properties to be called from the UI:
    @property
    def is_playing(self):
        return self._playing

    @property
    def is_paused(self):
        return self._paused

    @property
    def current_step(self):
        return self._current_step

    # Basic track functions:
    def add_track(self, filename, name, pattern: list | None = None):
        track = Track(filename, name, pattern)
        if pattern is None:
            track.set_length(self.num_steps)
        self.tracks.append(track)
    
    def set_length(self, num_steps: int):
        for track in self.tracks:
            current_length = len(track.pattern)
            if num_steps <= current_length:
                track.pattern = track.pattern[:num_steps]
            else:
                new_steps = np.array([0 for s in range(num_steps - current_length)])
                track.pattern = np.concatenate([track.pattern, new_steps])
        self.num_steps = num_steps

        if self._current_step >= self.num_steps:
            self._current_step = 0
 
    def remove_track(self, track: Track):
        self.tracks.remove(track)

    def move_track_up(self, track: Track):
        i = self.tracks.index(track)
        if i > 0:
            self.tracks[i], self.tracks[i -
                                        1] = self.tracks[i - 1], self.tracks[i]

    def move_track_down(self, track: Track):
        i = self.tracks.index(track)
        if i < len(self.tracks) - 1:
            self.tracks[i], self.tracks[i +
                                        1] = self.tracks[i + 1], self.tracks[i]

    def length(self):
        return self.num_steps

    def play(self):
        if self._playing:  # If already playing, do nothing
            return

        if self._paused:  # If paused, resume
            self._paused = False

        else:  # Play from the beginning
            self._current_step = 0

        self._playing = True

        # Run audio playback in separate thread!
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
            track.set_length(self.num_steps)

    def _step_duration(self):
        return (60 / self.bpm) / self.steps_per_beat

    def _trigger_step(self, step: int):
        for track in self.tracks:
            if step < len(track.pattern) and track.pattern[step] == 1:
                self.engine.play(
                    track.data, volume=track.volume, pan=track.pan)

    def _play_loop(self):
        next_step_time = time.perf_counter()

        while self._playing:
            if not self.tracks:
                self._playing = False
                break
            self._trigger_step(self._current_step)
            self._current_step = (self._current_step + 1) % self.length() # Loop the steps
            next_step_time += self._step_duration()
            # Wait time to advance to next step
            sleep_for = next_step_time - time.perf_counter()
            if sleep_for > 0:
                time.sleep(sleep_for)
