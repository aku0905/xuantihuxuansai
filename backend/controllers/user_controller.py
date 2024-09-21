import jwt
import bcrypt
from flask import jsonify
from backend.models.user_model import User, get_user_by_username, create_user, update_user, delete_user
from backend.models.topic_model import Topic
from backend.models.redemption_model import Redemption
import datetime
from sqlalchemy.exc import IntegrityError

SECRET_KEY = 'your_secret_key'


# 登录用户，生成 JWT token
def login_user(data):
    username = data.get('username')
    password = data.get('password')

    # 根据用户名查找用户
    try:
        user = get_user_by_username(username)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # 验证密码
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({'message': 'Invalid password'}), 401

        # 生成 JWT token
        token = jwt.encode({
            'user_id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({'token': token}), 200

    except Exception as e:
            return jsonify({"error": str(e)}), 500



# 解码 token
def decode_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


# 获取所有用户
def get_users():
    users = User.query.all()  # 从数据库中获取所有用户
    users_list = [{
        'user_id': user.user_id,
        'username': user.username,
        'total_points': user.total_points,
        'available_points': user.available_points
    } for user in users]

    return jsonify(users_list)


# 获取单个用户信息
def get_user(user_id):
    user = User.query.get(user_id)  # 从数据库中获取指定用户
    if user:
        return jsonify({
            "user_id": user.user_id, # 从数据库中获取
            "username": user.username,
            "totalPoints": user.total_points,
            "availablePoints": user.available_points,
        })
    else:
        return jsonify({'message': 'User not found'}), 404


# 创建新用户
def create_new_user(data):
    try:
        # 密码加密
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')  # 转换为字符串存储

        # 使用模型层的 create_user 方法
        create_user(data)
        return jsonify({'message': 'User created successfully'}), 201

    except IntegrityError:
        return jsonify({'message': 'Username already exists'}), 400


# 更新现有用户信息
def update_existing_user(user_id, data):
    user = User.query.get(user_id)  # 检查用户是否存在
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if 'password' in data:
        # 如果更新了密码，则加密
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')

    # 使用模型层的 update_user 方法
    update_user(user_id, data)
    return jsonify({'message': 'User updated successfully'})


# 删除用户
def delete_user_record(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    delete_user(user_id)  # 从数据库中删除用户
    return jsonify({'message': 'User deleted successfully'})


# 获取用户提出的选题
def get_user_proposed_topics(user_id):
    proposed_topics = Topic.query.filter_by(proposed_by=user_id).all()

    # 将结果转为 JSON 格式
    topics_list = [{
        'topic_name': topic.topic_name,
        'status': topic.status
    } for topic in proposed_topics]

    return jsonify(topics_list), 200


# 获取用户认领的选题
def get_user_claimed_topics(user_id):
    claimed_topics = Topic.query.filter_by(claimed_by=user_id).all()

    # 将结果转为 JSON 格式
    topics_list = [{
        'topic_name': topic.topic_name,
        'status': topic.status,
        'submitted_at': topic.submitted_at
    } for topic in claimed_topics]

    return jsonify(topics_list), 200


# 获取当前用户的兑换记录
def get_user_redemption_history(user_id):
    redemption_records = Redemption.query.filter_by(user_id=user_id).all()

    # 将结果转为 JSON 格式
    redemption_list = [{
        'reward_name': redemption.reward.name,  # 假设 reward_id 外键链接到 rewards 表
        'quantity': redemption.quantity,
        'status': redemption.status,
        'created_at': redemption.created_at
    } for redemption in redemption_records]

    return jsonify(redemption_list), 200
