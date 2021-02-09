
from ..config.exts import db

# 通过interface_id，获取接口数据，如果不存在，返回None
def query_user_by_interface_id(interface_id):
    print(interface_id)
    tempInterface = CoreInterface.query.filter_by(interface_id=interface_id).all()
    if len(tempInterface) != 0:
        return tempInterface[0]
    return None

# 通过 interfaceRegular 获取接口数据，如果不存在，返回None
def query_interface_by_regular(interface_regular):
    interface_list = CoreInterface.query.filter_by(interface_regular=interface_regular).all()
    if len(interface_list) != 0:
        return interface_list[0]
    return None

# 通过port,查询现有临时mitmproxy表中数据，如果不存在，返回None
def query_user_by_port(port):
    print(port)
    tempUserPort = TempUserPort.query.filter_by(port=port).all()
    if len(tempUserPort) != 0:
        return tempUserPort[0]
    return None

# 通过mitm_id,查询现有临时mitmproxy表中数据，如果不存在，返回None
def query_user_by_mitm_id(mitm_id):
    print(mitm_id)
    tempUserPort = TempUserPort.query.filter_by(mitm_id=mitm_id).all()
    if len(tempUserPort) != 0:
        return tempUserPort[0]
    return None

# 通过user_id,查询现有临时mitmproxy表中数据，如果不存在，返回None
def query_tempuser_by_user_id(user_id):
    print(user_id)
    tempUserPort = TempUserPort.query.filter_by(user_id=user_id).all()
    if len(tempUserPort) != 0:
        return tempUserPort[0]
    return None


# 创建核心接口ORM映射
class CoreInterface(db.Model):
    __tablename__ = 'core_interface_list'
    interface_id = db.Column(db.String(20), primary_key=True, nullable=False)
    interface_path = db.Column(db.String(256))
    req_header = db.Column(db.Text)
    user_id = db.Column(db.String(80))
    user_name = db.Column(db.String(80))
    req_data = db.Column(db.Text)
    req_query = db.Column(db.String(80))
    req_form = db.Column(db.String(80))
    req_method = db.Column(db.String(80))
    req_scheme = db.Column(db.String(80))
    req_start = db.Column(db.String(80))
    req_end = db.Column(db.String(80))
    req_cookie = db.Column(db.Text)
    res_status_code = db.Column(db.String(80))
    res_header = db.Column(db.Text)
    res_text = db.Column(db.Text)
    res_cookie = db.Column(db.Text)
    res_start = db.Column(db.String(80))
    res_end = db.Column(db.String(80))
    exprie_time = db.Column(db.String(80))
    mitm_id = db.Column(db.String(80))
    content = db.Column(db.String(80))
    interface_regular = db.Column(db.String(80))
    interface_desc = db.Column(db.String(256))

class TempUserPort(db.Model):
    __tablename__ = 'temp_mitmproxy_list'
    port = db.Column(db.String(256))
    host_list = db.Column(db.Text)
    user_id = db.Column(db.String(80))
    expire_time = db.Column(db.String(80))
    mitm_id = db.Column(db.String(20), primary_key=True, nullable=False)