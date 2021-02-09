
from flask import Blueprint
from flask import request, jsonify
from flask_login import current_user
from flask_login import login_required

from ..utils.usually_req import *
from ..utils.redis_operat import *
from ..models.user_model import *
from ..models.history_plan_model import *

plan = Blueprint('plan', __name__)

@plan.route("/createplan", methods=["GET", "POST"])
@login_required
def create_plan():
    if request.method != 'POST':
        response = make_response(jsonify(get_res_common_struct(300001, "创建测试计划接口方式/参数不对", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    resJson = request.get_json(force=True)
    print(resJson)
    user_one = query_user_by_user_id(current_user.user_id)
    resJson["planUser"] = user_one.nick_name
    resJson["planUserId"] = user_one.user_id
    core_result = set_plan_data.delay(resJson)
    RedisOperator().set_string_data("plan_id", str(core_result.id))
    response = make_response(jsonify(get_res_common_struct(300000, "创建测试计划成功，稍后可以刷新查看", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response

@plan.route("/stopplan", methods=["GET", "POST"])
# @login_required
def stop_plan():
    if request.method != 'POST':
        response = make_response(jsonify(get_res_common_struct(320001, "终止测试计划接口方式/参数不对", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    stop_plan_and_file()
    response = make_response(jsonify(get_res_common_struct(320000, "终止测试计划成功", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response

@plan.route("/queryplan", methods=["GET"])
@login_required
def query_plan():
    # 查询是否已经存在plan_id
    redis_opera = RedisOperator()
    plan_result_id = redis_opera.get_string_data("plan_id")
    if plan_result_id != None:
        print(plan_result_id)
        plan_content = MCelery.AsyncResult(id=plan_result_id.decode())
        if plan_content.status == 'SUCCESS':
            plan_json = {
                "clientVersion": redis_opera.get_hash_data("plan_core", "clientVersion").decode(),
                "planUser": redis_opera.get_hash_data("plan_core", "planUser").decode(),
                "planUserId": redis_opera.get_hash_data("plan_core", "planUserId").decode(),
                "planStart": redis_opera.get_hash_data("plan_core", "planStart").decode(),
                "planEnd": redis_opera.get_hash_data("plan_core", "planEnd").decode(),
                "coreRate": redis_opera.get_hash_data("plan_core", "coreRate").decode(),
            }
            response = make_response(jsonify(get_res_common_struct(310000, "查询成功", plan_json)), 200)
            response = set_req_header_fix_cross_domain(response, "GET")
            return response
        elif plan_content.status == 'FAILED':
            redis_opera = RedisOperator()
            redis_opera.delete_data("plan_id")
            redis_opera.delete_data("plan_core")

            response = make_response(jsonify(get_res_common_struct(310001, "创建失败，请稍后重试", {})), 200)
            response = set_req_header_fix_cross_domain(response, "GET")
            return response
        elif plan_content.status == 'STARTED':
            response = make_response(jsonify(get_res_common_struct(310002, "正在创建，请稍后查看", {})), 200)
            response = set_req_header_fix_cross_domain(response, "GET")
            return response
        elif plan_content.status == 'PENDING':
            response = make_response(jsonify(get_res_common_struct(310003, "任务还在等待，请稍后查看", {})), 200)
            response = set_req_header_fix_cross_domain(response, "GET")
            return response
    response = make_response(jsonify(get_res_common_struct(310004, "暂无已创建计划，请操作创建", {})), 200)
    response = set_req_header_fix_cross_domain(response, "GET")
    return response

@plan.route("/queryplancore", methods=["GET"])
@login_required
def query_planCore_url():
    redis_opera = RedisOperator()

    if "pageid" not in list(request.args.keys()):
        response = make_response(jsonify(get_res_common_struct(330001, "缺少必要参数pageid，无法获取相应数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response

    if "tabtype" not in list(request.args.keys()):
        response = make_response(jsonify(get_res_common_struct(330002, "缺少必要参数tabtype，无法获取相应数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response

    if redis_opera.get_hash_data("plan_core", "coreData") is None \
            or redis_opera.get_hash_data("plan_core", "unDoneCore") is None:
        response = make_response(jsonify(get_res_common_struct(330003, "查询数据为空", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response

    if request.args["tabtype"] == "coreData":
        data_list = json.loads(redis_opera.get_hash_data("plan_core", "coreData").decode())
    elif request.args["tabtype"] == "unDoneCore":
        data_list = json.loads(redis_opera.get_hash_data("plan_core", "unDoneCore").decode())
    else:
        response = make_response(jsonify(get_res_common_struct(330004, "不合法的查询类型", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response

    page_id = int(request.args["pageid"])
    if len(data_list) % 10 == 0:
        totalPages = int(len(data_list) / 10)
    else:
        totalPages = int(len(data_list)/10) + 1

    if page_id * 10 - len(data_list) >= 10:
        response = make_response(jsonify(get_res_common_struct(330007, "查询越界", {"data": [], "totalPages": totalPages})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response

    if "usersearch" in list(request.args.keys()):
        user_name = request.args["usersearch"]
        new_data_list = []
        for each_data in data_list:
            if each_data["user_name"] == user_name:
                new_data_list.append(each_data)

        if page_id * 10 - len(new_data_list) >= 10:
            response = make_response(
                jsonify(get_res_common_struct(330005, "查询越界", {"data": [], "totalPages": totalPages})), 200)
            response = set_req_header_fix_cross_domain(response, "GET")
            return response

        core_data_list = new_data_list[page_id * 10 - 10:page_id * 10]
        response = make_response(
            jsonify(get_res_common_struct(330006, "查询成功", {"data": core_data_list, "totalPages": totalPages})),
            200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response

    # 没有usersearch返回数据
    core_data_list = data_list[page_id * 10 - 10:page_id * 10]
    response = make_response(jsonify(get_res_common_struct(330000, "查询成功", {"data": core_data_list, "totalPages": totalPages})),
                             200)
    response = set_req_header_fix_cross_domain(response, "GET")
    return response

# 历史计划列表
@plan.route("/historyplan", methods=["GET"])
@login_required
def history_plan():
    if "pageid" not in list(request.args.keys()):
        response = make_response(jsonify(get_res_common_struct(340001, "缺少必要参数pageid，无法获取相应数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response
    page_id = int(request.args["pageid"])
    if "clientVersion" in list(request.args.keys()):
        page_data = PlanList.query.filter(PlanList.client_version == request.args["clientVersion"])\
            .order_by(PlanList.id.asc()).paginate(page=page_id, per_page=5)
    else:
        page_data = PlanList.query.order_by(PlanList.id.desc()).paginate(page=page_id, per_page=5)
    print(page_data.items)
    print(page_data.pages)
    history_plan_list = []
    for each_plan in page_data.items:
        each_history_plan = {}
        each_history_plan['clientVersion'] = each_plan.client_version
        each_history_plan['planUser'] = each_plan.plan_user
        each_history_plan['planUserId'] = each_plan.plan_userId
        each_history_plan['planStart'] = each_plan.plan_start
        each_history_plan['planEnd'] = each_plan.plan_end
        each_history_plan['coreRate'] = each_plan.core_rate
        each_history_plan['id'] = each_plan.id
        history_plan_list.append(each_history_plan)
    response = make_response(jsonify(
        get_res_common_struct(340000, "核心接口数据请求成功", {"data": history_plan_list, "totolPage": page_data.pages})), 200)
    response = set_req_header_fix_cross_domain(response, "GET")
    return response

# 删除历史计划接口
@plan.route("/deletehistoryplan", methods=["POST"])
@login_required
def delete_history_plan():
    resJson = request.get_json(force=True)
    if 'id' not in resJson.keys():
        response = make_response(jsonify(get_res_common_struct(350001, "缺少必要参数id，无法操作删除数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "POST")
        return response
    history_plan_data = query_plan_byId(resJson["id"])
    if history_plan_data:
        try:
            db.session.delete(history_plan_data)
            db.session.commit()
            response = make_response(jsonify(get_res_common_struct(350000, "历史计划删除成功", {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify(get_res_common_struct(350002, "数据库操作失败:{0}".format(e), {})), 200)
            response = set_req_header_fix_cross_domain(response, "POST")
            return response
    response = make_response(jsonify(get_res_common_struct(350003, "没有查询到此interfaceid对应的接口数据", {})), 200)
    response = set_req_header_fix_cross_domain(response, "POST")
    return response

# 查看单个历史计划数据
@plan.route("/historyplan/<id>", methods=["GET"])
@login_required
def certain_history_plan(id):
    history_plan_data = query_plan_byId(plan_id=id)
    if not history_plan_data:
        response = make_response(jsonify(get_res_common_struct(360001, "没有查询到此id对应的历史计划数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response

    if "pageid" not in list(request.args.keys()):
        response = make_response(jsonify(get_res_common_struct(360002, "缺少必要参数pageid，无法获取相应数据", {})), 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response
    page_id = int(request.args["pageid"])
    core_data_list = json.loads(history_plan_data.core_data)

    if len(core_data_list) % 10 == 0:
        totalPages = int(len(core_data_list) / 10)
    else:
        totalPages = int(len(core_data_list)/10) + 1

    if page_id * 10 - len(core_data_list) >= 10:
        response = make_response(jsonify(get_res_common_struct(360003, "查询越界", {"data": [], "totalPages": totalPages})),
                                 200)
        response = set_req_header_fix_cross_domain(response, "GET")
        return response

    core_data_list = core_data_list[page_id * 10 - 10:page_id * 10]
    response = make_response(jsonify(
        get_res_common_struct(360000, "查询成功", {"data": core_data_list, "totalPages": totalPages})),200)
    response = set_req_header_fix_cross_domain(response, "GET")
    return response