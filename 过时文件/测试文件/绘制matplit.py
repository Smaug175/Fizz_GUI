import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# 创建Tkinter窗口
window = tk.Tk()
window.title("Matplotlib图形")

# 创建Matplotlib图形
figure = Figure(figsize=(6, 4), dpi=100)
subplot = figure.add_subplot(1, 1, 1)
subplot.plot([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])  # 示例绘图数据

# 创建绘图区域
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# 运行Tkinter事件循环
tk.mainloop()
