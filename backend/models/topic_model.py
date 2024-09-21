from datetime import datetime
from backend.db import db

class Topic(db.Model):
    """
    主题模型，代表数据库中的topics表。
    """
    __tablename__ = 'topics'  # 表名

    topic_id = db.Column(db.Integer, primary_key=True)  # 主题ID，主键
    direction_id = db.Column(db.Integer, nullable=False)  # 方向ID，不能为空
    topic_name = db.Column(db.String(255), nullable=False)  # 主题名称，不能为空
    topic_description = db.Column(db.Text, nullable=False)  # 主题描述，不能为空
    proposed_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # 提出者，不能为空
    claimed_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)  # 认领者，可以为空
    submission_link = db.Column(db.String(255), nullable=True)  # 提交链接，可以为空
    status = db.Column(db.String(50), nullable=False)  # 状态，不能为空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，默认为当前UTC时间
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)  # 提交时间，默认为当前UTC时间

    # 定义与 User 的关系
    proposed_by_user = db.relationship('User', foreign_keys=[proposed_by])  # 通过proposed_by外键关联User
    claimed_by_user = db.relationship('User', foreign_keys=[claimed_by])    # 通过claimed_by外键关联User


# 获取所有选题
def get_all_topics():
    return Topic.query.all()

# 根据 topic_id 获取特定的选题
def get_topic_by_id(topic_id):
    return Topic.query.get(topic_id)

# 创建新的选题
def create_topic(data):
    new_topic = Topic(
        direction_id=data['direction_id'],  # 选题方向ID
        topic_name=data['topic_name'],  # 选题名称
        topic_description=data['topic_description'],  # 选题描述
        proposed_by=data['proposed_by'],  # 提案人
        claimed_by=data.get('claimed_by'),  # 已认领人（可能为空）
        submission_link=data.get('submission_link'),  # 提交链接（可能为空）
        status=data['status']  # 选题状态
    )
    db.session.add(new_topic)
    db.session.commit()

# 更新现有的选题
def update_topic(topic_id, data):
    topic = Topic.query.get(topic_id)
    if topic:
        topic.direction_id = data['direction_id']
        topic.topic_name = data['topic_name']
        topic.topic_description = data['topic_description']
        topic.proposed_by = data['proposed_by']
        topic.claimed_by = data.get('claimed_by')
        topic.submission_link = data.get('submission_link')
        topic.status = data['status']
        db.session.commit()

# 删除选题
def delete_topic(topic_id):
    topic = Topic.query.get(topic_id)
    if topic:
        db.session.delete(topic)
        db.session.commit()

# 获取用户认领的选题
def get_claimed_topics_by_user(user_id):
    return Topic.query.filter_by(claimed_by=user_id).all()
