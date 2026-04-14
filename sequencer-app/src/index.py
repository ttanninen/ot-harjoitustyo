import os
import tkinter as tk

from ui.ui import UI
from services.sequencer import Sequence, Track
from services.audioengine import AudioEngine

def main():

    # Add initial sample files

    dirname = os.path.dirname(__file__)

    kick = os.path.join(dirname, "samples", "bd01.wav")
    snare = os.path.join(dirname, "samples", "sd01.wav")
    hihat = os.path.join(dirname, "samples", "ch01.wav")

    # Start audio engine

    engine = AudioEngine()
    engine.start()

    # Initialize demo sequence

    seq = Sequence(bpm=120, steps_per_beat=4, engine=engine)

    kick_sample = Track(kick,  "Kick",  pattern=[
                        1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
    snare_sample = Track(snare, "Snare", pattern=[
                        0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0])
    hihat_sample = Track(hihat, "Hi-hat", pattern=[
                        0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0])

    seq.add_track(kick_sample)
    seq.add_track(snare_sample)
    seq.add_track(hihat_sample)

    # Initialize GUI and run main loop
    root = tk.Tk()
    app = UI(root, seq)
    root.mainloop()
    engine.stop()

if __name__ == "__main__":
    main()
