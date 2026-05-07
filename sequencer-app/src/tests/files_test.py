import os
import json

import unittest
from scipy.io import wavfile
from services.files import save_sequence, load_sequence, export_wav
from services.audioengine import AudioEngine
from services.sequencer import Sequence, Track

dirname = os.path.dirname(__file__)

class testSaveSequence(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(dirname, "testfile.wav")
        self.engine = AudioEngine()
        self.track = Track(self.filename, "Test_track", pattern=[1,0,1,0])
        self.sequence = Sequence(
            self.engine,
            bpm=128,
            steps_per_beat=4,
            num_steps=4,
            tracks=[self.track],
            )

    def test_save_file_creation(self):
        filename = "test_file.seqjson"
        try:
            save_sequence(self.sequence, filename)
            self.assertTrue(os.path.exists(self.filename))
        finally:
            os.remove(filename)

    def test_save_file_contents(self):
        filename = "test_file.seqjson"

        try:
            save_sequence(self.sequence, filename)
            with open(filename, "r", encoding="utf-8") as f:
                payload = json.load(f)

                self.assertEqual(payload["bpm"], self.sequence.bpm)
                self.assertEqual(payload["steps_per_beat"], self.sequence.steps_per_beat)
                self.assertEqual(payload["num_steps"], self.sequence.num_steps)
                self.assertEqual(len(payload["tracks"]), len(self.sequence.tracks))

        finally:
            os.remove(filename)

class testLoadSequence(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(dirname, "testfile.wav")
        self.engine = AudioEngine()
        self.track = Track(self.filename, "Test_track", pattern=[1,0,1,0])
        self.sequence = Sequence(
            self.engine,
            bpm=128,
            steps_per_beat=4,
            num_steps=4,
            tracks=[self.track],
            )
        save_sequence(self.sequence, "test_file.seqjson")

    def test_load_sequence(self):
        filename = "test_file.seqjson"
        try:
            loaded_sequence = load_sequence(self.engine, filename)

            self.assertEqual(loaded_sequence.bpm, self.sequence.bpm)
            self.assertEqual(loaded_sequence.steps_per_beat, self.sequence.steps_per_beat)
            self.assertEqual(loaded_sequence.num_steps, self.sequence.num_steps)
            self.assertEqual(len(loaded_sequence.tracks), len(self.sequence.tracks))

        finally:
            os.remove("test_file.seqjson")

    def tearDown(self):
        self.engine.stop()

class testExportWav(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(dirname, "testfile.wav")
        self.engine = AudioEngine()
        self.track = Track(self.filename, "Test_track", pattern=[1,0,1,0])
        self.sequence = Sequence(
            self.engine,
            bpm=128,
            steps_per_beat=4,
            num_steps=4,
            tracks=[self.track],
            )

    def test_export_file_creation(self):
        filename = "test_export.wav"
        try:
            export_wav(self.sequence, filename)

            self.assertTrue(os.path.exists(filename))

        finally:
            os.remove(filename)

    def test_export_file_contents(self):
        filename = "test_export.wav"

        try:
            export_wav(self.sequence, filename)
            samplerate, data = wavfile.read(filename)
            length = int((60 / self.sequence.bpm)
                         / self.sequence.steps_per_beat
                         * samplerate) * self.sequence.num_steps

            self.assertEqual(samplerate, 44100)
            self.assertEqual(len(data), length)

        finally:
            os.remove(filename)

    def tearDown(self):
        self.engine.stop()
