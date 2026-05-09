import tkinter as tk

from app import App
from ui.ui import UI


def main():
    # Start app context
    app = App()
    app.start()

    # Start GUI
    root = tk.Tk()
    ui = UI(root, app) # pylint: disable=unused-variable
    root.mainloop()
    app.stop()


if __name__ == "__main__":
    main()
