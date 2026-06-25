from flask import Blueprint, jsonify
from abundance_flask.app.services.user_service import get_user_list

# 创建蓝图（模块化路由）
main_bp = Blueprint("main", __name__)

@main_bp.route("/users", methods=["GET"])
def get_users():
    """示例接口：获取用户列表"""
    users = get_user_list()
    return jsonify({"code": 200, "data": users, "msg": "success"})