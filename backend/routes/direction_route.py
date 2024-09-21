from flask import Blueprint, request
from backend.controllers.direction_controller import get_directions, get_direction, create_new_direction, update_existing_direction, delete_direction_record
from backend.middleware import token_required

direction_bp = Blueprint('direction_bp', __name__)

# 获取所有选题方向
@direction_bp.route('/directions', methods=['GET'])
def list_directions():
    return get_directions()

# 根据 ID 获取单个选题方向
@direction_bp.route('/directions/<int:direction_id>', methods=['GET'])
def get_direction_by_id(direction_id):
    return get_direction(direction_id)

# 创建新选题方向
@direction_bp.route('/directions', methods=['POST'])
@token_required  # 需要登录用户才能创建新方向
def create_direction(user_id):
    data = request.json
    return create_new_direction(data)

# 根据 ID 更新选题方向
@direction_bp.route('/directions/<int:direction_id>', methods=['PUT'])
@token_required  # 需要登录用户才能更新方向
def update_direction(user_id, direction_id):
    data = request.json
    return update_existing_direction(direction_id, data)

# 根据 ID 删除选题方向
@direction_bp.route('/directions/<int:direction_id>', methods=['DELETE'])
@token_required  # 需要登录用户才能删除方向
def delete_direction(user_id, direction_id):
    return delete_direction_record(direction_id)
