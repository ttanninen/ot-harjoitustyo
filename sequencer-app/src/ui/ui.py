import tkinter as tk
from sequencer import Sequence, Track
from audioengine import AudioEngine
import clock
import os

dirname = os.path.dirname(__file__)
kick = os.path.join(dirname, "samples", "bd01.wav")
snare = os.path.join(dirname, "samples", "sd01.wav")
hihat = os.path.join(dirname, "samples", "ch01.wav")


class UI:
    def __init__(self, root, sequence):
        self.root = root
        self.sequence = sequence
        self.root.title("Simple Sequencer")
        self.step_buttons = []

        self.build_toolbar()
        self.build_grid()

    def build_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text="Play", width=10,
                  command=self._play).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Pause", width=10,
                  command=self._pause).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Stop", width=10,
                  command=self._stop).pack(side=tk.LEFT)

    def build_grid(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.rebuild_grid()

    def rebuild_grid(self):
        for button in self.grid_frame.winfo_children():
            button.destroy()

        self.step_buttons.clear()

        num_steps = self.sequence.length()

        for track_i, track in enumerate(self.sequence.tracks):
            row_buttons = []
            active = False
            for step_i in range(num_steps):
                btn = tk.Button(self.grid_frame,
                                width=3,
                                relief=tk.SUNKEN if active else tk.RAISED,
                                bg="#4caf50" if active else "#d0d0d0",
                                command=lambda ti=track_i, si=step_i: self._toggle_step(
                                    ti, si),
                                )
                btn.grid(row=track_i, column=step_i + 1)
                row_buttons.append(btn)

            self.step_buttons.append(row_buttons)

    def _toggle_step(self, track_i, step_i):
        track = self.sequence.tracks[track_i]
        btn = self.step_buttons[track_i][step_i]
        if track.pattern[step_i]:
            track.erase_step(step_i)
            btn.config(relief=tk.RAISED, bg="#d0d0d0")
        else:
            track.write_step(step_i)
            btn.config(relief=tk.SUNKEN, bg="#4caf50")

    def _play(self):
        self.sequence.play()

    def _pause(self):
        self.sequence.pause()

    def _stop(self):
        self.sequence.stop()


if __name__ == "__main__":
    clock.start()

    engine = AudioEngine()
    engine.start()

    seq = Sequence(bpm=120, steps_per_beat=4, engine=engine)

    # Add tracks — replace filenames with your own samples
    kick_sample = Track(kick,  "Kick",  pattern=[
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    snare_sample = Track(snare, "Snare", pattern=[
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    hihat_sample = Track(
        hihat, "Hi-hat", pattern=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    seq.add_track(kick_sample)
    seq.add_track(snare_sample)
    seq.add_track(hihat_sample)

    root = tk.Tk()
    app = UI(root, seq)
    root.mainloop()

    clock.stop()
    engine.stop()
