from abundance_flask.app.models.user_model import User
from abundance_flask.app import db

def get_user_list():
    """获取用户列表（业务逻辑）"""
    users = User.query.all()
    # 数据格式化（也可通过schemas层校验/序列化）
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]