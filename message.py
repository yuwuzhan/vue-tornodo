class BaseData:
    def __init__(self):
        """ 
        type:{
            0:退出游戏,
            1:进入房间,
            2:加入游戏,
            3:游戏进行数据,
            4:无法加入游戏,
        }
         """
        self.data = {
            'type': 0,
            'mes': {},
        }

    def getData(self):
        return self.data

    def setType(self, mestype):
        self.data['type'] = mestype

    def setMes(self, mes):
        self.data['mes'] = mes
