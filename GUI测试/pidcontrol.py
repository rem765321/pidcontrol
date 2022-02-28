import PID
import time
import matplotlib

#matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import spline ### 会报错
from scipy.interpolate import make_interp_spline

# 这个程序的实质就是在前九秒保持零输出，在后面的操作中在传递函数为某某的系统中输出1

##模拟 L = 80  秒

def test_pid(P=0.2, I=0.0, D=0.0, L=100):
    """Self-test PID class

    .. note::
      ...
      for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        if pid.SetPoint > 0:
          feedback += (output - (1/i))
        if i>9:
          pid.SetPoint = 1
        time.sleep(0.02)
      ---
    """
    pid = PID.PID(P, I, D) ##调用PID类

    pid.SetPoint = 0.0  #前9s设定0  后面设定自己想要的值
    #pid.setSampleTime(0.01)#####################

    END = L
    feedback = 0

    feedback_list = []  ##反馈列表
    time_list = []      ##时间  列表
    setpoint_list = []  ##设定列表

    for i in range(1, END):
        pid.update_increment(feedback)###选择pid类型 增量pid
        output = pid.output
        if pid.SetPoint >0:  #到了第9s
            feedback += output # (output - (1/i))控制系统的函数   #
        if i > 9:
            pid.SetPoint = 100  ##前9s 输出0###########################################################################380
        #time.sleep(0.01) ## 延时0.01s ##使点 少一些 #使仿真更直观

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)#[0,0,0,0,0,0,0,0,0,1,1,1,...]
        time_list.append(i) ##[1,2,...,L]
        #print(feedback_list)
    time_sm = np.array(time_list)##x [1 2 3 ... L]
    feedback_sm =np.array(feedback_list)##y

    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)###x_smooth 等差

    feedback_smooth = make_interp_spline(time_sm, feedback_sm)(time_smooth)  #####y_smooth 线性插值

    plt.figure("PID仿真")#窗口名
    plt.plot(time_smooth, feedback_smooth)####反馈的pid线
    plt.plot(time_list, setpoint_list)  ##设定的pid

    plt.xlim((0, L))### L 时间长度##横坐标的范围 (0,l)
    plt.ylim((min(feedback_list) - pid.SetPoint*0.5, max(feedback_list) + pid.SetPoint*0.5))  ##设置纵坐标范围

    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST PID')

    #plt.ylim((1 - 0.5, 1 + 0.5)) ##设置纵坐标范围(0.5,1.5)

    plt.grid(True)##有 坐标方格
    plt.show()
    print(time_smooth,feedback_smooth)

if __name__ == "__main__":
    #test_pid(0.85, 0.001, 0.000, L=80)
    test_pid(0.68,0.010,0.05, L=100)


#