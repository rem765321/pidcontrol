class BenzCar():
    brand = '奔驰'  # 品牌属性
    country = '德国'  # 产地属性

    @staticmethod#类的静态方法#从而可以实现实例化使用 C().f()，当然也可以不实例化调用该方法 C.f()。
    def pressHorn():
        print('嘟嘟~~~~~~')

    def __init__(self,color,esn):
        self.color=color
        self.engineSN=esn

class BenzCar2016(BenzCar):
    price = 222222
    model = 'BenzCar2016'




BenzCar.pressHorn()
#BenzCar().pressHorn()
#car1=BenzCar()#加括号相当于实例化了
#car2=BenzCar()
car3=BenzCar('green','42424')
carlist = []

# for n in range(100):
#     carlist.append(BenzCar())

#print(carlist)
car4=BenzCar2016('red','11111')
print(car4.brand)


class Benz2018(BenzCar):
    price = 880000
    model = 'Benz2018'

    def __init__(self, color, engineSN, weight):
        # 先调用父类的初始化方法
        BenzCar.__init__(self, color, engineSN)
        self.weight = weight  # 车的重量
        self.oilweight = 0  # 油的重量

    # 加油
    def fillOil(self, oilAdded):
        self.oilweight += oilAdded
        self.weight += oilAdded

car2 = Benz2018('blue','111135545988',1500)
print (car2.oilweight)
print (car2.weight)
car2.fillOil(50)
print (car2.oilweight)
print (car2.weight)


class Benz2018Hybrid(Benz2018):
    model = 'Benz2018Hybrid'
    price = 980000

    def __init__(self, color, engineSN, weight):
        Benz2018.__init__(self, color, engineSN, weight)


# 轮胎
class Tire:
    def __init__(self, size, createDate):
        self.size = size  # 尺寸
        self.createDate = createDate  # 出厂日期


class BenzCar:
    brand = '奔驰'
    country = '德国'

    def __init__(self, color, engineSN, tires):
        self.color = color  # 颜色
        self.engineSN = engineSN  # 发动机编号
        self.tires = tires


# 创建4个轮胎实例对象
tires = [Tire(20, '20160808') for i in range(4)]
car = BenzCar('red', '234342342342566', tires)

print(car.tires[0].size)
print(tires)