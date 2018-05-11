from tornado.websocket import WebSocketHandler
import json
from getname import get_name
from message import BaseData


class ChatHandler(WebSocketHandler):

    users = set()  # 用来存放在线用户的容器
    mes = BaseData()

    def open(self):
        self._temp_name = get_name()
        self.users.add(self)  # 建立连接后添加用户到容器中
        for u in self.users:  # 向已在线用户发送消息
            u.write_message(u"[%s]-[%s]-进入游戏室" %
                            (self.request.remote_ip,
                             self._temp_name))

    def on_message(self, message):
        for u in self.users:  # 向在线用户广播消息
            u.write_message(u"[%s]-[%s]-说：%s" %
                            (self.request.remote_ip,
                             self._temp_name,
                             message))

    def on_close(self):
        self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        for u in self.users:
            u.write_message(u"[%s]-[%s]-离开游戏室" %
                            (self.request.remote_ip,
                             self._temp_name))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


class TankHandler(WebSocketHandler):
    users = []          # 用来存放在线用户的容器
    players = []  # 存放用户信息的容器
    mes = BaseData()
    initPosition = {
        0: {'x': 380, 'y': 740, 'size': 40},
        1: {'x': 20, 'y': 380, 'size': 40},
        2: {'x': 740, 'y': 380, 'size': 40},
        3: {'x': 380, 'y': 20, 'size': 40},
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

    def changeSite(self):
        # TODO:changeSite

    def open(self):
        nums = len(self.users)
        if nums < 4:
            self.isRoomer = 1 if nums == 0 else 0
            self.name = get_name()
            self.pos = self.initPosition[nums]
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

    def on_message(self, message):
        for u in self.users:  # 向在线用户广播消息
            u.write_message(u'123')

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
