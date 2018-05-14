from tornado.websocket import WebSocketHandler
import json
from tools.tools import get_name
from message import BaseData
from threading import Timer
import time

init_position = {
    0: {'x': 380, 'y': 740, 'size': 40},
    1: {'x': 20, 'y': 380, 'size': 40},
    2: {'x': 740, 'y': 380, 'size': 40},
    3: {'x': 380, 'y': 20, 'size': 40},
}


class Bullet:
    def __init__(self, belone_to, direction, pos, b_type):
        self.belone_to = belone_to
        self.type = b_type
        self.direction = direction
        self.speed = 10 + self.type*10
        self.operation_handel = {
            'direction': {
                119: [0, -self.speed],
                115: [0, self.speed],
                97: [-self.speed, 0],
                100: [self.speed, 0],
            }
        }
        self.postion = {
            'x': pos['x'],
            'y': pos['y'],
            'size': self.type*10,
        }

    def getPositon(self):
        return {
            'x': self.postion['x'],
            'y': self.postion['y'],
            'size': self.postion['size'],
            'belone_to': self.belone_to,
        }


class TankHandler(WebSocketHandler):

    users = []         # 用来存放在线用户的容器
    players = []       # 存放用户信息的容器
    bullets = []  # 存放子弹信息的容器
    mes = BaseData()
    id = ''
    bullets_type = 1
    speed = 10
    isRoomer = 0  # 是否房主
    name = ''  # 名字
    pos = {}  # 位置,大小
    direction = ''  # 方向
    operation_handel = {
        'direction': {
            119: [0, -speed],
            115: [0, speed],
            97: [-speed, 0],
            100: [speed, 0],
        }
    }

    def getPlayerInfo(self):
        players = []
        for u in self.users:
            players.append({
                'name': u.name,
                'pos': u.pos,
                'id': u.id,
            })
        return players

    def changePosition(self):
        # TODO:changePosition

        return 0

    def sendBullets(self):
        self.mes.setType(0)
        self.mes.setMes({'time': time.time()})
        for u in self.users:  # 向在线用户广播消息
            u.write_message(json.dumps(self.mes.getData()).encode())

    def set_interval(self, func, sec):
        def func_wrapper():
            self.set_interval(func, sec)
            func()
        t = Timer(sec, func_wrapper)
        t.start()
        return t

    def open(self):
        nums = len(self.users)
        if nums < 4:
            self.isRoomer = 1 if nums == 0 else 0
            self.name = get_name()
            self.pos = init_position[nums]
            self.users.append(self)
            self.id = self.users.index(self)
            self.mes.setType(2)
            player = self.getPlayerInfo()
            for u in self.users:
                send_mes = {
                    'name': u.name,
                    'isRoomer': u.isRoomer,
                    'id': self.id,
                    'numbers': player,
                }
                self.mes.setMes(send_mes)
                u.write_message(json.dumps(self.mes.getData()).encode())
        else:
            self.mes.setType(4)
            self.mes.setMes({'info': '房间人数已满'})
            self.write_message(json.dumps(self.mes.getData()).encode())
            self.close()
        self.set_interval(self.sendBullets, 1)

    def on_message(self, message):
        msg = json.loads(message)
        if msg['key'] != 32:
            self.direction = msg['key']
            self.pos['x'] += self.operation_handel['direction'][msg['key']][0]
            self.pos['y'] += self.operation_handel['direction'][msg['key']][1]
            self.mes.setType(2)
            players = self.getPlayerInfo()
            send_mes = {
                'numbers': players
            }
            self.mes.setMes(send_mes)
            for u in self.users:  # 向在线用户广播消息
                u.write_message(json.dumps(self.mes.getData()).encode())
        else:
            self.bullet = Bullet(self.id, self.direction,
                                 self.pos, self.bullets_type)

    def on_close(self):
        self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        players = self.getPlayerInfo()
        self.mes.setType(2)
        if self.isRoomer and len(self.users) > 0:
            self.users[0].isRoomer = 1
        for u in self.users:
            u.id = self.users.index(u)
            send_mes = {
                'name': u.name,
                'isRoomer': u.isRoomer,
                'id': self.id,
                'numbers': players,
            }
            self.mes.setMes(send_mes)
            u.write_message(json.dumps(self.mes.getData()).encode())

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
