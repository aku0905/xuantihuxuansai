from flask import Blueprint, request, jsonify
from backend.controllers.redemption_controller import get_redemptions, get_redemptions, create_new_redemption, update_existing_redemption, delete_redemption_record
from backend.middleware import token_required

redemption_bp = Blueprint('redemption_bp', __name__)

# 获取所有兑换记录
@redemption_bp.route('/redemptions', methods=['GET'])
@token_required  # 需要登录用户才能获取兑换记录
def list_redemptions(user_id):
    redemptions = get_redemptions(user_id)
    return jsonify(redemptions)

# 根据 ID 获取单个兑换记录
@redemption_bp.route('/redemptions/<int:redemption_id>', methods=['GET'])
def get_redemption_by_id(redemption_id):
    return get_redemptions(redemption_id)

# 创建新兑换记录
@redemption_bp.route('/redemptions', methods=['POST'])
@token_required  # 需要登录用户才能创建兑换记录
def create_redemption(user_id):
    data = request.json
    return create_new_redemption(data)

# 根据 ID 更新兑换记录
@redemption_bp.route('/redemptions/<int:redemption_id>', methods=['PUT'])
@token_required  # 需要登录用户才能更新兑换记录
def update_redemption(user_id, redemption_id):
    data = request.json
    return update_existing_redemption(redemption_id, data)

# 根据 ID 删除兑换记录
@redemption_bp.route('/redemptions/<int:redemption_id>', methods=['DELETE'])
@token_required  # 需要登录用户才能删除兑换记录
def delete_redemption(user_id, redemption_id):
    return delete_redemption_record(redemption_id)
