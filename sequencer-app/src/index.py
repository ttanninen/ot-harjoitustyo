import os
import tkinter as tk

from app import App
from ui.ui import UI


def main():
    # Start app context
    app = App()
    app.start()

    # Add initial samples and tracks
    dirname = os.path.dirname(__file__)

    kick = os.path.join(dirname, "samples", "bd01.wav")
    snare = os.path.join(dirname, "samples", "sd01.wav")
    hihat = os.path.join(dirname, "samples", "ch01.wav")

    app.add_track(kick,  "Kick",  pattern=[
        1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
    app.add_track(snare, "Snare", pattern=[
        0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0])
    app.add_track(hihat, "Hi-hat", pattern=[
        0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0])

    # Start GUI
    root = tk.Tk()
    ui = UI(root, app)
    root.mainloop()
    app.stop()


if __name__ == "__main__":
    main()
