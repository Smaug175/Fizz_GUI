import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class Paint(QWidget):
    def __init__(self):
        super(Paint, self).__init__()
        self.resize(400, 300) # 设置窗口大小
        self.move(100, 100)
        self.setWindowTitle("画板") # 设置窗口标题
        # setMouseTracking设置为False，以便在按下鼠标时跟踪鼠标事件
        self.setMouseTracking(False)
        self.points = [] # 定义列表，用来存储鼠标移动轨迹上的所有点

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine) # 创建画笔对象
        painter.setPen(pen) # 设置画笔
        if len(self.points) > 1: # 判断是否至少有两个点
            start = self.points[0] # 记录开始点
            # 循环在相邻两个点之间画线，以便形成鼠标移动轨迹
            for temp in self.points: # 利用中间变量pos_tmp遍历整个points列表
                end = temp
                if end == (-1, -1): #  判断point_end是否是断点
                    start = (-1, -1) # point_start赋值为断点
                    continue
                if start == (-1, -1): # 判断point_start是否是断点
                    start = end # point_start赋值为point_end
                    continue
                # 画point_start到point_end之间的线
                painter.drawLine(start[0], start[1], end[0], end[1])
                start = end # 重新设置开始点
        painter.end()

    # 按住鼠标移动事件
    def mouseMoveEvent(self, event):
        # 定义临时变量，记录当前点
        temp = (event.pos().x(), event.pos().y())
        self.points.append(temp) # 将当前点添加到points列表中
        self.update() # 清空之前痕迹

    # 重写鼠标按住后松开的事件
    def mouseReleaseEvent(self, event):
        reset = (-1, -1) # 记录一个断点，在每次松开鼠标后停止绘制
        self.points.append(reset) # 将断点添加到points列表中
        self.update() # 刷新

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pyqt_learn = Paint()
    pyqt_learn.show()
    app.exec_()