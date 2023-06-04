import tkinter as tk

def zoom_in():
    canvas.scale("all", 0, 0, 1.2, 1.2)

def zoom_out():
    canvas.scale("all", 0, 0, 0.8, 0.8)

root = tk.Tk()

scrollbar = tk.Scrollbar(root, orient="vertical")
scrollbar.pack(side="right", fill="y")

canvas = tk.Canvas(root, width=400, height=300, yscrollcommand=scrollbar.set)
canvas.create_arc(0, 0, 400, 300, start=0, extent=359, fill="red")
canvas.pack(side="left", expand=True, fill="both")

scrollbar.config(command=canvas.yview)

button_zoom_in = tk.Button(root, text="Zoom In", command=zoom_in)
button_zoom_in.pack()

button_zoom_out = tk.Button(root, text="Zoom Out", command=zoom_out)
button_zoom_out.pack()

root.mainloop()
