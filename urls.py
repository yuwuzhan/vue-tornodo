from games import ChatHandler
from game.tank import TankHandler
urls = [
    (r"/ws", ChatHandler),
    (r"/tank", TankHandler), ]
