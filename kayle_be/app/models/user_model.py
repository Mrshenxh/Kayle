
from flask_login import UserMixin
from ..config.exts import db

# 通过用户名,获取用户记录,如果不存在,返回None
def query_user(username):
    print(username)
    users = UserList.query.filter_by(username=username).all()
    if len(users) != 0:
        return users[0]
    return None

# 通过用户id，获取用户记录，如果不存在，返回None
def query_user_by_user_id(user_id):
    print(user_id)
    users = UserList.query.filter_by(user_id=user_id).all()
    if len(users) != 0:
        return users[0]
    return None

# 创建ORM映射
class UserList(db.Model):
    __tablename__ = 'user_list'
    user_id = db.Column(db.String(20), primary_key=True, nullable=False)
    username = db.Column(db.String(20))
    passward = db.Column(db.String(20))
    nick_name = db.Column(db.String(20))

class User(UserMixin):

    def __init__(self, user):
        self.user_id = user.user_id
        self.username = user.username
        self.password = user.passward
        self.nick_name = user.nick_name

    def get_id(self):
        """获取用户ID"""
        return self.user_id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        users = UserList.query.filter_by(user_id=user_id).all()
        if len(users) != 0:
            return User(users[0])
        return None

