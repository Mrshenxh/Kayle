
from flask import Blueprint
from ..utils.cron_jobs import *
from ..utils.usually_req import *
from flask import jsonify,make_response

operator = Blueprint('operator', __name__)

# 触发扫描计划是否结束
@operator.route("scanplan", methods=["GET"])
def scan_test_plan():
    scan_plan()
    response = make_response(jsonify(get_res_common_struct(400000, "成功操作计划扫描", {})), 200)
    response = set_req_header_fix_cross_domain(response, "GET")
    return response

# 触发扫描mitmproxy代理接口
@operator.route("scanmitm", methods=["GET"])
def scan_mitm():
    scan_mitmproxy(current_app)
    response = make_response(jsonify(get_res_common_struct(410000, "成功操作mitmproxy扫描", {})), 200)
    response = set_req_header_fix_cross_domain(response, "GET")
    return response