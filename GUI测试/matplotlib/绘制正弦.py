from testmat import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QGridLayout, QApplication

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from matplotlib.figure import Figure
import sys

# 这个类用来画图
class Figure_Canvas(FigureCanvas):
    def __init__(self, width=4, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=100)  # 设置长宽以及分辨率
        super(Figure_Canvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)  # 创建axes对象实例，这个也可以在具体函数中添加

# 这是主界面
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Plot_Sin)  # 按键连接Plot_Sin函数

    def Plot(self):  # 这里是绘图的关键
        self.plot_Figure = Figure_Canvas()  # 创建实例
        self.plot_FigureLayout = QGridLayout(self.groupBox)  # 利用栅格布局将图像与画板连接
        self.plot_FigureLayout.addWidget(self.plot_Figure)

    def Plot_Sin(self):
        self.Plot()
        self.x = np.linspace(0, 2 * np.pi, 240, endpoint=True)
        self.y = np.sin(self.x)
        self.plot_Figure.ax.plot(self.x, self.y)  # 绘图


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())