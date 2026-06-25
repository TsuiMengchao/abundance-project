from abundance_flask.app import db

class User(db.Model):
    """用户模型"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, default=db.func.now())