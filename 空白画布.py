import tkinter as tk

# 创建主窗口
root = tk.Tk()

# 获取屏幕尺寸
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 创建画布
canvas = tk.Canvas(root, width=screen_width, height=screen_height)

# 将画布置于主窗口
canvas.pack()

# 隐藏窗口边框
root.attributes('-fullscreen', True)

#按q退出
root.bind('q', lambda event: root.destroy())

# 进入主循环
root.mainloop()
