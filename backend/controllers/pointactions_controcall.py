from backend.models.pointaction_model import PointAction
from sqlalchemy.exc import SQLAlchemyError
from backend.db import db
from backend.models.user_model import User
from flask import jsonify

from sqlalchemy import func, extract
from datetime import datetime

# 更新用户积分
def update_user_points(user_id, points, action_type, topic_id=None):
    """
    更新用户积分，同时记录积分行为。

    :param user_id: 用户ID
    :param points: 需要增加或减少的积分（正数为加分，负数为扣分）
    :param action_type: 积分行为的类型（例如："出题", "提交作品"）
    :param topic_id: 关联的选题ID（可选）
    """
    try:
        # 更新用户积分
        user = User.query.get(user_id)
        user.available_points += points  # 更新剩余积分
        user.total_points += points  # 更新总积分

        # 插入积分行为记录
        new_point_action = PointAction(
            user_id=user_id,
            action_type=action_type,
            points=points,
            topic_id=topic_id  # 可选的选题ID
        )
        db.session.add(new_point_action)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        print(f"SQLAlchemy Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")

# 获取用户积分记录
def get_user_point_actions(user_id):
    """
    获取指定用户的积分记录。

    :param user_id: 用户ID
    :return: 用户积分记录的JSON格式
    """
    try:
        # 查询用户的积分记录
        point_actions = PointAction.query.filter_by(user_id=user_id).all()

        # 将记录转换为JSON格式
        result = []
        for action in point_actions:
            result.append({
                'action_id': action.action_id,
                'action_type': action.action_type,
                'points': action.points,
                'topic_id': action.topic_id,
                'created_at': action.created_at.isoformat()  # 将日期时间格式化为ISO格式
            })

        return jsonify(result), 200

    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return jsonify({'error': 'Unexpected error'}), 500

# 查询当月所有用户积分排名情况
def get_user_ranking():
    # 获取当前月份和年份
    current_month = datetime.now().month
    current_year = datetime.now().year

    # 查询当月每个用户的总积分，并按积分进行降序排序
    ranking_data = db.session.query(
        User.user_id, User.username, func.sum(PointAction.points).label('total_points')
    ).join(PointAction, User.user_id == PointAction.user_id).filter(
        extract('month', PointAction.created_at) == current_month,
        extract('year', PointAction.created_at) == current_year
    ).group_by(User.user_id).order_by(func.sum(PointAction.points).desc()).all()

    # 返回用户积分排名列表
    users_ranking = [
        {
            'user_id': user_id,
            'username': username,
            'total_points': total_points
        }
        for user_id, username, total_points in ranking_data
    ]

    return users_ranking

# 根据用户ID和选题ID删除积分记录
def delete_user_point_action(user_id, topic_id):
    """
    根据用户ID和选题ID删除积分记录。

    :param user_id: 用户ID
    :param topic_id: 选题ID
    :return: 删除结果的JSON格式
    """
    try:
        # 查询指定用户ID和选题ID的积分记录
        point_action = PointAction.query.filter_by(user_id=user_id, topic_id=topic_id).first()

        if not point_action:
            return jsonify({'message': 'No matching point action found'}), 404

        # 删除找到的记录
        db.session.delete(point_action)
        db.session.commit()

        return jsonify({'message': 'Point action deleted successfully'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()  # 回滚事务
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'error': 'Failed to delete point action', 'error_detail': str(e)}), 500

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return jsonify({'error': 'Unexpected error occurred', 'error_detail': str(e)}), 500
