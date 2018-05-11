from games import ChatHandler, TankHandler
urls = [
    (r"/ws", ChatHandler),
    (r"/tank", TankHandler), ]
