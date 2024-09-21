from flask import Blueprint, request
from backend.controllers.reward_controller import (
    get_rewards, get_reward, create_new_reward,
    update_existing_reward, delete_reward_record, redeem_reward
)
from backend.middleware import token_required

reward_bp = Blueprint('reward_bp', __name__)

# 获取所有商品
@reward_bp.route('/rewards', methods=['GET'])
@token_required  # 需要登录用户才能查看所有商品
def list_rewards(user_id):
    return get_rewards()

# 根据 ID 获取单个商品
@reward_bp.route('/rewards/<int:reward_id>', methods=['GET'])
@token_required  # 需要登录用户才能获取单个商品
def get_reward_by_id(reward_id):
    return get_reward(reward_id)

# 创建新商品
@reward_bp.route('/rewards', methods=['POST'])
@token_required  # 需要登录用户才能创建新商品
def create_reward(user_id):
    data = request.json
    return create_new_reward(data)

# 根据 ID 更新商品
@reward_bp.route('/rewards/<int:reward_id>', methods=['PUT'])
@token_required  # 需要登录用户才能更新商品
def update_reward(user_id, reward_id):
    data = request.json
    return update_existing_reward(reward_id, data)

# 根据 ID 删除商品
@reward_bp.route('/rewards/<int:reward_id>', methods=['DELETE'])
@token_required  # 需要登录用户才能删除商品
def delete_reward(user_id, reward_id):
    return delete_reward_record(reward_id)

# 兑换奖励
@reward_bp.route('/rewards/<int:reward_id>/redeem', methods=['POST'])
@token_required
def redeem_reward_route(user_id, reward_id):
    return redeem_reward(user_id, reward_id)