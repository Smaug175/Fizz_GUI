import tkinter as tk

def create_new_window():
    new_window = tk.Toplevel(root)
    # 在新窗口中添加组件和逻辑

root = tk.Tk()

# 创建按钮，点击按钮时创建新窗口
button = tk.Button(root, text="Create New Window", command=create_new_window)
button.pack()

root.mainloop()
