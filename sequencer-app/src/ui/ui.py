import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog
from tkinter import messagebox


class UI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("Simple Sequencer")
        self.step_buttons = []
        self.indicators = []
        self._current_light = -1

        self.root.bind("<space>", lambda e: self._toggle_play())

        self.build_toolbar()
        self.build_indicators()
        self.build_grid()

        self._poll_step()

    def build_toolbar(self):
        '''
        Toolbar for playback control and sequence management
        '''
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Playback buttons
        tk.Button(toolbar, text="Play", width=10,
                  command=self._play).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Pause", width=10,
                  command=self._pause).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Stop", width=10,
                  command=self._stop).pack(side=tk.LEFT)

        # BPM input
        tk.Label(toolbar, text="BPM").pack(side=tk.LEFT, padx=(12, 2))
        self._bpm_var = tk.StringVar(value=str(int(self.app.sequence.bpm)))
        bpm_entry = tk.Entry(toolbar, textvariable=self._bpm_var, width=5)
        bpm_entry.pack(side=tk.LEFT)
        bpm_entry.bind("<Return>", lambda e: self._set_bpm())
        bpm_entry.bind("<FocusOut>", lambda e: self._set_bpm())

        # Sequence length input
        tk.Label(toolbar, text="Steps").pack(side=tk.LEFT, padx=(12,2))
        self._steps_var = tk.StringVar(value=str(self.app.sequence.num_steps))
        steps_entry = tk.Entry(toolbar, textvariable=self._steps_var, width=5)
        steps_entry.pack(side=tk.LEFT)
        steps_entry.bind("<Return>", lambda e: self._set_steps())
        steps_entry.bind("<FocusOut>", lambda e: self._set_steps())

        # Sequence steps per beat
        tk.Label(toolbar, text="Steps per beat").pack(side=tk.LEFT, padx=(12,2))
        self._steps_per_beat_var = tk.StringVar(value=str(self.app.sequence.steps_per_beat))
        steps_per_beat_entry = tk.Entry(toolbar, textvariable=self._steps_per_beat_var, width=5)
        steps_per_beat_entry.pack(side=tk.LEFT)
        steps_per_beat_entry.bind("<Return>", lambda e: self._set_steps_per_beat())
        steps_per_beat_entry.bind("<FocusOut>", lambda e: self._set_steps_per_beat())

        # Disable spacebar from text fields
        bpm_entry.bind("<space>", lambda e: self._toggle_play() or "break")
        steps_entry.bind("<space>", lambda e: self._toggle_play() or "break")
        steps_per_beat_entry.bind("<space>", lambda e: self._toggle_play() or "break")


        # Sequence manipulation buttons
        add_track_btn = tk.Button(toolbar, text="Add track", width=20,
                                  command=self._add_track)
        add_track_btn.pack(side=tk.RIGHT)
        add_track_btn.bind("<space>", lambda e:self._toggle_play() or "break")
        
        clear_pattern_btn = tk.Button(toolbar, text="Clear pattern", width=20,
                                      command=self._clear_pattern)
        clear_pattern_btn.pack(side=tk.RIGHT)
        clear_pattern_btn.bind("<space>", lambda e:self._toggle_play() or "break")

    # Sequencer playhead indicators
    def build_indicators(self):
        self.indicator_canvas = tk.Canvas(
            self.root, height=20, bg=self.root.cget("bg"), highlightthickness=0)
        self.indicator_canvas.pack(side=tk.TOP, fill=tk.X, padx=2)
        self.root.after(100, self._draw_indicators)

    def _draw_indicators(self):
        self.indicator_canvas.delete("all")
        self.indicators = []
        num_steps = self.app.sequence.length()

        if not self.step_buttons or not self.step_buttons[0]:
            return

        first_btn = self.step_buttons[0][0]
        x_start = first_btn.winfo_x() + first_btn.winfo_width() // 2
        step_width = first_btn.winfo_width()

        for i in range(num_steps):
            x = x_start + i * step_width
            dot = self.indicator_canvas.create_oval(
                x-5, 5, x+5, 15, fill="#3a1a1a", outline="")
            self.indicators.append(dot)

    def _update_indicators(self, step):
        if 0 <= self._current_light < len(self.indicators):
            self.indicator_canvas.itemconfig(
                self.indicators[self._current_light], fill="#3a1a1a")
        if 0 <= step < len(self.indicators):
            self.indicator_canvas.itemconfig(
                self.indicators[step], fill="#ff3333")
        self._current_light = step

    def _poll_step(self):
        step = self.app.sequence.current_step
        if self.app.sequence.is_playing:
            self._update_indicators(step)
        self.root.after(16, self._poll_step)

    # Step sequncer grid
    def build_grid(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(side=tk.TOP, fill=tk.BOTH,
                             expand=True, padx=(0, 8))

        self.rebuild_grid()

    def _step_color(self, step_i, active):
        if active:
            return "#4caf50"
        # Highlight different beats for easier pattern drawing
        beat = (step_i // self.app.sequence.steps_per_beat) % 2
        return "#A0A0A0" if beat == 0 else "#d8d8d8"

    def rebuild_grid(self):
        # Start from clean slate
        for button in self.grid_frame.winfo_children():
            button.destroy()

        self.step_buttons.clear()

        # Reserve space for track controls
        self.grid_frame.columnconfigure(0, minsize=120)

        num_steps = self.app.sequence.length()

        for track_i, track in enumerate(self.app.sequence.tracks):
            # When the number of tracks is resolved, build track controls first
            self.build_track_controls(self.grid_frame, track_i, track)

            # Read track patterns and draw the step sequencer grid accordingly
            row_buttons = []
            for step_i in range(num_steps):
                active = bool(track.pattern[step_i]) # 0 = False, 1 = True
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
        self.root.update_idletasks() # Force the grid to be finished before drawing indicators
        self._draw_indicators()

    def _toggle_step(self, track_i, step_i):
        track = self.app.sequence.tracks[track_i]
        btn = self.step_buttons[track_i][step_i]
        if track.pattern[step_i]:
            track.erase_step(step_i)
            btn.config(relief=tk.RAISED, bg=self._step_color(step_i, False))
        else:
            track.write_step(step_i)
            btn.config(relief=tk.SUNKEN, bg="#4caf50")

    # Track controls
    def build_track_controls(self, parent, track_i, track):
        frame = tk.Frame(parent)
        frame.grid(row=track_i, column=0, padx=(4, 8), pady=2, sticky="w")

        # Track name and rename button
        name_row = tk.Frame(frame)
        name_row.pack(side=tk.TOP, anchor="w")
        tk.Label(name_row, text=track.name, width=10,
                 anchor="w").pack(side=tk.LEFT)
        tk.Button(name_row, text="Rename", width=6,
                  command=lambda t=track: self._rename_track(t)
                  ).pack(side=tk.LEFT, padx=(0, 0))

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

        # Move track up button
        tk.Button(frame, text="▲", width=2,
                  command=lambda t=track: self._move_track_up(t)
                  ).pack(side=tk.LEFT, padx=2)

        # Move track down button
        tk.Button(frame, text="▼", width=2,
                  command=lambda t=track: self._move_track_down(t)
                  ).pack(side=tk.LEFT, padx=2)

        # Remove track button
        tk.Button(
            frame, text="X", width=2, fg="red",
            command=lambda t=track: self._remove_track(t)
        ).pack(side=tk.LEFT, padx=2)

    # Event handlers
    def _set_bpm(self):
        try:
            bpm = int(self._bpm_var.get())
            if 20 <= bpm <= 300:
                self.app.sequence.bpm = bpm
            else:
                self._bpm_var.set(str(int(self.app.sequence.bpm)))
        except ValueError:
            self._bpm_var.set(str(int(self.app.sequence.bpm)))

    def _set_steps(self):
        try:
            steps = int(self._steps_var.get())
            if 1 <= steps <= 32:
                self.app.sequence.set_length(steps)
                self.rebuild_grid()
            else:
                self._steps_var.set(str(self.app.sequence.num_steps))
        
        except ValueError:
            self._steps_var.set(str(self.app.sequence.num_steps))

    def _set_steps_per_beat(self):
        try:
            steps_per_beat = int(self._steps_per_beat_var.get())
            if 1 <= steps_per_beat <= 16:
                self.app.sequence.steps_per_beat = steps_per_beat
                self.rebuild_grid()
            else:
                self._steps_per_beat_var.set(str(self.app.sequence.steps_per_beat))
            
        except ValueError:
            self._steps_per_beat_var.set(str(self.app.sequence.steps_per_beat))

    def _open_file(self):
        filetypes = (
            ("WAV files", "*.wav"),
        )
        initial_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "samples"))

        filename = fd.askopenfilename(
            title="Open a sample",
            initialdir=initial_dir,
            filetypes=filetypes
        )
        return filename

    def _add_track(self):
        audio_file = self._open_file()

        if not audio_file:
            return

        filename = os.path.splitext(os.path.basename(audio_file))[0]
        
        try:
            self.app.sequence.add_track(audio_file, filename)
            self.rebuild_grid()
        except ValueError as e:
            messagebox.showerror("Invalid sample", e)
        
    def _rename_track(self, track):
        new_name = simpledialog.askstring(
            "Rename track", "Enter new name: ", initialvalue=track.name)
        if new_name:
            track.name = new_name
        self.rebuild_grid()

    def _move_track_up(self, track):
        self.app.sequence.move_track_up(track)
        self.rebuild_grid()

    def _move_track_down(self, track):
        self.app.sequence.move_track_down(track)
        self.rebuild_grid()

    def _remove_track(self, track):
        self.app.sequence.remove_track(track)
        self.rebuild_grid()

    def _clear_pattern(self):
        self.app.sequence.clear_pattern()
        self.rebuild_grid()

    def _play(self):
        self.app.sequence.play()

    def _pause(self):
        self.app.sequence.pause()

    def _stop(self):
        self.app.sequence.stop()
        self._update_indicators(-1)

    def _toggle_play(self):
        if self.app.sequence.is_playing:
            self.app.sequence.stop()
            self._update_indicators(-1)
        else:
            self.app.sequence.play()
