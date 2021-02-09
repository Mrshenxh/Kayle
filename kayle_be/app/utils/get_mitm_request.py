
import sys
import demjson
import requests
from websocket import create_connection
from mitmproxy import http

def parser_data(query):
    data = {}
    for key, value in query.items():
        data[key] = value
    return data

# 根据开辟端口号查询现有对应信息
def get_temp_interface(port):
    # get_user_url = "http://10.101.1.51:3334/tempinter/queryportmsg?port={0}".format(port)
    get_user_url = "http://0.0.0.0:3334/tempinter/queryportmsg?port={0}".format(port)
    response = requests.post(get_user_url).json()
    print(response)
    if response["code"] == 220000:
        print("请求成功")
        return response
    else:
        print("获取失败")
        return False

class GetMitmInterface:
    def __init__(self):
        self.host_list = None
        self.data_result = {}
        print("lululu")
        print(sys.argv)
        print(len(sys.argv))
        self.user_dict = None
        if len(sys.argv) >= 5 and sys.argv[3] == "-p":
            print("lelele")
            self.port = sys.argv[4]
            self.user_dict = get_temp_interface(self.port)["data"]
            self.host_list = self.user_dict["host_list"].split(",")
            print(self.host_list)

    def request(self, flow:http.HTTPFlow):
        print(self.host_list)
        print("I am request")
        print(flow.request.get_text())
        if self.host_list and flow.request.host in self.host_list:
            print(flow.request.url)
            self.data_result["req_url"] = flow.request.url
            self.data_result["req_method"] = flow.request.method
            self.data_result["req_header"] = {}
            for item in flow.request.headers:
                self.data_result['req_header'][item] = flow.request.headers[item]
            self.data_result['get_data'] = parser_data(flow.request.query)
            self.data_result['post_data'] = parser_data(flow.request.urlencoded_form)
            if flow.request.get_text() == '':
                self.data_result['json_text'] = {}
            else:
                self.data_result['json_text'] = demjson.decode(flow.request.get_text())
            self.data_result["req_scheme"] = flow.request.scheme
            self.data_result["req_start"] = flow.request.timestamp_start
            self.data_result["req_end"] = flow.request.timestamp_end
            self.data_result["req_cookie"] = {}
            for item in flow.request.cookies:
                self.data_result['req_cookie'][item] = flow.request.cookies[item]

    def response(self, flow:http.HTTPFlow):
        print("I am response")
        print(flow.response.get_content())
        if self.host_list and flow.request.host in self.host_list:
            self.data_result["res_start"] = flow.response.timestamp_start
            self.data_result["res_end"] = flow.response.timestamp_end
            self.data_result["res_status_code"] = flow.response.status_code
            self.data_result["res_header"] = {}
            for item in flow.response.headers:
                self.data_result['res_header'][item] = flow.response.headers[item]
            self.data_result["res_cookie"] = {}
            for item in flow.response.cookies:
                self.data_result['res_cookie'][item] = flow.response.cookies[item]
            try:
                self.data_result["res_text"] = demjson.decode(flow.response.get_content())
            except Exception as e:
                print("非json类型数据")
                print(e)
                self.data_result["res_text"] = flow.response.get_content()
            self.data_result["user_id"] = self.user_dict["user_id"]
            self.data_result["expire_time"] = self.user_dict["expire_time"]
            self.data_result["mitm_id"] = self.user_dict["mitm_id"]
            # 这个地方针对clientdisconnect的接口再做赋值
            if self.data_result["req_url"] != flow.request.url:
                self.data_result["req_url"] = flow.request.url
            print("打印所有数据")
            print(self.data_result)

            # ws = create_connection("ws://10.101.1.51:3334/tempinter/tempsocket/flow/{0}".format(self.data_result["mitm_id"]))
            ws = create_connection(
                "ws://0.0.0.0:3334/tempinter/tempsocket/flow/{0}".format(self.data_result["mitm_id"]))
            ws.send(demjson.encode(self.data_result))
            ws.close()

addons = [GetMitmInterface()]






