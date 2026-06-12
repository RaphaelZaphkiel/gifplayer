import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import sys

class OverlayGIF:
    def __init__(self, root, gif_path):
        self.root = root

        root.overrideredirect(True)
        root.attributes("-topmost", True)

        # warna transparan
        root.config(bg="black")
        root.wm_attributes("-transparentcolor", "black")

        self.label = tk.Label(root, bg="black", border=0)
        self.label.pack()

        gif = Image.open(gif_path)

        self.frames = []
        self.delays = []

        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")

            self.frames.append(ImageTk.PhotoImage(frame))

            delay = frame.info.get("duration", 40)
            self.delays.append(delay)

        self.frame = 0

        w, h = gif.size
        root.geometry(f"{w}x{h}+300+300")

        self.animate()

        # drag
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        # right click close
        self.label.bind("<Button-3>", lambda e: root.destroy())

    def animate(self):
        self.label.config(image=self.frames[self.frame])

        delay = self.delays[self.frame]

        self.frame = (self.frame + 1) % len(self.frames)

        self.root.after(delay, self.animate)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y

        self.root.geometry(f"+{x}+{y}")


if len(sys.argv) < 2:
    print("Usage:")
    print("python player.py gifname.gif")
    sys.exit()

root = tk.Tk()

OverlayGIF(root, sys.argv[1])

root.mainloop()