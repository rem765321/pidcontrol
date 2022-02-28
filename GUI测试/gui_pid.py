import sys
import PID

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
from scipy.interpolate import make_interp_spline



from pid_ui import Ui_MainWindow
from functools import partial   ###传参


mode = 0 ### 全局变量 定义开始

#创建一个matplotlib图形绘制类
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形  #python2 中super(B， self).show()  # 需要传入自己的类名以及对象self
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
    #第四步：就是画图，【可以在此类中画，也可以在其它类中画】

class QmyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()  # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面

        # self.figure = Myfigure()
        # self.fig_ntb = NavigationToolbar(self.figure, self)  # 注意，记得指向figure的FigureCanvas

        # 第五步：定义MyFigure类的一个实例
        self.ui.F = MyFigure(width=3, height=2, dpi=100)
        self.plotcos()
        # 第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.ui.gridlayout= QtWidgets.QHBoxLayout(self.ui.groupBox)  # 继承容器groupBox
        self.ui.gridlayout.addWidget(self.ui.F)



        #仿真button 点击事件
        self.ui.btnfangzhen.clicked.connect(self.fangzhen)
        #下拉菜单信号事件
        self.ui.comboBox.currentIndexChanged.connect(self.select)

    def plotcos(self):
        t = np.arange(0.0, 5.0, 0.01)#  (起点，终点，步长)
        s = np.cos(2 * np.pi * t)
        self.ui.F.axes.plot(t, s)
        self.ui.F.fig.suptitle("cos")
        self.ui.F.axes.plot(t, s)

    def plotother(self):
        F1 = MyFigure(width=5, height=4, dpi=100)
        F1.fig.suptitle("Figuer_4")
        F1.axes1 = F1.fig.add_subplot(221)
        x = np.arange(0, 50)
        y = np.random.rand(50)
        F1.axes1.hist(y, bins=50)
        F1.axes1.plot(x, y)
        F1.axes1.bar(x, y)
        F1.axes1.set_title("hist")
        F1.axes2 = F1.fig.add_subplot(222)

        ## 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        F1.axes2.plot(x, y)
        F1.axes2.set_title("line")
        # 散点图
        F1.axes3 = F1.fig.add_subplot(223)
        F1.axes3.scatter(np.random.rand(20), np.random.rand(20))
        F1.axes3.set_title("scatter")
        # 折线图
        F1.axes4 = F1.fig.add_subplot(224)
        x = np.arange(0, 5, 0.1)
        F1.axes4.plot(x, np.sin(x), x, np.cos(x))
        F1.axes4.set_title("sincos")
        self.gridlayout.addWidget(F1, 0, 2)

    def select(self):
        global mode
        if self.ui.comboBox.currentText() == "增量式pid (推荐PI控制)":
            mode = 1
            print(self.ui.comboBox.currentIndex())
        elif self.ui.comboBox.currentText() == "位置式pid (推荐PD控制)":
            mode = 2


    def fangzhen(self):
        global mode
        plt.close()
        input_kp = self.ui.textEdit_kp.toPlainText()
        input_ki = self.ui.textEdit_ki.toPlainText()
        input_kd = self.ui.textEdit_kd.toPlainText()
        input_set = self.ui.textEdit_set.toPlainText()
        ##result = float(input_set) *6.7

        P = float(input_kp)
        I = float(input_ki)
        D = float(input_kd)


        pid = PID.PID(P, I, D)  ##调用PID类

        pid.SetPoint = 0.0  # 前9s设定0  后面设定自己想要的值
        # pid.setSampleTime(0.01)#####################

        L = 100
        END = L
        feedback = 0

        feedback_list = []  ##反馈列表
        time_list = []  ##时间  列表
        setpoint_list = []  ##设定列表

        for i in range(1, END):
            if (mode ==1 ):
                pid.update_increment(feedback)  ###选择pid类型 增量pid
            elif (mode == 2):
                pid.update_position(feedback)
            else :
                pid.update_increment(feedback)
            output = pid.output
            if pid.SetPoint > 0:  # 到了第9s
                feedback += output  # (output - (1/i))控制系统的函数   #
            if i > 9:
                pid.SetPoint = float(input_set) ##前9s 输出0###########################################################################380
            # time.sleep(0.01) ## 延时0.01s ##使点 少一些 #使仿真更直观

            feedback_list.append(feedback)
            setpoint_list.append(pid.SetPoint)  # [0,0,0,0,0,0,0,0,0,1,1,1,...]
            time_list.append(i)  ##[1,2,...,L]
            # print(feedback_list)
        time_sm = np.array(time_list)  ##x [1 2 3 ... L]
        feedback_sm = np.array(feedback_list)  ##y

        time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)  ###x_smooth 等差

        feedback_smooth = make_interp_spline(time_sm, feedback_sm)(time_smooth)  #####y_smooth 线性插值

        plt.figure("PID仿真")  # 窗口名
        plt.plot(time_smooth, feedback_smooth)  ####反馈的pid线
        plt.plot(time_list, setpoint_list)  ##设定的pid

        plt.xlim((0, L))  ### L 时间长度##横坐标的范围 (0,l)
        plt.ylim((min(feedback_list) - pid.SetPoint * 0.5, max(feedback_list) + pid.SetPoint * 0.5))  ##设置纵坐标范围

        plt.xlabel('time (s)')
        plt.ylabel('PID (PV)')
        plt.title('TEST PID')

        # plt.ylim((1 - 0.5, 1 + 0.5)) ##设置纵坐标范围(0.5,1.5)

        plt.grid(True)  ##有 坐标方格
        plt.show()
        self.ui.textEdit.setText(str(feedback_smooth))
        #print(feedback_smooth)



if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
