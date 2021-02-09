from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 定义一个全局socket dict，存储用户和mitmproxy上传socket
user_socket_dict = {}