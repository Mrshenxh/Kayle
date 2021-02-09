
from flask import Blueprint, request
from app import MCelery
import time

intercase = Blueprint('intercase', __name__)
user_socket_list = []

@intercase.route("/my_socket")
def my_socket():
    user_socket = request.environ.get("wsgi.websocket")
    print("request", request)
    print("user_socket", user_socket)
    if user_socket:
        user_socket_list.append(user_socket)
        print(len(user_socket_list), user_socket_list)
    while True:
        msg = user_socket.receive()
        print(msg)
        for usocket in user_socket_list:
            try:
                usocket.send(msg)
            except :
                continue

@intercase.route("/hello", methods=["GET", "POST"])
def hello():
    print("haha")
    test_woker.apply_async(args=[10,20], countdown=2)
    return "hello, world!"

@MCelery.task
def test_woker(num1:int, num2:int):
    time.sleep(30)
    return num1 + num2


