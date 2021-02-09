
import os
import socket

from flask import make_response

def set_req_header_fix_cross_domain(response:make_response, req_method:str):
    # 设置响应请求头,解决跨域问题
    # response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Allow-Methods"] = req_method
    response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"

    return response

def get_res_common_struct(code:int, msg:str, data):
    # 设置返回数据结构体
    common_struct = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return common_struct

def create_mitm_proxy(port, mitm_id):
    while check_port_is_use(port):
        port = str(int(port) + 1)
    run_mitm_server(port, mitm_id)
    return port

def stop_mitm_proxy(port, mitm_id):
    if check_port_is_use(port):
        killport(port)
        clear_static_file(mitm_id)
        return "端口已经被清除"
    else:
        return "端口并未使用"

# 查看某个端口是否被占用
def check_port_is_use(port, ip='0.0.0.0'):
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        normal_socket.connect((ip, int(port)))
        normal_socket.shutdown(2)
        print('sorry, %s:%s is used' % (ip, port))
        return True
    except Exception as e:
        print('ok %s:%s is unused' % (ip, port))
        print(e)
        return False

# 清除被占用端口号
def killport(port):
    '''root authority is required'''
    seach_read_line = os.popen("lsof -i:%s | awk '{print $2}'" % port).read()
    seach_read_list = seach_read_line.split("\n")
    for each_pid in seach_read_list:
        if each_pid and each_pid != '' and each_pid != "PID":
            os.system("kill -9 {0}".format(each_pid))

# 启动mitmproxy服务
def run_mitm_server(port, mitm_id):
    # 本地启动port
    mitm_command = "cd /Users/shenxh/Desktop/company/zhihu&&source " \
                   "QA_Tools_BE/venv/bin/activate&&nohup mitmdump -s QA_Tools_BE/app/utils/get_mitm_request.py" \
                   " -p {0} > QA_Tools_BE/app/statics/{1} 2>&1 &".format(port, mitm_id)
    import subprocess
    # mitm_command = "sudo -i&&cd /data/zhihu/shenxh&&source " \
    #                "venv/bin/activate&&nohup mitmdump -s kayle_be/app/utils/get_mitm_request.py" \
    #                " -p {0} > kayle_be/app/statics/{1} 2>&1 &".format(port, mitm_id)
    subprocess.call(mitm_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, executable="/bin/bash")

# 杀掉端口时，清除对应的statics文件
def clear_static_file(mitm_port):
    # 本地删除
    mitm_command = "rm -rf /Users/shenxh/Desktop/company/zhihu/QA_Tools_BE/app/statics/{0}".format(mitm_port)
    import subprocess
    # mitm_command = "sudo -i&&rm -rf /data/zhihu/shenxh/kayle_be/app/statics/{0}".format(mitm_port)
    subprocess.call(mitm_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, executable="/bin/bash")

# clear_static_file("281958")

# run_mitm_server("8090", "123457")
# killport("8089")

#
# import redis
# client = redis.StrictRedis(host='localhost', port=6379, db=0)
# age = client.get('plan_id')
# print(age.decode())   # 输出：100
# client_version = client.hget('plan_core', 'clientVersion')
# print(client_version.decode())
# client_all = client.hgetall("plan_core")
# print(client_all)
# import json
# aa = '''[{"cc": "dd"}, {"cc": "dd"}, {"cc": "dd"}]'''
# print(json.loads(aa))

# import demjson
# import json
# strs = '''
# [{'interface_id': '439510933471', 'interface_regular': 'https://api.zhihu.com/market/svip_note/paid_column/\\d{6,20}', 'content': 'Content', 'interface_desc': '进入文稿页，会员账号弹窗展示“亲爱的会员，你已畅享该会员内容”', 'user_id': '10000000', 'is_finished': False}, {'interface_id': '403969377552', 'interface_regular': 'https://api.zhihu.com/market/vip_recommend', 'content': 'Content', 'interface_desc': '市场首页榜单，换一换相关业务接口', 'user_id': '10000000', 'is_finished': False}, {'interface_id': '397757998591', 'interface_regular': 'https://api.zhihu.com/market/tab_header', 'content': 'Content', 'interface_desc': '市场首页Tab，banner，用户信息下发接口', 'user_id': '10000000', 'is_finished': False}]
# '''
#
# # dicts = demjson.decode(strs)
# # print(dicts)
#
# dictss = json.loads(strs)
# print(dictss)


# import re
# pattern = re.compile(r'https://api.zhihu.com/market/vip_recommend\?limit=\d{1,3}&offset=\d{1,5}')   # 查找数字
# result1 = pattern.findall('https://api.zhihu.com/market/vip_recommend?limit=3&offset=30')
# print(result1)

# print(round(float(3)/float(7), 4))


# from websocket import create_connection
# ws = create_connection("ws://10.101.1.51:3334/tempinter/tempsocket/flow/{0}".format('927087'))
# ws.send("{'sss':'ddd'}")
# print(ws.recv())
# ws.close()

from websocket import create_connection
import json
import time

aa = {
    "Cookie": "JSESSIONID=tracking-validation1i8dss9yk1gfh1i67xrv83a331.tracking-validation",
}

dd = ["CONNECT\naccept-version:1.1,1.0\nheart-beat:10000,10000\n\n\u0000"]

ee = ["SUBSCRIBE\nid:sub-0\ndestination:/topic/instance/1612159195674\n\n\u0000"]

def websocket(url, headers_dict=None, params_dict=None, result: list = None):
    """
    websocket请求
    :param url:
    :param headers_dict:
    :param params_dict:
    :param result: 请求结果列表
    """
    print('websocket请求url：{}'.format(url))
    # step1 创建连接
    while True:
        try:
            if headers_dict is not None:
                ws = create_connection(url, header=headers_dict)
            else:
                ws = create_connection(url)
            break
        except Exception as e:
            print('连接错误:{}'.format(e))
            time.sleep(5)
    print('请求是否成功：{}'.format('成功' if ws.status == 101 else '失败'))


    # ws.send(str(ee))

    # step2：请求/获取 响应
    while True:

        if params_dict is not None:
            params = params_dict
            ws.send(str(params))
        response = ws.recv()
        if response == "o":
            ws.send(json.dumps(dd))
        if 'heart-beat' in response:
            ws.send(json.dumps(ee))
        if result is not None:
            result.append(response)
        print(response)

# websocket(url="ws://tv.in.zhihu.com:80/api/v1/tracking/844/g1aughbn/websocket?instanceId=1612162048649", headers_dict=aa)



# ws = create_connection(url="ws://tv.in.zhihu.com:80/api/v1/tracking/844/g1aughbn/websocket?instanceId=1612162048649", header=aa)
#
# while True:
#     print(ws.recv())



