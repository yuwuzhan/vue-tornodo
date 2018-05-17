from tornado.websocket import WebSocketHandler
import json
from tools.tools import get_name
from message import BaseData
from threading import Timer

common_send_sign = 0
all_bullet = []
init_position = {
    0: {'x': 380, 'y': 740, 'size': 40},
    1: {'x': 20, 'y': 380, 'size': 40},
    2: {'x': 740, 'y': 380, 'size': 40},
    3: {'x': 380, 'y': 20, 'size': 40},
}


class CommonSend:
    def __init__(self):
        self.common_send = ''


class Bullet:
    def __init__(self, belone_to, direction, pos, b_type):
        self.belone_to = belone_to
        self.type = b_type
        self.speed = 10 + self.type*10
        self.direction = direction
        self.operation_handel = {
            'direction': {
                87: [0, -self.speed],
                83: [0, self.speed],
                65: [-self.speed, 0],
                68: [self.speed, 0],
            }
        }
        self.postion = {
            'x': pos['x'],
            'y': pos['y'],
            'size': self.type*10,
        }
        # self.direction = self.getDirection(direction)

    # def getDirection(self, direction):
    #     temp = []
    #     for(k, v) in direction.items():
    #         if v:
    #             temp[0] += self.operation_handel['direction'][int(k)][0]
    #             temp[1] += self.operation_handel['direction'][int(k)][1]
    #     return temp

    def getPositon(self):
        return {
            'x': self.postion['x'],
            'y': self.postion['y'],
            'type': self.type,
            'speed': self.speed,
            'direction': self.direction,
            'size': self.postion['size'],
            'belone_to': self.belone_to,
        }


class TankHandler(WebSocketHandler):

    users = []         # 用来存放在线用户的容器
    players = []       # 存放用户信息的容器
    mes = BaseData()
    id = ''
    bullets_type = 1
    speed = 10
    isRoomer = 0  # 是否房主
    name = ''  # 名字
    pos = {}  # 位置,大小
    common = 0
    direction = ''  # 方向
    operation_handel = {
        'direction': {
            87: [0, -speed],
            83: [0, speed],
            65: [-speed, 0],
            68: [speed, 0],
        }
    }

    def checkCrash(self, key_evt):
        allow_move = True
        if key_evt['87']:
            move_y = self.pos['y']+self.operation_handel['direction'][87][1]
            if move_y <= 0:
                allow_move = False
            else:
                for u in self.users:
                    if not self.name == u.name:
                        if ((u.pos['y'] <= move_y <= u.pos['y']+u.pos['size'])and (u.pos['x'] <= self.pos['x'] <= u.pos['x']+u.pos['size'])):
                            allow_move = False
                        else:
                            # allow_move = False
                            pass
            if allow_move:
                self.pos['y'] = move_y

        if key_evt['83']:
            move_y = self.pos['y']+self.operation_handel['direction'][83][1]
            if move_y+self.pos['size'] >= 800:
                allow_move = False
            else:
                for u in self.users:
                    if not self.name == u.name:
                        if ((u.pos['y'] <= move_y+self.pos['size'] <= u.pos['y']+u.pos['size'])and(
                            u.pos['x'] <= self.pos['x'] +
                                self.pos['size'] <= u.pos['x']+u.pos['size']
                        )):
                            allow_move = False
                        else:
                            # allow_move = False
                            pass
                            # self.pos['y'] = move_y
            if allow_move:
                self.pos['y'] = move_y

        if key_evt['65']:
            move_x = self.pos['x'] + self.operation_handel['direction'][65][0]
            if move_x <= 0:
                allow_move = False
            else:
                for u in self.users:
                    if not self.name == u.name:
                        if ((u.pos['x'] <= move_x <= u.pos['x']+u.pos['size'])and(
                            u.pos['y'] <= self.pos['y'] <= u.pos['y'] +
                                u.pos['size']
                        )):
                            allow_move = False
                        else:
                            pass
            if allow_move:
                self.pos['x'] = move_x
                # self.pos['x'] = move_x
            # self.pos['x'] += self.operation_handel['direction'][65][0]
        if key_evt['68']:
            move_x = self.pos['x'] + self.operation_handel['direction'][68][0]
            if move_x+self.pos['size'] >= 800:
                allow_move = False
            else:
                for u in self.users:
                    if not self.name == u.name:
                        if ((u.pos['x'] <= move_x+self.pos['size'] <= u.pos['x']+u.pos['size'])and(
                            u.pos['y'] <= self.pos['y'] <= u.pos['y']+u.pos['size']
                        )):
                            allow_move = False
                        else:
                            pass
                            # self.pos['x'] = move_x
            if allow_move:
                self.pos['x'] = move_x
            # self.pos['x'] += self.operation_handel['direction'][68][0]

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
        global all_bullet
        # self.mes.setType(2)
        for each in all_bullet:
            if(len(each['direction']) > 0):
                each['y'] += each['speed']*each['direction'][1]
                each['x'] += each['speed']*each['direction'][0]
                if each['y'] > 800 or each['y'] < 0 or each['x'] > 800 or each['x'] < 0:
                    all_bullet.remove(each)
        # self.mes.setMes(
        #     {'bullets': all_bullet, 'numbers': self.getPlayerInfo()})
        # for u in self.users:  # 向在线用户广播消息
        #     u.write_message(json.dumps(self.mes.getData()).encode())

    def set_interval(self, func, sec):
        def func_wrapper():
            self.set_interval(func, sec)
            func()
        t = Timer(sec, func_wrapper)
        t.start()
        return t

    def open(self):
        global common_send_sign
        nums = len(self.users)
        if nums < 4:
            self.isRoomer = 1 if nums == 0 else 0
            self.name = get_name()
            self.pos = init_position[nums]
            self.users.append(self)
            self.id = self.users.index(self)
            self.mes.setType(2)
            for u in self.users:
                send_mes = {
                    'name': u.name,
                    'isRoomer': u.isRoomer,
                    'id': self.id,
                    'numbers': self.getPlayerInfo(),
                    'bullets': all_bullet,
                }
                self.mes.setMes(send_mes)
                u.write_message(json.dumps(self.mes.getData()).encode())
        else:
            self.mes.setType(4)
            self.mes.setMes({'info': '房间人数已满'})
            self.write_message(json.dumps(self.mes.getData()).encode())
            self.close()
        if not isinstance(common_send_sign, CommonSend):
            common_send_sign = CommonSend()
            common_send_sign.common_send = self.set_interval(
                self.sendBullets, 0.06)

    def on_message(self, message):
        global all_bullet
        msg = json.loads(message)
        if msg['key'] != 32:
            self.direction = msg['direction']
            self.checkCrash(msg['key'])
            self.mes.setType(2)
            players = self.getPlayerInfo()
            send_mes = {
                'numbers': players,
                'bullets': all_bullet,
            }
            self.mes.setMes(send_mes)
            for u in self.users:
                u.write_message(json.dumps(self.mes.getData()).encode())
        else:
            self.bullet = Bullet(self.id, self.direction,
                                 self.pos, self.bullets_type)
            position = self.bullet.getPositon()
            all_bullet.append(position)
            self.mes.setType(99)
            send_mes = {
                'bullets': position,
            }
            self.mes.setMes(send_mes)
            for u in self.users:
                u.write_message(json.dumps(self.mes.getData()).encode())

    def on_close(self):
        if self in self.users:
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
