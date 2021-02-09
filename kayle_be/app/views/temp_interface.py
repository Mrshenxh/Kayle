
import string, random, demjson
from flask import Blueprint
from flask import request, jsonify
from flask_login import current_user
from flask_login import login_required

from ..utils.usually_req import *
from ..models.temp_interface_model import *
from ..models.user_model import *
from ..config.exts import user_socket_dict
from ..utils.redis_operat import *

tempinter = Blueprint('tempinter', __name__)

# 查询对应mitmproxy端口信息数据(给脚本使用，无需登录)
@tempinter.route("/queryportmsg", methods=["GET", "POST"])
def query_port_message():
    if request.method == 'POST' and request.values.get("port"):
        tempUserPort = query_user_by_port(request.values.get("port"))
        if tempUserPort is not None:
            json_dic = {
                "port": tempUserPort.port,
                "host_list": tempUserPort.host_list,
                "user_id": tempUserPort.user_id,
                "expire_time": tempUserPort.expire_time,
                "mitm_id": tempUserPort.mitm_id,
            }
            response = make_response(jsonify(get_res_common_struct(220000, "查询mitm端口成功", json_dic)), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
        response = make_response(jsonify(get_res_common_struct(220002, "没有找到指定端口数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    response = make_response(jsonify(get_res_common_struct(220001, "查询mitmproxy接口方式/参数不对", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response

# 根据use_id查询对应端口信息数据(给前端使用，校验登录状态)
@tempinter.route("/queryusersocket", methods=["GET", "POST"])
@login_required
def query_message_by_userid():
    if request.method != 'POST':
        response = make_response(jsonify(get_res_common_struct(230001, "查询mitmproxy接口方式/参数不对", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    tempUserPort = query_tempuser_by_user_id(current_user.user_id)
    if tempUserPort is not None:
        json_dic = {
            "port": tempUserPort.port,
            "host_list": tempUserPort.host_list,
            "user_id": tempUserPort.user_id,
            "expire_time": tempUserPort.expire_time,
            "mitm_id": tempUserPort.mitm_id,
        }
        response = make_response(jsonify(get_res_common_struct(230000, "查询mitm端口成功", json_dic)), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    response = make_response(jsonify(get_res_common_struct(230002, "没有找到指定端口数据", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response


# 核心接口数据上传
@tempinter.route("/uploadcoreinter", methods=["GET", "POST"])
@login_required
def upload_tempinter():
    if request.method == 'POST' and request.get_json(force=True):
        resJson = request.get_json(force=True)
        print(resJson)
        # 先判断是否已经存在此接口
        interface_data = query_interface_by_regular(resJson["interfaceRegular"])
        if interface_data is not None:
            response = make_response(jsonify(get_res_common_struct(200003, "此接口已上传过，如要编辑请前往核心接口列表", {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response

        interface_id = ''
        # 为每个核心接口生成对应的 interface_id
        is_repeat = True
        while is_repeat:
            seeds = string.digits
            random_str = random.choices(seeds, k=12)
            print("".join(random_str))
            interface_id = "".join(random_str)
            tempinterface = query_user_by_interface_id(interface_id)
            if tempinterface is None:
                is_repeat = False
        # 查询用户 username 查不到就抛错，前端需要容错
        user_data = query_user_by_user_id(resJson["userId"])
        if user_data is None:
            response = make_response(jsonify(get_res_common_struct(200004, "核心接口数据导入失败，非有效用户", {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
        try:
            db.session.add(CoreInterface(
                interface_id=interface_id,
                interface_path=str(resJson["interfacePath"]),
                req_header=demjson.encode(resJson["requestHeader"]),
                user_id=str(resJson["userId"]),
                user_name=user_data.nick_name,
                req_data=demjson.encode(resJson["requestData"]),
                req_query=demjson.encode(resJson["requestQuery"]),
                req_form=demjson.encode(resJson["requestForm"]),
                req_method=str(resJson["requestMethod"]),
                req_scheme=str(resJson["requestScheme"]),
                req_start=str(resJson["reqStart"]),
                req_end=str(resJson["reqEnd"]),
                req_cookie=demjson.encode(resJson["requestCookie"]),
                res_header=demjson.encode(resJson["responseHeader"]),
                res_status_code=int(resJson["responseStatus"]),
                res_cookie=demjson.encode(resJson["responseCookie"]),
                res_text=demjson.encode(resJson["responseData"]),
                res_start=str(resJson["resStart"]),
                res_end=str(resJson["resEnd"]),
                exprie_time=str(resJson["expireTime"]),
                mitm_id=str(resJson["mitmId"]),
                content=str(resJson["belongBusiness"]),
                interface_regular=str(resJson["interfaceRegular"]),
                interface_desc=str(resJson["interfaceDesc"]),
            ))
            db.session.commit()

            response = make_response(jsonify(get_res_common_struct(200000, "核心接口数据导入成功", {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify(get_res_common_struct(200002, "核心接口数据导入失败:{}".format(e), {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
    else:
        response = make_response(jsonify(get_res_common_struct(200001, "核心接口请求方式/数据格式不正确", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response

@tempinter.route("/createmitm", methods=["GET","POST"])
@login_required
def create_mitmproxy_port():
    '''
    开启一个mitmproxy服务
    :return:
    '''
    if request.method != "POST" or not request.get_json(force=True):
        response = make_response(jsonify(get_res_common_struct(210001, "添加mitmproxy请求方式/数据格式不正确", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    resJson = request.get_json(force=True)
    print("i am in createmitm...")
    print(resJson)
    host_list = resJson["host_list"]
    mitm_id = ''
    is_repeat = True
    while is_repeat:
        seeds = string.digits
        random_str = random.choices(seeds, k=6)
        print("".join(random_str))
        mitm_id = "".join(random_str)
        tempinterface = query_user_by_mitm_id(mitm_id)
        if tempinterface is None:
            is_repeat = False
    user_id = current_user.user_id
    expire_time = resJson["expire_time"]
    port = resJson["port"]

    real_port = create_mitm_proxy(port, mitm_id)
    try:
        db.session.add(TempUserPort(
            port=real_port,
            host_list=host_list,
            mitm_id=mitm_id,
            user_id=user_id,
            expire_time=expire_time
        ))
        db.session.commit()
        json_dic = {
            "port": real_port,
            "mitm_id": mitm_id,
            "host_list": host_list,
            "expire_time": expire_time,
            "user_id": user_id
        }
        if real_port == port:
            response = make_response(jsonify(get_res_common_struct(210002, "添加mitmproxy成功,端口{0}".format(real_port), json_dic)), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response

        response = make_response(jsonify(get_res_common_struct(210003, "{0}端口被占用,已经为您添加新的端口{1}".format(port, real_port), json_dic)), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    except Exception as e:
        db.session.rollback()
        response = make_response(
            jsonify(get_res_common_struct(210004, "数据库操作错误: {0}".format(e), {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response

@tempinter.route("/stopmitm", methods=["GET", "POST"])
@login_required
def stop_mitmproxy_port():
    if request.method != "POST":
        response = make_response(jsonify(get_res_common_struct(220001, "请求方式不对，无法停掉mitmproxy", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    temp_user_port = query_tempuser_by_user_id(current_user.user_id)
    if temp_user_port:
        # 停端口，删库,需要把user_socket_dict对应的数据清理掉
        stop_mitm_proxy(port=temp_user_port.port, mitm_id=temp_user_port.mitm_id)
        try:
            if temp_user_port.mitm_id in user_socket_dict.keys():
                user_socket_dict.pop(temp_user_port.mitm_id)
            if current_user.user_id in user_socket_dict.keys():
                user_socket_dict.pop(current_user.user_id)

            db.session.delete(temp_user_port)
            db.session.commit()
            response = make_response(jsonify(get_res_common_struct(220000, "mitmproxy停用成功", {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify(get_res_common_struct(220003, "数据库操作失败: {0}".format(e), {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
    response = make_response(jsonify(get_res_common_struct(220002, "当前用户没有可以停用的mitmproxy服务", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response

# 开辟socket服务校验端口
@tempinter.route("/tempsocket/flow/<userid>")
def temp_interface_socket_flow(userid):
    print(request.environ)
    user_socket = request.environ.get("wsgi.websocket")
    print("request", request)
    print("user_socket", user_socket)
    if user_socket:
        user_socket_dict[userid] = user_socket
        print(user_socket_dict)
        msg = user_socket.receive()
        print(msg)
        try:
            msg_dict = demjson.decode(msg)
            msg_dict['from_port'] = userid
            # 将匹配规则放到任务队列
            match_valid_interface(msg_dict)
            to_user = msg_dict.get('user_id')
            u_socket = user_socket_dict.get(to_user)
            u_socket.send(demjson.encode(msg_dict))
        except Exception as e:
            print(e)
        return "返回成功"
    return "初始化socket失败"

# 分页下发核心接口数据
@tempinter.route("/getcoreinter", methods=["GET", "POST"])
@login_required
def get_core_interface():
    if request.method != "GET":
        response = make_response(jsonify(get_res_common_struct(230001, "请求方式不对，无法获取核心接口数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response
    if "pageid" not in list(request.args.keys()):
        response = make_response(jsonify(get_res_common_struct(230002, "缺少必要参数pageid，无法获取相应数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response
    page_id = int(request.args["pageid"])

    if "urlcontent" in list(request.args.keys()) and "belongBusiness" in list(request.args.keys()):
        page_data = CoreInterface.query.filter(CoreInterface.interface_path.contains(request.args["urlcontent"]))\
            .filter(CoreInterface.content == request.args["belongBusiness"])\
            .order_by(CoreInterface.interface_path.asc()).paginate(page=page_id, per_page=10)
    elif "urlcontent" in list(request.args.keys()) and "belongBusiness" not in list(request.args.keys()):
        page_data = CoreInterface.query.filter(CoreInterface.interface_path.contains(request.args["urlcontent"]))\
            .order_by(CoreInterface.interface_path.asc()).paginate(page=page_id, per_page=10)
    elif "urlcontent" not in list(request.args.keys()) and "belongBusiness" in list(request.args.keys()):
        page_data = CoreInterface.query.filter(CoreInterface.content == request.args["belongBusiness"]) \
            .order_by(CoreInterface.interface_path.asc()).paginate(page=page_id, per_page=10)
    else:
        page_data = CoreInterface.query.order_by(CoreInterface.interface_path.asc()).paginate(page=page_id, per_page=10)
    print(page_data.items)
    print(page_data.pages)
    core_interface_list = []
    for each_inter in page_data.items:
        each_core_interface = {}
        each_core_interface['interfacePath'] = each_inter.interface_path
        each_core_interface['interfaceId'] = each_inter.interface_id
        each_core_interface['userId'] = each_inter.user_id
        each_core_interface['userName'] = each_inter.user_name
        each_core_interface['requestMethod'] = each_inter.req_method
        each_core_interface['content'] = each_inter.content
        each_core_interface['key'] = each_inter.interface_id
        each_core_interface['interfaceRegular'] = each_inter.interface_regular
        each_core_interface['interfaceDesc'] = each_inter.interface_desc
        core_interface_list.append(each_core_interface)
    response = make_response(jsonify(get_res_common_struct(230003, "核心接口数据请求成功", {"data": core_interface_list, "totolPage": page_data.pages})), 200)
    response = set_req_header_fix_cross_domain(response, "GET")
    return response

# 根据interface_id查询接口详细信息
@tempinter.route("/searchcore", methods=["GET", "POST"])
@login_required
def search_by_interface_id():
    if request.method != "GET":
        response = make_response(jsonify(get_res_common_struct(240001, "请求方式不对，无法获取相应接口数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response
    if "interfaceid" not in list(request.args.keys()):
        response = make_response(jsonify(get_res_common_struct(240002, "缺少必要参数interfaceid，无法获取相应数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response
    interface_id = request.args["interfaceid"]
    interface_data = query_user_by_interface_id(interface_id)
    if interface_data:
        each_core_interface = {}
        each_core_interface['interfacePath'] = interface_data.interface_path
        each_core_interface['interfaceId'] = interface_data.interface_id
        each_core_interface['requestHeader'] = interface_data.req_header
        each_core_interface['userId'] = interface_data.user_id
        each_core_interface['userName'] = interface_data.user_name
        each_core_interface['requestData'] = interface_data.req_data
        each_core_interface['requestMethod'] = interface_data.req_method
        each_core_interface['requestScheme'] = interface_data.req_scheme
        each_core_interface['requestCookie'] = interface_data.req_cookie
        each_core_interface['responseHeader'] = interface_data.res_header
        each_core_interface['responseStatusCode'] = interface_data.res_status_code
        each_core_interface['responseCookie'] = interface_data.res_cookie
        each_core_interface['responseData'] = interface_data.res_text
        each_core_interface['content'] = interface_data.content
        each_core_interface['key'] = interface_data.interface_id
        each_core_interface['interfaceRegular'] = interface_data.interface_regular
        each_core_interface['interfaceDesc'] = interface_data.interface_desc
        response = make_response(jsonify(get_res_common_struct(240000, "查询成功", each_core_interface)), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response
    response = make_response(jsonify(get_res_common_struct(240003, "没有查询到此interfaceid对应的接口数据", {})), 200)
    response = set_req_header_fix_cross_domain(response, "GET")
    return response

# 根据interface_id删除接口数据
@tempinter.route("/deletecore", methods=["GET", "POST"])
@login_required
def search_core_by_interface_id():
    if request.method != "POST":
        response = make_response(jsonify(get_res_common_struct(250001, "请求方式不对，无法获取相应接口数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    resJson = request.get_json(force=True)
    if "interfaceId" not in resJson.keys():
        response = make_response(jsonify(get_res_common_struct(250002, "请求数据不对，没有携带interfaceId", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    interface_data = query_user_by_interface_id(resJson["interfaceId"])
    if interface_data:
        try:
            db.session.delete(interface_data)
            db.session.commit()
            response = make_response(jsonify(get_res_common_struct(250000, "接口删除成功", {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify(get_res_common_struct(250004, "数据库操作失败:{0}".format(e), {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
    response = make_response(jsonify(get_res_common_struct(250003, "没有查询到此interfaceid对应的接口数据", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response

# 核心接口数据二次编辑
@tempinter.route("/editcore", methods=["GET", "POST"])
@login_required
def edit_core_by_interface_id():
    if request.method != "POST":
        response = make_response(jsonify(get_res_common_struct(260001, "请求方式不对，无法获取相应接口数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    resJson = request.get_json(force=True)
    if "interfaceId" not in resJson.keys():
        response = make_response(jsonify(get_res_common_struct(260002, "请求数据不对，没有携带interfaceId", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    interface_data = query_user_by_interface_id(resJson["interfaceId"])
    if interface_data:
        try:
            interface_data.interface_id = resJson["interfaceId"]
            interface_data.interface_path = str(resJson["interfacePath"])
            interface_data.user_id = str(current_user.user_id)
            interface_data.user_name = str(current_user.nick_name)
            # interface_data.req_header = str(resJson["requestHeader"])
            # interface_data.req_data = str(resJson["requestData"])
            # interface_data.req_method = str(resJson["requestMethod"])
            # interface_data.req_scheme = str(resJson["requestScheme"])
            # interface_data.req_start = str(resJson["reqStart"])
            # interface_data.req_end = str(resJson["reqEnd"])
            # interface_data.req_cookie = str(resJson["requestCookie"])
            # interface_data.res_header = str(resJson["responseHeader"])
            # interface_data.res_status_code = int(resJson["responseStatus"])
            # interface_data.res_cookie = str(resJson["responseCookie"])
            # interface_data.res_text = str(resJson["responseData"])
            # interface_data.res_start = str(resJson["resStart"])
            # interface_data.res_end = str(resJson["resEnd"])
            # interface_data.exprie_time = str(resJson["expireTime"])
            # interface_data.mitm_id = str(resJson["mitmId"])
            interface_data.content = str(resJson["belongBusiness"])
            interface_data.interface_regular = str(resJson["interfaceRegular"])
            interface_data.interface_desc = str(resJson["interfaceDesc"])
            db.session.commit()
            response = make_response(jsonify(get_res_common_struct(260000, "接口数据更新成功", {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify(get_res_common_struct(260003, "接口更新失败: {0}".format(e), {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
    response = make_response(jsonify(get_res_common_struct(260001, "更新失败，没有查到此interfaceId对应的接口信息", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response