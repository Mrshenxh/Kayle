

from ..config.exts import db

# 根据id查找plan
def query_plan_byId(plan_id):
    plans = PlanList.query.filter_by(id=plan_id).all()
    if len(plans) != 0:
        return plans[0]
    return None

# 创建ORM映射
class PlanList(db.Model):
    __tablename__ = 'history_plan_list'
    id = db.Column(db.Integer, primary_key=True)
    plan_userId = db.Column(db.String(20))
    plan_user = db.Column(db.String(20))
    client_version = db.Column(db.String(20))
    plan_start = db.Column(db.String(20))
    plan_end = db.Column(db.String(20))
    core_rate = db.Column(db.String(20))
    core_data = db.Column(db.Text)