from flask import jsonify
from backend.models.reward_model import Reward
from sqlalchemy.exc import SQLAlchemyError
from backend.models.user_model import User
from backend.db import db
from backend.models.redemption_model import Redemption

# 获取所有奖励
def get_rewards():
    try:
        rewards = Reward.query.all()
        rewards_list = [reward.to_dict() for reward in rewards]
        return jsonify(rewards_list), 200
    except SQLAlchemyError as e:
        return jsonify({'message': 'Failed to retrieve rewards', 'error': str(e)}), 500

# 获取单个奖励
def get_reward(reward_id):
    try:
        reward = Reward.query.get(reward_id)
        if reward:
            return jsonify(reward.to_dict()), 200
        else:
            return jsonify({'message': 'Reward not found'}), 404
    except SQLAlchemyError as e:
        return jsonify({'message': 'Failed to retrieve reward', 'error': str(e)}), 500

# 创建新的奖励
def create_new_reward(data):
    try:
        new_reward = Reward(
            name=data['name'],
            description=data['description'],
            points_required=data['points_required'],
            stock=data['stock'],
            image_url=data.get('image_url')
        )
        db.session.add(new_reward)
        db.session.commit()
        return jsonify({'message': 'Reward created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create reward', 'error': str(e)}), 500

# 更新现有奖励
def update_existing_reward(reward_id, data):
    try:
        reward = Reward.query.get(reward_id)
        if not reward:
            return jsonify({'message': 'Reward not found'}), 404

        reward.name = data.get('name', reward.name)
        reward.description = data.get('description', reward.description)
        reward.points_required = data.get('points_required', reward.points_required)
        reward.stock = data.get('stock', reward.stock)
        reward.image_url = data.get('image_url', reward.image_url)

        db.session.commit()
        return jsonify({'message': 'Reward updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update reward', 'error': str(e)}), 500

# 删除奖励
def delete_reward_record(reward_id):
    try:
        reward = Reward.query.get(reward_id)
        if not reward:
            return jsonify({'message': 'Reward not found'}), 404

        db.session.delete(reward)
        db.session.commit()
        return jsonify({'message': 'Reward deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete reward', 'error': str(e)}), 500

# 兑换奖励
def redeem_reward(user_id, reward_id):
    try:
        user = User.query.get(user_id)
        reward = Reward.query.get(reward_id)

        if not user or not reward:
            return jsonify({'message': '用户或奖励未找到'}), 404

        # 检查用户的剩余积分（available_points）是否足够
        if user.available_points < reward.points_required:
            return jsonify({'message': '积分不足，无法兑换奖励'}), 400

        if reward.stock <= 0:
            return jsonify({'message': '该奖励已售罄'}), 400

        # 减少用户的剩余积分 (available_points)，但保持 total_points 不变
        user.available_points -= reward.points_required
        reward.stock -= 1

        # 创建兑换记录，插入到 `redemptions` 表中
        redemption = Redemption(
            user_id=user_id,
            reward_id=reward_id,
            quantity=1,  # 假设每次兑换一个商品
            points_spent=reward.points_required,
            status="completed"  # 兑换状态为已完成
        )
        db.session.add(redemption)
        db.session.commit()

        return jsonify({'message': '奖励兑换成功'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': '兑换奖励失败', 'error': str(e)}), 500