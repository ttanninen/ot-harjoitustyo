import os
import unittest


from services.sequencer import Track, Sequence
from services.audioengine import AudioEngine

dirname = os.path.dirname(__file__)


class testTrack(unittest.TestCase):
    def setUp(self):
        filename = os.path.join(dirname, "testfile.wav")
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

    def test_replace_pattern(self):
        pattern = [1, 0, 0, 1]
        self.track.set_length(4)
        self.track.replace_pattern(pattern)

        self.assertEqual(self.track.pattern.tolist(), [1, 0, 0, 1])


class testSequence(unittest.TestCase):
    def setUp(self):
        filename = os.path.join(dirname, "testfile.wav")
        self.track1 = Track(filename, "test_name1")
        self.track2 = Track(filename, "test_name2")
        self.engine = AudioEngine()
        self.sequence = Sequence(bpm=120, steps_per_beat=4, engine=self.engine)


    def test_add_track(self):
        self.sequence.add_track(self.track1)

        self.assertEqual(self.sequence.tracks[0], self.track1)

    def test_move_track_up(self):
        self.sequence.add_track(self.track1)
        self.sequence.add_track(self.track2)
        self.sequence.move_track_up(self.track2)

        self.assertEqual(self.sequence.tracks[0].name, "test_name2")

    def test_move_first_track_up(self):
        self.sequence.add_track(self.track1)
        self.sequence.add_track(self.track2)
        self.sequence.move_track_up(self.track1)

        self.assertEqual(self.sequence.tracks[0].name, "test_name1")

    def test_move_track_down(self):
        self.sequence.add_track(self.track1)
        self.sequence.add_track(self.track2)
        self.sequence.move_track_down(self.track1)

        self.assertEqual(self.sequence.tracks[1].name, "test_name1")

    def test_move_last_track_down(self):
        self.sequence.add_track(self.track1)
        self.sequence.add_track(self.track2)
        self.sequence.move_track_down(self.track2)

        self.assertEqual(self.sequence.tracks[1].name, "test_name2")

    def test_sequence_length_with_no_tracks(self):
        self.assertEqual(self.sequence.length(), 0)

    def test_sequence_length_with_empty_track(self):
        self.sequence.add_track(self.track1)

        self.assertEqual(self.sequence.length(), 0)

    def test_sequence_length_with_filled_track(self):
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.assertEqual(self.sequence.length(), 4)

    def test_step_duration(self):
        self.assertEqual(self.sequence.step_duration(), 0.125)

    def test_play_when_stopped_and_not_paused(self):
        # Must have tracks to play:
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.sequence._playing = False
        self.sequence._paused = False

        self.sequence.play()
        self.assertEqual(self.sequence.is_playing, True)

    def test_play_when_playing_and_not_paused(self):
        # Must have tracks to play:
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.sequence._playing = True
        self.sequence._paused = False

        self.sequence.play()
        self.assertEqual(self.sequence.is_playing, True)

    def test_play_when_paused(self):
        # Must have tracks to play:
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.sequence._playing = False
        self.sequence._paused = True

        self.sequence.play()
        self.assertEqual(self.sequence.is_playing, True)

    def test_play_from_start(self):
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.sequence.play()
        self.assertEqual(self.sequence.current_step, 1)

    def test_play_threading(self):
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)
        self.sequence.play()

        self.assertIsNotNone(self.sequence._thread, True)

    def test_pause_when_not_playing(self):
        # Must have tracks to play:
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.sequence._playing = False
        self.sequence._paused = False

        self.sequence.pause()
        self.assertEqual(self.sequence.is_paused, False)

    def test_pause_when_playing(self):
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.sequence._playing = True
        self.sequence._paused = False

        self.sequence.pause()
        self.assertEqual(self.sequence.is_paused, True)

    def test_pause_threading_join(self):
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)
        self.sequence.play()
        self.sequence.pause()

        self.assertIsNone(self.sequence._thread, True)

    def test_stop_when_playing(self):
        # Must have tracks to play:
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.sequence._playing = True
        self.sequence.stop()

        self.assertEqual(self.sequence._playing, False)

    def test_stop_return_to_first_step(self):
        # Must have tracks to play:
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.sequence._playing = True
        self.sequence.stop()

        self.assertEqual(self.sequence._current_step, 0)

    def test_stop_threading_join(self):
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)
        self.sequence.play()
        self.sequence.stop()

        self.assertIsNone(self.sequence._thread, False)

    def test_clear_pattern(self):
        self.track1.replace_pattern([1, 0, 0, 0])
        self.sequence.add_track(self.track1)

        self.sequence.clear_pattern()

        self.assertEqual(
            self.sequence.tracks[0].pattern.tolist(), [0, 0, 0, 0])

    def test_play_loop_without_tracks(self):
        self.sequence.play()

        self.assertEqual(self.sequence._playing, False)
