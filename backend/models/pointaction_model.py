from datetime import datetime
from backend.db import db  # 引入全局的 db 实例，而不是重新创建 SQLAlchemy 实例
from backend.models.user_model import User

class PointAction(db.Model):
    __tablename__ = 'point_actions'  # 定义表名为 point_actions

    action_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 定义 action_id 字段为主键，自增
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # 定义 user_id 字段，外键关联 users 表的 user_id，不能为空
    action_type = db.Column(db.String(255), nullable=False)  # 定义 action_type 字段，字符串类型，最大长度 255，不能为空
    points = db.Column(db.Integer, nullable=False)  # 定义 points 字段，整型，不能为空
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'), nullable=True)  # 定义 topic_id 字段，外键关联 topics 表的 topic_id，可以为空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 定义 created_at 字段，日期时间类型，默认值为当前 UTC 时间

    # 定义 relationship，指向 User 模型
    user = db.relationship('User', backref='point_actions')

    def __repr__(self):
        """返回 PointAction 对象的字符串表示形式"""
        return f"<PointAction {self.action_id} - User {self.user_id} - Points {self.points}>"
