
# 定时任务脚本

import time
import requests

from app.utils.redis_operat import RedisOperator
from app.utils.usually_req import stop_mitm_proxy
from app import MCelery
from flask import current_app
from ..config.exts import db, user_socket_dict

from ..models.temp_interface_model import TempUserPort

class TimeCheck():
    '''
    时间戳比较类，如果是未来时间返回True，否则返回Fasle
    '''
    def return_is_feature(self, time_sj):
        # 定义格式
        data_sj = time.strptime(time_sj, "%Y-%m-%d %H:%M:%S")
        time_int = int(time.mktime(data_sj))
        # 当前时间戳
        now_time = int(time.time())
        if time_int > now_time:
            return True
        return False

@MCelery.task
def scan_plan():
    redis_opera = RedisOperator()
    plan_result_id = redis_opera.get_string_data("plan_id")
    if plan_result_id is None:
        print("没有进行中的计划，计划扫描结束")
        return
    try:
        plan_end = redis_opera.get_hash_data("plan_core", "planEnd").decode()
        is_feature = TimeCheck().return_is_feature(plan_end)
        if is_feature:
            print("将来时间，无需关闭计划")
            return
        stop_url = "http://0.0.0.0:3334/plan/stopplan"
        stop_response = requests.post(url=stop_url).json()
        print(stop_response["msg"])
    except Exception as e:
        print("计划扫描时遇到异常：")
        print(e)
        return

@MCelery.task
def scan_mitmproxy(app):
    # fix db 无法查询的问题
    if not app is current_app:
        app.app_context().push()
    # 获取所有正在使用的mitmproxy
    temp_port_list = TempUserPort.query.all()
    if len(temp_port_list) == 0:
        print("没有在进行中的代理")
        return
    mitm_needclose_list = []
    for each_mitm in temp_port_list:
        is_feture = TimeCheck().return_is_feature(each_mitm.expire_time)
        if not is_feture:
            mitm_needclose_list.append(each_mitm)

    for each_needclose in mitm_needclose_list:
        try:
            stop_mitm_proxy(port=each_needclose.port, mitm_id=each_needclose.mitm_id)
            print("I am in scan_mitmproxy")
            print(user_socket_dict)
            if each_needclose.mitm_id in user_socket_dict.keys():
                user_socket_dict.pop(each_needclose.mitm_id)
            if each_needclose.user_id in user_socket_dict.keys():
                user_socket_dict.pop(each_needclose.user_id)
            db.session.delete(each_needclose)
            db.session.commit()
            print("停用端口成功:{0}".format(each_needclose.port))
        except Exception as e:
            print("停用端口失败:{0}".format(e))
            db.session.rollback()

# redis_opera = RedisOperator()
# aa = redis_opera.get_hash_data("plan_core", "planStart").decode()
# print(TimeCheck().return_is_feature(aa))
# print(aa)
# print(time.time())#获当前时间的时间戳

