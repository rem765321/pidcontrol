import sys
import PID

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QApplication
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
#import sip


mode = 0 ### 全局变量 定义开始

#创建一个matplotlib图形绘制类
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形  #python2 中super(B， self).show()  # 需要传入自己的类名以及对象self
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)#创建axes对象实例，这个也可以在具体函数中添加  给个坐标轴

    #第四步：就是画图，【可以在此类中画，也可以在其它类中画】
    def plotcos(self): ##cos图
        self.axes0 = self.fig.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes.plot(t, s)
        plt.show()

class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super().__init__()  # 调用父类构造函数，创建窗体
        #self = Ui_MainWindow()  # 创建UI对象
        self.setupUi(self)  # 构造UI界面

        # 仿真button 点击事件
        self.btnfangzhen.clicked.connect(self.fangzhen)
        # 下拉菜单信号事件
        self.comboBox.currentIndexChanged.connect(self.select)



    def Plot(self):##这里是绘图关键
        # 第五步：定义MyFigure类的一个实例
        self.F = MyFigure(width=3, height=2, dpi=100)  #意思就是给个画布

        # 第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.F_layout= QGridLayout(self.groupBox)  # 继承容器groupBox    #F_layout 这个是自己随便取的名字 且之前千万不要布好局了
        self.F_layout.addWidget(self.F)

    def Plot_sin(self):###测试绘图
        self.Plot()
        x = np.linspace(0, 2 * np.pi, 240, endpoint=True)
        y = np.sin(x)
        self.F.axes.plot(x, y)  # 绘图  axes 绘制坐标系图形对象  即self.fig.add_subplot(111)

        #self.F.axes.plot.xlim((0, 1))  ### L 时间长度##横坐标的范围 (0,l)
        # plt.ylim((min(feedback_list) - pid.SetPoint * 0.5, max(feedback_list) + pid.SetPoint * 0.5))  ##设置纵坐标范围
        #
        #self.F.axes.plot.xlabel('time (s)')
        # plt.ylabel('PID (PV)')
        # plt.title('TEST PID')

    def select(self):
        global mode
        if self.comboBox.currentText() == "增量式pid (推荐PI控制)":
            mode = 1
            print(self.comboBox.currentIndex())
        elif self.comboBox.currentText() == "位置式pid (推荐PD控制)":
            mode = 2


    def fangzhen(self):
        self.Plot()

        self.F_layout.deleteLater()  # 删除布局


        global mode
        #plt.close()
        input_kp = self.textEdit_kp.toPlainText()
        input_ki = self.textEdit_ki.toPlainText()
        input_kd = self.textEdit_kd.toPlainText()
        input_set = self.textEdit_set.toPlainText()
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


        self.F.axes.plot(time_smooth, feedback_smooth)
        self.F.axes.plot(time_list, setpoint_list)

        #plt.figure("PID仿真")  # 窗口名
        #plt.plot(time_smooth, feedback_smooth)  ####反馈的pid线
        #plt.plot(time_list, setpoint_list)  ##设定的pid

        # plt.xlim((0, L))  ### L 时间长度##横坐标的范围 (0,l)
        # plt.ylim((min(feedback_list) - pid.SetPoint * 0.5, max(feedback_list) + pid.SetPoint * 0.5))  ##设置纵坐标范围
        #
        # plt.xlabel('time (s)')
        # plt.ylabel('PID (PV)')
        # plt.title('TEST PID')
        #
        # # plt.ylim((1 - 0.5, 1 + 0.5)) ##设置纵坐标范围(0.5,1.5)
        #
        # plt.grid(True)  ##有 坐标方格
        # plt.show()
        self.textEdit.setText(str(feedback_smooth))
        #print(feedback_smooth)



if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建GUI应用程序
    ui = MainWindow()  # 创建窗体
    ui.show()
    sys.exit(app.exec_())
