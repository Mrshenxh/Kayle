
import string, random

from flask import Blueprint
from flask import request, jsonify
from urllib.parse import urlparse, urljoin
from flask_login import login_user, login_required, logout_user, current_user

from ..models.user_model import *
from ..utils.usually_req import *

user = Blueprint('user', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# 登录接口
@user.route('/login', methods=['GET', 'POST'])
def login():
    # 假设通过数据库验证
    if request.method == 'POST' and request.get_json(force=True):
        resJson = request.get_json(force=True)
        print(resJson)
        username = resJson["username"]
        password = resJson["password"]
        # 验证表单,数据库
        user = query_user(username)
        if user and password == user.passward:
            # curr_user 是 User类的一个实例
            curr_user = User(user)
            curr_user.id = query_user(username).user_id
            # 通过 Flask-login的login_user来登录账户
            login_user(curr_user)
            nextD = request.args.get('next')
            print(nextD)
            # is_safe_url 用来检查url是否可以安全的重定向
            # 避免重定向攻击
            # if not is_safe_url(nextD):
            #     return abort(404)
            # return redirect(next or url_for('index'))
            # return redirect(url_for('user.index'))
            response = make_response(jsonify(get_res_common_struct(100000, "登录成功",{})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response

        response = make_response(jsonify(get_res_common_struct(100001, "账号或密码错误", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    else:
        response = make_response(jsonify(get_res_common_struct(100002, "登录请求方式/传输数据格式不正确", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response

# 注册接口
@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method != 'POST' or not request.get_json(force=True):
        response = make_response(jsonify(get_res_common_struct(110002, "注册请求方式/传输数据格式不正确", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    resJson = request.get_json(force=True)
    print(resJson)
    username = resJson["username"]
    password = resJson["password"]
    confirm = resJson["confirm"]
    nickname = resJson["nickname"]
    if password != confirm:
        response = make_response(jsonify(get_res_common_struct(110003, "注册前后密码不一致", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    user = query_user(username)
    if user:
        response = make_response(jsonify(get_res_common_struct(110004, "用户已存在", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response

    user_id = ''
    is_repeat = True
    while is_repeat:
        seeds = string.digits
        random_str = random.choices(seeds, k=8)
        print("".join(random_str))
        user_id = "".join(random_str)
        user = query_user_by_user_id(user_id)
        if user is None:
            is_repeat = False
    # 操作提交数据
    db.session.add(UserList(username=username, user_id=user_id, passward=password, nick_name=nickname))
    db.session.commit()

    new_user = query_user(username)
    if new_user:
        curr_user = User(new_user)
        curr_user.id = query_user(username).user_id
        # 通过 Flask-login的login_user来登录账户
        login_user(curr_user)
        response = make_response(jsonify(get_res_common_struct(110000, "注册成功", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    response = make_response(jsonify(get_res_common_struct(110005, "注册失败", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response


@user.route('/message', methods=['GET', 'POST'])
@login_required
def message():
    '''
    返回用户信息
    :return:
    '''
    print("hahaha")
    print(current_user.username)
    message_dict = {
        "username": current_user.username,
        "user_id": current_user.user_id,
        "nick_name": current_user.nick_name,
        "user_icon": "",
        "user_message": "",
    }
    response = make_response(jsonify(get_res_common_struct(120000, "用户信息获取成功", message_dict)), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response

# 验证是否登录成功
@user.route('/checklogin', methods=['GET', 'POST'])
@login_required
def personal():
    response = make_response(jsonify(get_res_common_struct(100004, "用户已经登录", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response

# 登出
@user.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    response = make_response(jsonify(get_res_common_struct(100003, "退出登录成功", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response

