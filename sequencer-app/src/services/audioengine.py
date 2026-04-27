import queue
import numpy as np
import miniaudio

MAX_SAMPLE_DURATION = 10.0

def load_sound(filename: str):
    """Read waveform (numpy array) and samplerate from file

    Raises:
        ValueError: If wav-file length surpasses MAX_SAMPLE_DURATION

    Returns:
        _type_: tuple with audio data and sample rate
    """

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
        """AudioFile object stores audio data which is read and played
        by the AudioEngine.

        Args:
            data (np.frombuffer): Audio data in raw wav format stored in numpy array
            volume (float, optional): Audio volume between 0.0-1.0. Defaults to 1.0.
            pan (float, optional): Panning between -1.0-1.0. Defaults to 0.0.
        """

        self.data = data
        self.position = 0  # Pointer to waveform playback position
        self.volume = volume
        self.pan = pan


class AudioEngine:
    def __init__(self, sample_rate=44100, buffer_ms=15):
        """AudioEngine calls methods from miniaudio and maintains the
        sound queue of samples being triggered to play. Audio is played
        using the miniaudio stream which routes the sounds to default
        sound device.

        Args:
            sample_rate (int, optional): Sample rate of the audio file. Defaults to 44100 khz.
            buffer_ms (int, optional): Audio buffer size. Defaults to 15 ms.
        """
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
        """Start the audio stream
        """
        stream = self._generator()
        next(stream)
        self._device.start(stream)

    def stop(self):
        """Stop the audio stream
        """
        self._device.close()

    def play(self, audio_data: np.frombuffer, volume=1.0, pan=0.0):
        """Play the input audio file by placing the audio data into
        the audio stream.

        Args:
            audio_data (np.frombuffer): Audio data in numpy array
            volume (float, optional): Audio volume. Defaults to 1.0.
            pan (float, optional): Audio panning. Defaults to 0.0.
        """
        self._pending.put(AudioFile(audio_data, volume, pan))

    ### AI-generated code begins ###

    def _generator(self):
        """_summary_

        Yields:
            _type_: stream of bytes
        """
        # Yield empty bytes to prime, then loop
        frames = yield b""

        while True:

            while not self._pending.empty():
                self._sounds.append(self._pending.get_nowait())

            buffer = np.zeros((frames, 2), dtype=np.float32)

            active_sounds = []

            # Go through sounds which are queued to play
            for sound in self._sounds:
                remaining = len(sound.data) - sound.position
                length = min(frames, remaining)

                chunk = sound.data[sound.position:sound.position + length]
                chunk = chunk * sound.volume

                left_gain = (1.0 - sound.pan) / 2.0
                right_gain = (1.0 + sound.pan) / 2.0

                buffer[:length, 0] += chunk * left_gain
                buffer[:length, 1] += chunk * right_gain

                sound.position += length

                if sound.position < len(sound.data):
                    active_sounds.append(sound)

            self._sounds = active_sounds

            # Prevent audio buffer from clipping:
            buffer = np.clip(buffer, -1.0, 1.0)

            frames = yield buffer.tobytes()

    ### AI-generated code ends ###
