from tornado.websocket import WebSocketHandler
import json
from tools.tools import get_name
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
