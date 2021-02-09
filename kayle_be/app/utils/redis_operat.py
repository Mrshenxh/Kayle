# redis相关的一些操作

import re
import redis
import json
from app import MCelery
from flask import current_app
from app import app

from ..models.history_plan_model import *
from ..models.temp_interface_model import CoreInterface


class RedisOperator():
    def __init__(self):
        self.client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get_string_data(self, search_str: str):
        return self.client.get(search_str)

    def set_string_data(self, key_str: str, value_str: str):
        return self.client.set(key_str, value_str)

    def set_more_string(self, more_str: dict):
        return self.client.mset(more_str)

    def get_more_string(self, more_str: list):
        return self.client.mget(more_str)

    def delete_data(self, delete_str: str):
        return self.client.delete(delete_str)

    def set_hash_data(self, hash_name: str, hash_key: str, hash_value: str):
        return self.client.hset(hash_name, hash_key, hash_value)

    def get_hash_data(self, hash_name: str, hash_key: str):
        return self.client.hget(hash_name, hash_key)

    def get_hash_all(self, hash_name: str):
        return self.client.hgetall(hash_name)


# 将计划数据存储到redis里
@MCelery.task
def set_plan_data(plan_dic):
    redis_operator = RedisOperator()
    # 插入计划版本
    redis_operator.set_hash_data("plan_core", "clientVersion", plan_dic["clientVersion"])
    # 插入计划创建人
    redis_operator.set_hash_data("plan_core", "planUser", plan_dic["planUser"])
    redis_operator.set_hash_data("plan_core", "planUserId", plan_dic["planUserId"])
    # 插入计划开始时间
    redis_operator.set_hash_data("plan_core", "planStart", plan_dic["planStart"])
    # 插入计划结束时间
    redis_operator.set_hash_data("plan_core", "planEnd", plan_dic["planEnd"])
    # 插入接口初始覆盖率
    redis_operator.set_hash_data("plan_core", "coreRate", "0.0%")
    # fix db 无法查询的问题
    if not app is current_app:
        app.app_context().push()

    # 接下来插入最复杂的一块儿内容，接口数据
    total_core_list = []
    for each_business in plan_dic["planBusiness"]:
        total_core = CoreInterface.query.filter_by(content=each_business).all()
        if len(total_core) != 0:
            for each_core_data in total_core:
                each_core_dict = {"interface_id": each_core_data.interface_id,
                                  "interface_regular": each_core_data.interface_regular,
                                  "content": each_core_data.content, "interface_desc": each_core_data.interface_desc,
                                  "user_id": each_core_data.user_id,
                                  "user_name": each_core_data.user_name,
                                  "key": each_core_data.interface_id,
                                  "is_finished": False,
                                  "match_infomation":[],
                                  }
                total_core_list.append(each_core_dict)
    # 插入接口数据
    redis_operator.set_hash_data("plan_core", "coreData", json.dumps(total_core_list))
    # 插入未完成接口数据
    redis_operator.set_hash_data("plan_core", "unDoneCore", json.dumps(total_core_list))

    return "插入核心数据成功"


# 每个数据通过websocket上传之后，进行匹配，看是否命中
@MCelery.task
def match_valid_interface(inter_dict):
    # 查询是否已经存在plan_id
    redis_opera = RedisOperator()
    plan_result_id = redis_opera.get_string_data("plan_id")
    plan_core_data = redis_opera.get_hash_data("plan_core", "coreData")
    if plan_result_id is None or plan_core_data is None:
        return "当前无计划"

    # 查询计划版本是否匹配
    # inter_version: app版本，如6.70.0
    # inter_os: app os，如iOS，Android
    # inter_release: app系统，如14.3, 10
    # inter_brand: 手机厂商 如Apple，huawei
    # inter_uuid: 手机唯一ID 避免一个设备重复打点

    inter_version = ''
    inter_os = ''
    inter_release = ''
    inter_brand = ''
    # 先从 x-app-version 中取App版本，取不到则从 x-app-za 中拿，如果都没有就放弃此接口
    if "x-app-version" in inter_dict["req_header"].keys():
        inter_version = inter_dict["req_header"]["x-app-version"]

    if "x-app-za" in inter_dict["req_header"].keys():
        za_key_value = inter_dict["req_header"]["x-app-za"].split("&")
    elif "X-APP-ZA" in inter_dict["req_header"].keys():
        za_key_value = inter_dict["req_header"]["X-APP-ZA"].split("&")
    else:
        print("没有 x-app-za")
        return "没有 x-app-za"

    if "x-udid" in inter_dict["req_header"].keys():
        inter_uuid = inter_dict["req_header"]["x-udid"]
    elif "X-UDID" in inter_dict["req_header"].keys():
        inter_uuid = inter_dict["req_header"]["X-UDID"]
    else:
        print("没有 x-udid")
        return "没有 x-udid"

    for each_items in za_key_value:
        item_list = each_items.split("=")
        if item_list[0] == "OS" and len(item_list) >=2:
            inter_os = item_list[1]
        elif item_list[0] == "Release" and len(item_list) >=2:
            inter_release = item_list[1]
        elif item_list[0] == "Brand" and len(item_list) >=2:
            inter_brand = item_list[1]
        elif item_list[0] == "VersionName" and len(item_list) >=2:
            inter_version = item_list[1]

    # 遍历完成之后，查看数据是否齐全
    if inter_version == '' or inter_os == '' or inter_release == '' or inter_brand == '':
        print("数据不全;inter_version:{0};inter_os:{0};" \
               "inter_release:{0};inter_brand:{0};".format(inter_version, inter_os, inter_release, inter_brand))
        return "数据不全;inter_version:{0};inter_os:{0};" \
               "inter_release:{0};inter_brand:{0};".format(inter_version, inter_os, inter_release, inter_brand)

    plan_version = redis_opera.get_hash_data("plan_core", "clientVersion").decode()
    # 如果包含所选版本，则匹配成功，否则跳出
    if plan_version not in inter_version:
        print("版本不一致 plan_version:{0};inter_version: {1};".format(plan_version, inter_version))
        return "版本不一致 plan_version:{0};inter_version: {1};".format(plan_version, inter_version)

    # 继续匹配 url
    inter_url = inter_dict["req_url"]
    inter_userid = inter_dict["user_id"]
    core_data_list = json.loads(plan_core_data.decode())
    match_id = ''
    for each_items in core_data_list:
        pattern = re.compile(r'{0}'.format(each_items["interface_regular"]))  # 查找数字
        match_result = pattern.findall(inter_url)
        if len(match_result) == 1 and match_result[0] == inter_url:
            match_id = each_items["interface_id"]

            # 避免重复添加
            if len(each_items["match_infomation"]) != 0:
                for each_matched in each_items["match_infomation"]:
                    if inter_uuid == each_matched["inter_uuid"]:
                        return "此设备已经添加过: {0}".format(inter_uuid)

            each_items["match_infomation"].append(
                {
                    "inter_version": inter_version,
                    "inter_os": inter_os,
                    "inter_release": inter_release,
                    "inter_brand": inter_brand,
                    "inter_uuid": inter_uuid,
                    "inter_userid": inter_userid,
                }
            )
            each_items["is_finished"] = True
            break

    if match_id == '':
        print("match_id为空 {0}".format(inter_url))
        return "match_id为空 {0}".format(inter_url)

    # 写入成功之后，将unDoneCore的数据也做更改
    undone_core_data = redis_opera.get_hash_data("plan_core", "unDoneCore")
    undone_core_list = json.loads(undone_core_data.decode())

    for each_items in undone_core_list:
        if each_items["interface_id"] == match_id:
            undone_core_list.remove(each_items)
            break
    # 重新计算覆盖率
    float_Rate = float(len(core_data_list)-len(undone_core_list))/float(len(core_data_list))
    core_rate = float_Rate * 100
    core_rate = '%.2f' % core_rate

    # 将修改后的coreData以及unDoneCore 重写入redis
    redis_opera.set_hash_data("plan_core", "coreData", json.dumps(core_data_list))
    redis_opera.set_hash_data("plan_core", "unDoneCore", json.dumps(undone_core_list))
    # 插入接口初始覆盖率
    redis_opera.set_hash_data("plan_core", "coreRate", "{0}%".format(core_rate))

    return "状态修改成功 {0}".format(inter_url)

# 结束任务时，自动把任务进行归档，存储到历史计划当中
def stop_plan_and_file():
    # 清除相关数据即可
    redis_opera = RedisOperator()
    try:
        db.session.add(PlanList(
            plan_userId=redis_opera.get_hash_data("plan_core", "planUserId").decode(),
            plan_user=redis_opera.get_hash_data("plan_core", "planUser").decode(),
            client_version=redis_opera.get_hash_data("plan_core", "clientVersion").decode(),
            plan_start=redis_opera.get_hash_data("plan_core", "planStart").decode(),
            plan_end=redis_opera.get_hash_data("plan_core", "planEnd").decode(),
            core_rate=redis_opera.get_hash_data("plan_core", "coreRate").decode(),
            core_data=redis_opera.get_hash_data("plan_core", "coreData").decode()
        ))
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    # 不管是否写入数据库，都将redis里数据清理
    redis_opera.delete_data("plan_id")
    redis_opera.delete_data("plan_core")

