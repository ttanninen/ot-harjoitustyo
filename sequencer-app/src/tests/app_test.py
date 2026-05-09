import unittest
import app

class testApp(unittest.TestCase):
    def setUp(self):
        self.app = app.App()
    
    def test_start_stream(self):
        self.app.engine.start()

        self.assertTrue(self.app.engine._device.running)

    def test_stop_stream(self):
        self.app.engine.start()
        self.app.engine.stop()

        self.assertFalse(self.app.engine._device.running)

    def test_stop_playback(self):
        self.app.engine.start()
        self.app.engine.stop()

        self.assertFalse(self.app.sequence._playing)

    def tearDown(self):
        self.app.engine.stop()