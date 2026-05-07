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



class testAudioEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AudioEngine()
        self.filename = os.path.join(dirname, "testfile.wav")

    def test_init_sample_rate(self):
        self.assertEqual(self.engine.sample_rate, 44100)

    def test_init_buffer(self):
        self.assertEqual(self.engine.buffer_ms, 15)

    def test_init_sounds(self):
        self.assertEqual(self.engine._sounds, [])

    def test_init_pending_empty(self):
        self.assertTrue(self.engine._pending.empty())

    def test_init_sound_device(self):
        self.assertIsInstance(self.engine._device, miniaudio.PlaybackDevice)

    def test_start_audio_stream(self):
        self.engine.start()

        self.assertTrue(self.engine._device.running)
        self.engine.stop()

    def test_init_stopped_audio_stream(self):
        self.assertFalse(self.engine._device.running)

    def test_stop_running_audio_stream(self):
        self.engine.start()
        self.engine.stop()

        self.assertFalse(self.engine._device.running)

    def test_play(self):
        test_data, test_sample_rate = load_sound(self.filename)
        self.engine.start()
        self.engine.play(test_data)

        self.assertFalse(self.engine._pending.empty())
        self.engine.stop()

    def test_generator_yield_bytes(self):
        generator = self.engine._generator()
        next(generator)
        frames = generator.send(1)
        self.assertIsInstance(frames, bytes)

    def test_generator_yields_sound_data(self):
        test_data, test_sample_rate = load_sound(self.filename)
        self.engine.start()
        self.engine.play(test_data)

        generator = self.engine._generator()
        next(generator)
        frames = generator.send(len(test_data))

        mixed = np.frombuffer(frames, dtype=np.float32)
        self.assertTrue(np.any(mixed != 0))

    def test_clipping(self):
        test_data, test_sample_rate = load_sound(self.filename)
        self.engine.start()
        self.engine.play(test_data, volume=2.0)

        generator = self.engine._generator()
        next(generator)
        frames = generator.send(len(test_data))

        mixed = np.frombuffer(frames, dtype=np.float32)
        self.assertLessEqual(mixed.max(), 1.0)
        self.assertGreaterEqual(mixed.max(),-1.0)


