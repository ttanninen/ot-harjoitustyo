import queue
import numpy as np
import miniaudio

MAX_SAMPLE_DURATION = 10.0

def load_sound(filename: str):
    '''
    Read waveform (numpy array) and samplerate from file
    '''

    decoded = miniaudio.decode_file(
        filename,
        output_format=miniaudio.SampleFormat.FLOAT32,
        nchannels=1,
        sample_rate=44100,
    )
    data = np.frombuffer(decoded.samples, dtype=np.float32).copy()
    
    duration = len(data) / decoded.sample_rate
    if duration > MAX_SAMPLE_DURATION:
        raise ValueError(
            f"File duration is {duration:.1f}s."
            f"Maximum allowed is {MAX_SAMPLE_DURATION}"
        )

    return data, decoded.sample_rate


class AudioFile:
    def __init__(self, data: np.frombuffer, volume=1.0, pan=0.0):
        self.data = data
        self.position = 0  # Pointer to waveform playback position in the stream
        self.volume = volume
        self.pan = pan


class AudioEngine:
    def __init__(self, sample_rate=44100, buffer_ms=15):
        self.sample_rate = sample_rate
        self.buffer_ms = buffer_ms
        self._sounds = []
        self._pending = queue.SimpleQueue()

        self._device = miniaudio.PlaybackDevice(
            output_format=miniaudio.SampleFormat.FLOAT32,
            nchannels=2,
            sample_rate=self.sample_rate,
            buffersize_msec=self.buffer_ms,
        )

    def start(self):
        stream = self._generator()
        next(stream)
        self._device.start(stream)

    def stop(self):
        self._device.close()

    def play(self, audio_data: np.frombuffer, volume=1.0, pan=0.0):
        self._pending.put(AudioFile(audio_data, volume, pan))

    ### AI-generated code begins ###

    def _generator(self):
        # Yield empty bytes to prime, then loop
        frames = yield b""

        while True:

            while not self._pending.empty():
                self._sounds.append(self._pending.get_nowait())

            buffer = np.zeros((frames, 2), dtype=np.float32)

            # Prepare list of currently playing sounds
            active_sounds = []

            # Go through sounds which are queued to play
            for sound in self._sounds:
                # Calculate how much of playback is remaining
                remaining = len(sound.data) - sound.position
                # Set sound slice length to be copied to the output buffer
                length = min(frames, remaining)

                # Take a chunk of the sound
                chunk = sound.data[sound.position:sound.position + length]

                # Control volume:
                chunk = chunk * sound.volume

                # Control pan:
                left_gain = (1.0 - sound.pan) / 2.0
                right_gain = (1.0 + sound.pan) / 2.0

                buffer[:length, 0] += chunk * left_gain
                buffer[:length, 1] += chunk * right_gain

                # Move playback forward
                sound.position += length

                # if sound is still playing after loop is done, keep playing until finished
                if sound.position < len(sound.data):
                    active_sounds.append(sound)

            # Remove finished sounds from playback
            self._sounds = active_sounds

            # Prevent audio buffer from clipping:
            buffer = np.clip(buffer, -1.0, 1.0)

            # Send audio to sound device
            frames = yield buffer.tobytes()

    ### AI-generated code ends ###
