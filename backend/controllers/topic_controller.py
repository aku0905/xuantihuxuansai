from flask import jsonify
from sqlalchemy.orm import joinedload, aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from backend.controllers.pointactions_controcall import update_user_points, delete_user_point_action
from backend.models.topic_model import Topic
from backend.models.user_model import User
from backend.models.pointaction_model import PointAction
from backend.db import db


# 获取当前选题方向的题目
def get_current_topics_by_direction(direction_id):
    """
    根据选题方向ID查询当前方向下的所有题目，并返回题目信息，包括提出者和认领者的用户名。
    :param direction_id: 选题方向的唯一标识符
    :return: 题目列表的JSON对象和状态码
    """
    try:
        current_topics = Topic.query.filter_by(direction_id=direction_id) \
            .options(joinedload(Topic.proposed_by_user), joinedload(Topic.claimed_by_user)).all()

        result = [
            {
                'topic_id': topic.topic_id,
                'direction_id': topic.direction_id,
                'topic_name': topic.topic_name,
                'topic_description': topic.topic_description,
                'proposed_by': topic.proposed_by,
                'proposed_by_username': topic.proposed_by_user.username if topic.proposed_by_user else None,
                'claimed_by': topic.claimed_by,
                'claimed_by_username': topic.claimed_by_user.username if topic.claimed_by_user else None,
                'submission_link': topic.submission_link,
                'status': topic.status,
                'submitted_at': topic.submitted_at
            } for topic in current_topics
        ]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch topics', 'error': str(e)}), 500


# 创建新选题
def create_new_topic(data):
    """
    创建新选题记录，并根据规则为提出者加积分。
    :param data: 包含新选题信息的字典
    :return: 返回成功创建的信息以及选题ID，或错误信息和状态码
    """
    try:
        required_fields = ['direction_id', 'topic_name', 'topic_description', 'proposed_by', 'status']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        # 创建并添加新选题实例到数据库
        new_topic = Topic(
            direction_id=data['direction_id'],
            topic_name=data['topic_name'],
            topic_description=data['topic_description'],
            proposed_by=data['proposed_by'],
            claimed_by=data.get('claimed_by'),
            submission_link=data.get('submission_link'),
            status=data['status']
        )

        db.session.add(new_topic)
        db.session.commit()

        proposed_by = data['proposed_by']
        topic_id = new_topic.topic_id

        # 查询该方向下出题的加分记录数量
        current_direction_topics = get_direction_points_count(
            user_id=proposed_by,
            action_type='出题',
            direction_id=data['direction_id']
        )

        # 若本方向出题次数未超过3次，则增加2积分
        if current_direction_topics < 3:
            update_user_points(user_id=proposed_by, points=2, action_type='出题', topic_id=topic_id)

        return jsonify({'message': 'Topic created successfully', 'id': new_topic.topic_id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'message': 'Failed to create topic', 'error': str(e)}), 500

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500


# 获取所有选题，并返回认领用户和提出者的用户名而不是ID
def get_all_topics():
    """
    获取所有选题，并返回每个选题的详细信息，包括提出者和认领者的用户名。
    :return: 包含所有选题信息的JSON对象和状态码
    """
    try:
        topics = Topic.query.options(joinedload(Topic.proposed_by_user), joinedload(Topic.claimed_by_user)).all()

        result = [
            {
                'topic_id': topic.topic_id,
                'direction_id': topic.direction_id,
                'topic_name': topic.topic_name,
                'topic_description': topic.topic_description,
                'proposed_by': topic.proposed_by_user.username if topic.proposed_by_user else None,
                'claimed_by': topic.claimed_by_user.username if topic.claimed_by_user else None,
                'submission_link': topic.submission_link,
                'status': topic.status,
                'submitted_at': topic.submitted_at
            } for topic in topics
        ]

        return jsonify(result), 200
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch topics', 'error': str(e)}), 500


# 根据 topic_id 获取特定的选题
def get_topic_by_id(topic_id):
    """
    根据选题ID查询特定选题，并返回详细信息。
    :param topic_id: 选题的唯一标识符
    :return: 包含特定选题信息的JSON对象和状态码
    """
    try:
        topic = Topic.query.get(topic_id)
        if topic:
            return jsonify({
                'topic_id': topic.topic_id,
                'direction_id': topic.direction_id,
                'topic_name': topic.topic_name,
                'topic_description': topic.topic_description,
                'proposed_by': topic.proposed_by,
                'claimed_by': topic.claimed_by,
                'submission_link': topic.submission_link,
                'status': topic.status,
                'submitted_at': topic.submitted_at
            }), 200
        else:
            return jsonify({'message': 'Topic not found'}), 404
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch topic', 'error': str(e)}), 500


# 更新现有选题
def update_existing_topic(topic_id, data):
    """
    更新数据库中的现有选题信息，并根据更新的内容调整相关的用户积分。

    :param topic_id: 选题的唯一标识符
    :param data: 包含更新信息的字典
    :return: 返回更新成功或失败的信息以及相应的HTTP状态码
    """
    try:
        # 尝试从数据库中获取选题
        topic = Topic.query.get(topic_id)
        if not topic:
            return jsonify({'message': 'Topic not found'}), 404

        # 遍历更新数据，更新选题的属性
        for key, value in data.items():
            # 只更新选题表中存在的字段，否则保持原值
            setattr(topic, key, value if key in Topic.__table__.columns else getattr(topic, key))

        # 提交更改到数据库
        db.session.commit()

        # 获取选题的相关信息
        proposed_by = topic.proposed_by
        claimed_by = topic.claimed_by
        direction_id = topic.direction_id

        # 如果选题状态为待认领且没有被认领，更新出题人的积分
        if data.get('claimed_by') is None and data.get('status') == '待认领':
            direction_topics_count = get_direction_points_count(
                user_id=proposed_by,
                action_type='出题',
                direction_id=direction_id
            )
            # 如果出题人在该方向上的题目数量小于等于3，增加积分
            if direction_topics_count <= 3:
                update_user_points(user_id=proposed_by, points=2, action_type='出题', topic_id=topic_id)

        # 如果选题被认领且出题人与认领人相同，更新积分
        if data.get('claimed_by') and proposed_by == claimed_by:
            direction_topics_count = get_direction_points_count(
                user_id=proposed_by,
                action_type='出题',
                direction_id=direction_id
            )
            # 如果出题人在该方向上的题目数量小于3，删除认领人的积分并减少用户积分
            if direction_topics_count < 3:
                delete_user_point_action(user_id=claimed_by, topic_id=topic_id)
                user = User.query.get(claimed_by)
                user.available_points -= 2
                user.total_points -= 2
                db.session.add(user)
                db.session.commit()

        # 如果提供了新的提交链接，更新积分
        if data.get('submission_link'):
            previous_submission = PointAction.query.filter_by(topic_id=topic_id, action_type='题目被完成').first()

            # 如果出题人与认领人不同且之前没有完成记录，更新出题人积分
            if proposed_by != claimed_by and not previous_submission:
                proposed_points_sum = db.session.query(func.sum(PointAction.points)).join(
                    Topic, PointAction.topic_id == Topic.topic_id
                ).filter(
                    PointAction.user_id == proposed_by,
                    PointAction.action_type == '题目被完成',
                    Topic.direction_id == direction_id
                ).scalar() or 0
                if proposed_points_sum < 15:
                    points_to_add = min(5, 15 - proposed_points_sum)
                    update_user_points(user_id=proposed_by, points=points_to_add, action_type='题目被完成', topic_id=topic_id)

            # 更新认领人积分
            claimed_points_sum = db.session.query(func.sum(PointAction.points)).join(
                Topic, PointAction.topic_id == Topic.topic_id
            ).filter(
                PointAction.user_id == claimed_by,
                PointAction.action_type == '提交作品',
                Topic.direction_id == direction_id
            ).scalar() or 0
            if claimed_points_sum < 15:
                points_to_add = min(15, 15 - claimed_points_sum)
                update_user_points(user_id=claimed_by, points=points_to_add, action_type='提交作品', topic_id=topic_id)

        # 返回更新成功的消息和状态码
        return jsonify({'message': 'Topic updated successfully'}), 200
    except SQLAlchemyError as e:
        # 如果发生数据库错误，回滚事务并返回错误信息
        db.session.rollback()
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'message': 'Failed to update topic', 'error': str(e)}), 500


# 删除选题
def delete_topic_record(topic_id):
    """
    根据选题ID删除数据库中的选题记录。
    :param topic_id: 选题的唯一标识符
    :return: 成功或失败的JSON信息和状态码
    """
    try:
        topic = Topic.query.get(topic_id)
        if not topic:
            return jsonify({'message': 'Topic not found'}), 404

        db.session.delete(topic)
        db.session.commit()
        return jsonify({'message': 'Topic deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'message': 'Failed to delete topic', 'error': str(e)}), 500


# 统计加分次数
def get_direction_points_count(user_id, action_type, direction_id=None):
    """
    统计某用户在特定选题方向上的加分次数，基于指定的action类型。
    :param user_id: 用户ID
    :param action_type: 行为类型，例如“出题”或“提交作品”
    :param direction_id: 选题方向的唯一标识符，默认为None
    :return: 满足条件的加分记录的数量
    """
    topic_alias = aliased(Topic)

    query = db.session.query(PointAction).join(
        topic_alias, PointAction.topic_id == topic_alias.topic_id
    ).filter(
        PointAction.user_id == user_id,
        PointAction.action_type == action_type
    )

    # 如果提供了方向ID，添加筛选条件
    if direction_id:
        query = query.filter(topic_alias.direction_id == direction_id)

    return query.count()
