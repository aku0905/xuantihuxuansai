from datetime import datetime
from backend.db import db


class Redemption(db.Model):

    # 定义表名
    __tablename__ = 'redemptions'

    # 定义表中的字段
    redemption_id = db.Column(db.Integer, primary_key=True)  # 主键，自增ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID，不能为空
    reward_id = db.Column(db.Integer, nullable=False)  # 奖励ID，不能为空
    quantity = db.Column(db.Integer, nullable=False)  # 数量，不能为空
    points_spent = db.Column(db.Integer, nullable=False)  # 消耗的积分，不能为空
    status = db.Column(db.String(50), nullable=False)  # 状态，不能为空，最大长度50字符
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，默认为当前UTC时间

class Reward(db.Model):
    # 定义名为'rewards'的数据库表
    __tablename__ = 'rewards'

    # 定义表中的'reward_id'字段，数据类型为整数，作为主键
    reward_id = db.Column(db.Integer, primary_key=True)

    # 定义表中的'name'字段，数据类型为字符串，最大长度为255，且不能为空
    name = db.Column(db.String(255), nullable=False)




# 获取所有兑换记录
def get_all_redemptions():
    return Redemption.query.all()


# 根据 redemption_id 获取兑换记录
def get_redemption_by_id(redemption_id):
    return Redemption.query.get(redemption_id)


# 创建新的兑换记录
def create_redemption(data):
    new_redemption = Redemption(
        user_id=data['user_id'],  # 用户ID
        reward_id=data['reward_id'],  # 奖励ID
        quantity=data['quantity'],  # 兑换数量
        points_spent=data['points_spent'],  # 消耗的积分
        status=data['status']  # 兑换状态
    )
    db.session.add(new_redemption)  # 将新兑换记录添加到数据库会话
    db.session.commit()  # 提交数据库会话，保存更改


# 更新兑换记录
def update_redemption(redemption_id, data):
    redemption = Redemption.query.get(redemption_id)
    if redemption:
        redemption.user_id = data['user_id']
        redemption.reward_id = data['reward_id']
        redemption.quantity = data['quantity']
        redemption.points_spent = data['points_spent']
        redemption.status = data['status']
        db.session.commit()


# 根据兑换ID删除兑换记录
def delete_redemption(redemption_id):
    redemption = Redemption.query.get(redemption_id)
    if redemption:
        # 如果找到了兑换记录，则从数据库会话中删除并提交更改
        db.session.delete(redemption)
        db.session.commit()
