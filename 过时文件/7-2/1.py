from ctypes import windll
#from sympy.physics.units.definitions.unit_definitions import ms
windll.shcore.SetProcessDpiAwareness(1)

import threading
import tkinter as tk
import time
import win32api

class MouseTracker:
    def __init__(self, canvas):
        self.canvas = canvas
        self.thread = None
        self.is_tracking = False
        self.track=[]

    def start_tracking(self):
        self.track=[]
        self.is_tracking = True
        self.thread = threading.Thread(target=self.track_mouse)
        self.thread.start()

    def stop_tracking(self):
        self.is_tracking = False
        print(len(self.track))

    def track_mouse(self):
        while self.is_tracking:
            #x, y = self.canvas.winfo_pointerxy()
            x, y = win32api.GetCursorPos()
            print(f"Mouse position: ({x}, {y})")
            self.track.append((time.time(),x,y))

def on_canvas_click(event):
    if tracker.is_tracking:
        tracker.stop_tracking()
    else:
        tracker.start_tracking()

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

tracker = MouseTracker(canvas)

canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()