import unittest
from services.sequencer import Track, Sequence


class testTrack(unittest.TestCase):
    def setUp(self):
        filename = "testfile.wav"
        self.track = Track(filename, "test_name")

    def test_track_length_setting(self):
        self.track.set_length(16)

        self.assertEqual(len(self.track.pattern), 16)

    def test_track_step_write(self):
        self.track.set_length(8)
        self.track.write_step(4)

        self.assertEqual(self.track.pattern[4], 1)

    def test_track_step_erase(self):
        self.track.set_length(8)
        self.track.write_step(4)
        self.track.erase_step(4)

        self.assertEqual(self.track.pattern[4], 0)
