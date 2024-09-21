from flask import Blueprint, request, jsonify

from backend.controllers.pointactions_controcall import get_user_ranking
from backend.controllers.user_controller import (
    get_users, get_user, create_new_user, update_existing_user, delete_user_record,
    login_user, get_user_claimed_topics, get_user_redemption_history, get_user_proposed_topics
)
from backend.middleware import token_required

user_bp = Blueprint('user_bp', __name__)

# 用户本月积分排名路由
@user_bp.route('/users/ranking', methods=['GET'])
@token_required
def user_ranking_route(user_id):
    try:
        users_ranking = get_user_ranking()  # 调用控制器获取排名
        return jsonify(users_ranking), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 获取所有用户
@user_bp.route('/users', methods=['GET'])
@token_required
def list_users(user_id):
    return get_users()

# 根据 ID 获取单个用户
@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id_route(user_id_from_token, user_id):
    return get_user(user_id)

# 创建新用户
@user_bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.json
    return create_new_user(data)

# 根据 ID 更新用户
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user_route(user_id_from_token, user_id):
    data = request.json
    return update_existing_user(user_id, data)


# 根据 ID 删除用户
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user_route(user_id):
    return delete_user_record(user_id)

# 用户登录路由
@user_bp.route('/users/login', methods=['POST'])
def login_route():
    data = request.json
    try:
        return login_user(data)
    except Exception as e:
        # 捕获并输出错误信息
        return jsonify({'error': str(e)}), 500

# 获取当前用户信息
@user_bp.route('/users/me', methods=['GET'])
@token_required
def get_current_user_info_route(user_id):
    return get_user(user_id)  # `get_user` 方法会返回用户的详细信息

# 获取用户发布的选题，需登录（token_required）
@user_bp.route('/users/proposed-topics', methods=['GET'])
@token_required
def get_user_proposed_topics_route(user_id):
    # 通过 token_required 提取的 user_id 传递到控制器中
    return get_user_proposed_topics(user_id)

# 获取用户认领的选题
@user_bp.route('/users/claimed-topics', methods=['GET'])
@token_required
def get_user_claimed_topics_route(user_id):
    claimed_topics = get_user_claimed_topics(user_id)
    return jsonify(claimed_topics), 200

# 获取用户的兑换记录
@user_bp.route('/users/redemption-history', methods=['GET'])
@token_required
def get_user_redemption_history_route(user_id):
    redemption_history = get_user_redemption_history(user_id)
    return jsonify(redemption_history), 200
