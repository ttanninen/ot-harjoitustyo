import sounddevice as sd
import soundfile as sf
import numpy as np

def load_sound(filename):
    # Read waveform (numpy array) and samplerate from file
    data, samplerate = sf.read(filename, dtype="float32")

    # Convert to mono if not already
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    return data, samplerate

class Audio_file:
    def __init__(self, data, volume, pan):
        self.data = data
        self.position = 0 # Pointer to waveform playback position in the stream
        self.volume = volume
        self.pan = pan


class AudioEngine:
    def __init__(self, samplerate=44100, blocksize=512):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self._sounds = [] # Sounds in playback queue
        
        # Initialize stereo audio stream where audio files are inserted
        self._stream = sd.OutputStream(
            samplerate= self.samplerate,
            blocksize= self.blocksize,
            channels=2,
            callback=self._callback
        )

    def start(self):
        self._stream.start()

    def stop(self):
        self._stream.stop()

    def play(self, sample, volume=1.0, pan=0.0):
        self._sounds.append(Audio_file(sample, volume, pan))

    ### AI-generated code begins ###

    def _callback(self, outdata, frames, time, status):
        # Create empty output buffer
        buffer = np.zeros((frames, 2), dtype="float32")

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
        outdata[:] = buffer
    
    ### AI-generated code ends ###
