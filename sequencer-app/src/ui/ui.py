import os
import tkinter as tk
from services.sequencer import Sequence, Track
from services.audioengine import AudioEngine

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
            tk.Label(
                self.grid_frame,
                text=track.name,
                width=10,
                anchor="w",
            ).grid(row=track_i, column=0, padx=(4, 8), pady=2)

            row_buttons = []
            for step_i in range(num_steps):
                active = bool(track.pattern[step_i])
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
