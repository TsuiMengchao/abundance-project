from flask import Blueprint, request, jsonify
from abundance_flask.app.services.entry_service import query_to_flat_data, batch_save_flat

entry_bp = Blueprint("entry", __name__)

# ===================== 接口1：上传接口 POST /api/upload =====================
"""
请求体结构：
{
  "userId": "你的用户ID",
  "isPublic": false,
  "entries": [...主词条数组],
  "historyRecords": [...历史记录数组],
  "copyRecords": [...复制记录数组]
}
"""
@entry_bp.route("/upload", methods=["POST"])
def upload():
    req_data = request.get_json()
    if not req_data or "userId" not in req_data:
        return jsonify({"code": 400, "msg": "缺少userId参数"}), 400

    uid = req_data["userId"]
    is_public = req_data.get("isPublic", False)
    flat_data = {
        "entries": req_data.get("entries", []),
        "historyRecords": req_data.get("historyRecords", []),
        "copyRecords": req_data.get("copyRecords", [])
    }

    count = batch_save_flat(flat_data, uid, is_public)
    return jsonify({
        "code": 200,
        "msg": "上传完成",
        "uploadCount": count
    })

# ===================== 接口2：同步拉取接口 GET /api/sync =====================
"""
请求地址：/api/sync?userId=xxx
返回扁平三数组，前端直接复用导入合并逻辑
{
  "code":200,
  "data": {
    "entries": [],
    "historyRecords": [],
    "copyRecords": []
  }
}
"""
@entry_bp.route("/sync", methods=["GET"])
def sync():
    uid = request.args.get("userId", "")
    if not uid:
        return jsonify({"code": 400, "msg": "userId不能为空"}), 400

    flat = query_to_flat_data(uid)
    total = len(flat["entries"])
    return jsonify({
        "code": 200,
        "data": flat,
        "entryCount": total
    })