from flask import jsonify
from backend.models.redemption_model import Redemption
from sqlalchemy.exc import SQLAlchemyError
from backend.db import db


def get_redemptions(user_id):
    """
    获取指定用户的兑换记录，包含奖励的名称。

    参数:
        user_id (int): 用户的唯一标识符。

    Returns:
        list: 包含用户兑换记录和奖励名称的字典列表。
    """
    # 查询数据库，连接 Redemption 和 Reward 表，并筛选指定用户的兑换记录
    from backend.models.reward_model import Reward
    results = db.session.query(
        Redemption.redemption_id,  # 兑换ID
        Redemption.user_id,        # 用户ID
        Redemption.reward_id,      # 奖励ID
        Redemption.quantity,       # 数量
        Redemption.points_spent,   # 消耗积分
        Redemption.status,         # 状态
        Redemption.created_at,     # 创建时间
        Reward.name.label('reward_name')  # 获取奖励名称
    ) \
        .join(Reward, Redemption.reward_id == Reward.reward_id).filter(Redemption.user_id == user_id).all()

    # 将每条兑换记录转换为字典形式，并存储在列表中
    redemptions_list = [{
        'redemption_id': redemption.redemption_id,  # 兑换ID
        'user_id': redemption.user_id,              # 用户ID
        'reward_id': redemption.reward_id,          # 奖励ID
        'reward_name': redemption.reward_name,      # 奖励名称
        'quantity': redemption.quantity,            # 数量
        'points_spent': redemption.points_spent,    # 消耗的积分
        'status': redemption.status,                # 状态
        'created_at': redemption.created_at,        # 创建时间
    } for redemption in results]

    return redemptions_list  # 返回包含所有兑换记录的列表

# 创建新的兑换记录
def create_new_redemption(data):
    try:
        new_redemption = Redemption(
            user_id=data['user_id'],
            reward_id=data['reward_id'],
            quantity=data['quantity'],
            points_spent=data['points_spent'],
            status=data['status']
        )
        db.session.add(new_redemption)
        db.session.commit()
        return jsonify({'message': 'Redemption created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create redemption', 'error': str(e)}), 500


# 更新现有的兑换记录
def update_existing_redemption(redemption_id, data):
    redemption = Redemption.query.get(redemption_id)
    if not redemption:
        return jsonify({'message': 'Redemption not found'}), 404

    try:
        redemption.user_id = data.get('user_id', redemption.user_id)
        redemption.reward_id = data.get('reward_id', redemption.reward_id)
        redemption.quantity = data.get('quantity', redemption.quantity)
        redemption.points_spent = data.get('points_spent', redemption.points_spent)
        redemption.status = data.get('status', redemption.status)

        db.session.commit()
        return jsonify({'message': 'Redemption updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update redemption', 'error': str(e)}), 500


# 删除兑换记录
def delete_redemption_record(redemption_id):
    redemption = Redemption.query.get(redemption_id)
    if not redemption:
        return jsonify({'message': 'Redemption not found'}), 404

    try:
        db.session.delete(redemption)
        db.session.commit()
        return jsonify({'message': 'Redemption deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete redemption', 'error': str(e)}), 500
