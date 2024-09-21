from flask import Blueprint, request, jsonify
from backend.controllers.topic_controller import get_all_topics, create_new_topic, update_existing_topic, \
    delete_topic_record, get_current_topics_by_direction

from backend.controllers.user_controller import get_user_proposed_topics
from backend.middleware import token_required

# 创建 topic_bp 蓝图
topic_bp = Blueprint('topic_bp', __name__)

# 根据选题方向获取当前题目
@topic_bp.route('/topics/current', methods=['GET'])
def get_current_topics():
    direction_id = request.args.get('direction')
    print(f"Received direction_id: {direction_id}")  # 调试信息
    if not direction_id:
        return jsonify({'message': 'Direction ID is required'}), 400
    return get_current_topics_by_direction(direction_id)


# 获取所有选题
@topic_bp.route('/topics', methods=['GET'])
def list_topics():
    return get_all_topics()

# 根据 ID 获取单个选题
@topic_bp.route('/topics/<int:topic_id>', methods=['GET'])
def get_topic_by_id(topic_id):
    return get_all_topics(topic_id)


# 创建新选题的路由处理函数
@topic_bp.route('/topics', methods=['POST'])
@token_required  # 需要用户登录才可以创建新选题
def create_topic(user_id):
    data = request.json  # 获取请求中的JSON数据
    data['proposed_by'] = user_id  # 将当前登录用户的用户名添加到数据中
    return create_new_topic(data)  # 调用创建新选题的函数并返回结果


# 根据 ID 更新选题
@topic_bp.route('/topics/<int:topic_id>', methods=['PUT'])
@token_required  # 更新选题也应该需要用户登录
def update_topic(user_id, topic_id):
    data = request.json
    return update_existing_topic(topic_id, data)

# 根据 ID 删除选题
@topic_bp.route('/topics/<int:topic_id>', methods=['DELETE'])
@token_required  # 删除选题也应限制为登录用户操作
def delete_topic(user_id, topic_id):
    return delete_topic_record(topic_id)

# 获取用户发布的选题，需登录
@topic_bp.route('/users/proposed-topics', methods=['GET'])
@token_required
def get_user_proposed_topics_route(user_id):
    return get_user_proposed_topics(user_id)  # 确保函数名称一致
