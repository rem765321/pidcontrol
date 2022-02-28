import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import  numpy as np
# fig = plt.figure(figsize = (5,5))
# ax = fig.add_subplot(221)
# ax = fig.add_subplot(222)
# ax = fig.add_subplot(223)
# ax = fig.add_subplot(224)


class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形  #python2 中super(B， self).show()  # 需要传入自己的类名以及对象self
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
    #第四步：就是画图，【可以在此类中画，也可以在其它类中画】
    def plotcos(self): ##cos图
        self.axes0 = self.fig.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes0.plot(t, s)
        #plt.show()

d = MyFigure(width=5, height=4, dpi=100)
d.axes
print(MyFigure)
print(d)
print(d.plotcos())