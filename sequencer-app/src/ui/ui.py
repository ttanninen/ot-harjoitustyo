import os
import tkinter as tk
from tkinter import filedialog as fd

class UI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
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
        tk.Button(toolbar, text="Add track", width=20,
                  command=self._add_track).pack(side=tk.RIGHT)

    def build_grid(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.rebuild_grid()

    def build_track_controls(self, parent, track_i, track):
        frame = tk.Frame(parent)
        frame.grid(row=track_i, column=0, padx=(4, 8), pady=2, sticky="w")

        # Track name
        tk.Label(frame, text=track.name, width=10, anchor="w").pack(side=tk.TOP, anchor="w")

        # Volume slider
        tk.Label(frame, text="Vol", anchor="w").pack(side=tk.LEFT)
        vol_slider = tk.Scale(
        frame, from_=0.0, to=1.0, resolution=0.01,
        orient=tk.HORIZONTAL, length=80, showvalue=False,
        command=lambda v, t=track: setattr(t, "volume", float(v))
        )
        vol_slider.set(track.volume)
        vol_slider.pack(side=tk.LEFT)
        
        # Panning slider
        tk.Label(frame, text="Pan", anchor="w").pack(side=tk.LEFT)
        pan_slider = tk.Scale(
        frame, from_=-1.0, to=1.0, resolution=0.01,
        orient=tk.HORIZONTAL, length=80, showvalue=False,
        command=lambda v, t=track: setattr(t, "pan", float(v))
        )
        pan_slider.set(track.pan)
        pan_slider.pack(side=tk.LEFT)
        
        # Remove track button
        tk.Button(
            frame, text="X", width=2, fg="red",
            command=lambda t=track: self._remove_track(t)
        ).pack(side=tk.LEFT, padx=2)

    def _step_color(self, step_i, active):
        if active:
            return "#4caf50"
        # Highlight different beats for easier pattern drawing
        beat = (step_i // self.app.sequence.steps_per_beat) % 2
        return "#A0A0A0" if beat == 0 else "#d8d8d8"

    def rebuild_grid(self):
        for button in self.grid_frame.winfo_children():
            button.destroy()

        self.step_buttons.clear()
        self.grid_frame.columnconfigure(0, minsize=120) # Reserve space for track controls

        num_steps = self.app.sequence.length()

        for track_i, track in enumerate(self.app.sequence.tracks):
            self.build_track_controls(self.grid_frame, track_i, track)

            row_buttons = []
            for step_i in range(num_steps):
                active = bool(track.pattern[step_i])
                btn = tk.Button(self.grid_frame,
                                width=3,
                                relief=tk.SUNKEN if active else tk.RAISED,
                                bg=self._step_color(step_i, active),
                                command=lambda ti=track_i, si=step_i: self._toggle_step(
                                    ti, si),
                                )
                btn.grid(row=track_i, column=step_i + 1)
                row_buttons.append(btn)

            self.step_buttons.append(row_buttons)

    def _toggle_step(self, track_i, step_i):
        track = self.app.sequence.tracks[track_i]
        btn = self.step_buttons[track_i][step_i]
        if track.pattern[step_i]:
            track.erase_step(step_i)
            btn.config(relief=tk.RAISED, bg=self._step_color(step_i, False))
        else:
            track.write_step(step_i)
            btn.config(relief=tk.SUNKEN, bg="#4caf50")


    def _open_file(self):
        filetypes = (
            ("WAV files", "*.wav"),
            )
        initial_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "samples"))

        filename = fd.askopenfilename(
            title="Open a sample",
            initialdir=initial_dir,
            filetypes=filetypes
        )
        return filename
    
    def _add_track(self):
        sample = self._open_file()

        if not sample:
            return
        
        sample_name = os.path.splitext(os.path.basename(sample))[0]

        self.app.add_track(sample, sample_name)
        self.rebuild_grid()

    def _remove_track(self, track):
        self.app.remove_track(track)
        self.rebuild_grid()

    def _play(self):
        self.app.sequence.play()

    def _pause(self):
        self.app.sequence.pause()

    def _stop(self):
        self.app.sequence.stop()


