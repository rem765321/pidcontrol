import time


class PID:
    def __init__(self, P, I, D): #父类初始化
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time
        self.clear()

    def clear(self): # 初始化
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.last_last_error = 0.0
        #self.int_error = 0.0
        self.windup_guard = 20.0  ###积分限幅
        self.output = 0.0

    def update_position(self, feedback_value):#####位置式pid  (这个程序把T用进去了***)  kp=kp  ki=kp/Ti    kd=kp*Td   delta_time是采样周期T
        error = self.SetPoint - feedback_value
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time #采样周期T
        delta_error = error - self.last_error   #e-e1
        if (delta_time >= self.sample_time): ##如果采样周期大于0
            self.PTerm = self.Kp * error  # 比例
            self.ITerm += error * delta_time  # 积分   # 位置式pid 求和
            if (self.ITerm < -self.windup_guard):  ##积分限幅   #位置式PID在积分项达到饱和时,误差仍然会在积分作用下继续累积，一旦误差开始反向变化，系统需要一定时间从饱和区退出，所以在u(k)达到最大和最小时，要停止积分作用，并且要有积分限幅和输出限幅
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard
            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time
            self.last_time = self.current_time  #更新上次时间
            self.last_error = error             #更新上次误差
            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)


    def update_increment(self,feedback_value):##增量式pid###可以只做PI控制
        error = self.SetPoint - feedback_value
        self.output += self.Kp * (error - self.last_error) + self.Ki * error + self.Kd * (error -2 * self.last_error + self.last_error)
        self.last_error = error
        self.last_last_error = self.last_error

        #感觉没用 只是一些说明
    # def setKp(self, proportional_gain):
    #     self.Kp = proportional_gain
    #
    # def setKi(self, integral_gain):
    #     self.Ki = integral_gain
    #
    # def setKd(self, derivative_gain):
    #     self.Kd = derivative_gain
    #
    # def setWindup(self, windup):
    #     self.windup_guard = windup
    #
    # def setSampleTime(self, sample_time):
    #     self.sample_time = sample_time
