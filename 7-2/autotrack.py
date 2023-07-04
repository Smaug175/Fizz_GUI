import win32api

while True:
    x, y = win32api.GetCursorPos()
    print("鼠标位置：", x, y)