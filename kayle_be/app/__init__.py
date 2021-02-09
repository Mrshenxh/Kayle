
from flask import Flask
from celery import Celery
from .config import config

app = Flask(__name__)
app.config.from_object(config)

# print(app.name)
MCelery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
MCelery.conf.update(app.config)

from flask_login import LoginManager
from flask_cors import CORS
# https://www.cnblogs.com/franknihao/p/7202253.html uwsgi配置

from .models.user_model import *
from .config import exts
from .config.exts import db, user_socket_dict

CORS(app, supports_credentials=True)
db.init_app(app)

from .views.user import user
from .views.interface_case import intercase
from .views.temp_interface import tempinter
from .views.plan import plan
from .views.operator import operator

# 注册蓝图
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(intercase, url_prefix="/intercase")
app.register_blueprint(tempinter, url_prefix="/tempinter")
app.register_blueprint(plan, url_prefix="/plan")
app.register_blueprint(operator, url_prefix="/operator")

# 初始化login_manager
login_manager = LoginManager()
login_manager.init_app(app)
# 指定登录的URL
login_manager.login_view = 'user.login'

# login回调函数
@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    print(user_id)
    return User.get(user_id)

