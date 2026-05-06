import os
import unittest
import numpy as np
import miniaudio


from services.audioengine import AudioEngine, load_sound

dirname = os.path.dirname(__file__)


class testLoad_Sound(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(dirname, "testfile.wav")
        self.decoded = miniaudio.decode_file(
            self.filename,
            output_format=miniaudio.SampleFormat.FLOAT32,
            nchannels=1,
            sample_rate=44100,
        )
        
        self.valid_data = np.frombuffer(self.decoded.samples, dtype=np.float32).copy()
        self.valid_sample_rate = self.decoded.sample_rate
    
    def test_load_sound_data(self):
        test_data, test_sample_rate = load_sound(self.filename)
        
        self.assertEqual(str(test_data), str(self.valid_data))

    def test_load_sound_sample_rate(self):
        test_data, test_sample_rate = load_sound(self.filename)
        
        self.assertEqual(int(test_sample_rate), int(self.valid_sample_rate))

    def test_too_long_audio_raise_exception(self):
        too_long_sample = os.path.join(dirname, "too_long_sample.wav")

        self.assertRaises(ValueError, load_sound, too_long_sample)

