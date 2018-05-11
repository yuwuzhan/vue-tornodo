from games import ChatHandler, tankHandler
urls = [
    (r"/ws", ChatHandler),
    (r"/tank", tankHandler), ]
