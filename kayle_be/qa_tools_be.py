

from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from geventwebsocket.websocket import WebSocket

from app import app

http_serv = WSGIServer(("0.0.0.0", 3334),app,handler_class=WebSocketHandler)

if __name__ == "__main__":
    http_serv.serve_forever()


