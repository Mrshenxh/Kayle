#!/usr/bin/env python
from gevent.pywsgi import WSGIServer as _WSGIServer
from geventwebsocket.handler import WebSocketHandler as _WSHandler
from geventwebsocket import *
def WsServer(*a,**kw): return _WSGIServer(*a, handler_class=_WSHandler, **kw)
def main():
    def echo_app(env, start):
        if env["PATH_INFO"] == '/echo':
            ws = env["wsgi.websocket"]
            msg = ws.receive()
            ws.send(msg)
            pass
        pass
    WsServer(("", 8000), echo_app).serve_forever()
if __name__ == '__main__': main()
