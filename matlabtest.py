import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline #spline 线性插值法  #使线平滑

x = np.array([6, 7, 8, 9, 10, 11, 12])#array 矩阵
y = np.array([1.53E+03, 5.92E+02, 2.04E+02, 7.24E+01, 2.72E+01, 1.10E+01, 4.70E+00])
x_smooth = np.linspace(x.min(), x.max(), 300)# 6-12 之间299个间隔 300个数据  np.linspace创建等差数列。
#print(x_smooth)   retstep=True可看数据间隔

fuc = make_interp_spline(x, y)##实现函数  线性插值法
y_smooth= fuc(x_smooth)#利用x_smooth和func函数生成y_smooth,x_smooth数量等于y_smooth数量
#  这两句 相当于#y_smooth = make_interp_spline(x,y)(x_smooth)##############################important
#y_smooth = make_interp_spline(x,y)(x_smooth)
print(x)
# print(y)
# print(x_smooth)
# print(y_smooth)
#print(fuc)

plt.plot(x_smooth, y_smooth)
plt.show()











# numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0)
# Return evenly spaced numbers over a specified interval.
# (在start和stop之间返回均匀间隔的数据)
# Returns num evenly spaced samples, calculated over the interval [start, stop].
# (返回的是 [start, stop]之间的均匀分布)
# The endpoint of the interval can optionally be excluded.
# Changed in version 1.16.0: Non-scalar start and stop are now supported.
# (可以选择是否排除间隔的终点)

# start:返回样本数据开始点
# stop:返回样本数据结束点
# num:生成的样本数据量，默认为50
# endpoint：True则包含stop；False则不包含stop
# retstep：If True, return (samples, step), where step is the spacing between samples.(即如果为True则结果会给出数据间隔)
# dtype：输出数组类型
# axis：0(默认)或-1
#例子
# >>> np.linspace(2.0, 3.0, num=5)
# array([ 2.  ,  2.25,  2.5 ,  2.75,  3.  ])
# >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
# array([ 2. ,  2.2,  2.4,  2.6,  2.8])
# >>> np.linspace(2.0, 3.0, num=5, retstep=True)
# (array([ 2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)
