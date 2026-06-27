from abundance_flask.app import db

# 词条主表
class Entry(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    parentId = db.Column(db.String(128), nullable=True)
    content = db.Column(db.Text, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)
    deletedAt = db.Column(db.Integer, nullable=True)
    createdAt = db.Column(db.Integer, nullable=False)
    updatedAt = db.Column(db.Integer, nullable=True)
    userId = db.Column(db.String(64), nullable=False)
    updatorId = db.Column(db.String(64), nullable=True)
    isPublic = db.Column(db.Boolean, default=False)

# 词条历史记录表
class EntryHistoryItem(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    entryId = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.String(64), nullable=False)

# 词条复制记录表
class EntryCopyItem(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    entryId = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.String(64), nullable=False)