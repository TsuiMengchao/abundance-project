from abundance_flask.app import db
from abundance_flask.app.models.entry_model import Entry, EntryHistoryItem, EntryCopyItem

def query_to_flat_data(uid: str):
    """
    查询公开词条 + 当前用户私有词条，返回扁平三数组
    return {"entries": [], "historyRecords": [], "copyRecords": []}
    """
    # 1. 主词条：全部公开 + 当前用户私有
    entry_list = Entry.query.filter(
        db.or_(
            Entry.isPublic == True,
            db.and_(Entry.userId == uid, Entry.isPublic == False)
        )
    ).all()

    entries = []
    entry_ids = set()
    for e in entry_list:
        entries.append({
            "id": e.id,
            "parentId": e.parentId,
            "content": e.content,
            "isDeleted": e.isDeleted,
            "deletedAt": e.deletedAt,
            "createdAt": e.createdAt,
            "updatedAt": e.updatedAt,
            "userId": e.userId,
            "isPublic": e.isPublic
        })
        entry_ids.add(e.id)

    # 2. 对应词条的全部历史记录
    history = EntryHistoryItem.query.filter(EntryHistoryItem.entryId.in_(entry_ids)).all()
    history_records = []
    for h in history:
        history_records.append({
            "id": h.id,
            "entryId": h.entryId,
            "content": h.content,
            "timestamp": h.timestamp,
            "userId": h.userId
        })

    # 3. 对应词条的全部复制记录
    copy = EntryCopyItem.query.filter(EntryCopyItem.entryId.in_(entry_ids)).all()
    copy_records = []
    for c in copy:
        copy_records.append({
            "id": c.id,
            "entryId": c.entryId,
            "content": c.content,
            "timestamp": c.timestamp,
            "userId": c.userId
        })

    return {
        "entries": entries,
        "historyRecords": history_records,
        "copyRecords": copy_records
    }

def batch_save_flat(raw: dict, upload_user_id: str, is_public: bool):
    """
    接收前端扁平三数组，批量入库，只处理当前userId的词条
    raw = {"entries":[], "historyRecords":[], "copyRecords":[]}
    """
    entries = raw.get("entries", [])
    hist_list = raw.get("historyRecords", [])
    copy_list = raw.get("copyRecords", [])

    # 过滤：仅上传属于当前用户的词条
    my_entry_ids = set()
    for e in entries:
        if e.get("userId") != upload_user_id:
            continue
        eid = e["id"]
        my_entry_ids.add(eid)
        # 存在则删除旧数据
        Entry.query.filter_by(id=eid).delete()
        new_e = Entry(
            id=e["id"],
            parentId=e["parentId"],
            content=e["content"],
            isDeleted=e["isDeleted"],
            deletedAt=e.get("deletedAt"),
            createdAt=e["createdAt"],
            updatedAt=e["updatedAt"],
            userId=e["userId"],
            isPublic=is_public
        )
        db.session.add(new_e)

    # 批量保存历史记录（仅当前用户词条关联的）
    for h in hist_list:
        if h["entryId"] not in my_entry_ids:
            continue
        EntryHistoryItem.query.filter_by(id=h["id"]).delete()
        new_h = EntryHistoryItem(
            id=h["id"],
            entryId=h["entryId"],
            content=h["content"],
            timestamp=h["timestamp"],
            userId=h["userId"]
        )
        db.session.add(new_h)

    # 批量保存复制记录（仅当前用户词条关联的）
    for c in copy_list:
        if c["entryId"] not in my_entry_ids:
            continue
        EntryCopyItem.query.filter_by(id=c["id"]).delete()
        new_c = EntryCopyItem(
            id=c["id"],
            entryId=c["entryId"],
            content=c["content"],
            timestamp=c["timestamp"],
            userId=c["userId"]
        )
        db.session.add(new_c)

    db.session.commit()
    return len(my_entry_ids)