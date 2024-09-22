from flask import jsonify
from sqlalchemy.orm import joinedload
from werkzeug.debug import console

from backend.controllers.pointactions_controcall import update_user_points,delete_user_point_action
from backend.models.topic_model import Topic

from backend.db import db
from sqlalchemy.sql import func
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from backend.models.user_model import User
from backend.models.pointaction_model import PointAction
from backend.models.topic_model import Topic


# 获取当前选题方向的题目
def get_current_topics_by_direction(direction_id):
    try:
        current_topics = Topic.query.filter_by(direction_id=direction_id) \
            .options(joinedload(Topic.proposed_by_user), joinedload(Topic.claimed_by_user)).all()

        result = []
        for topic in current_topics:
            result.append({
                'topic_id': topic.topic_id,
                'direction_id': topic.direction_id,
                'topic_name': topic.topic_name,
                'topic_description': topic.topic_description,
                'proposed_by': topic.proposed_by,
                'proposed_by_username': topic.proposed_by_user.username if topic.proposed_by_user else None,  # 返回用户名
                'claimed_by': topic.claimed_by,
                'claimed_by_username': topic.claimed_by_user.username if topic.claimed_by_user else None,    # 返回认领者用户名
                'submission_link': topic.submission_link,
                'status': topic.status,
                'submitted_at': topic.submitted_at
            })
        return jsonify(result), 200
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch topics', 'error': str(e)}), 500


# 创建新选题
def create_new_topic(data):
    """
    根据传入的数据创建一个新的选题，并将其保存到数据库中，并根据规则为用户加积分。
    """
    try:
        # 验证必填字段
        required_fields = ['direction_id', 'topic_name', 'topic_description', 'proposed_by', 'status']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400  # 返回400错误

        # 创建 Topic 实例
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

        # 获取提出者ID和新创建的topic_id
        proposed_by = data['proposed_by']
        topic_id = new_topic.topic_id  # 获取新插入的topic_id

        # 查询用户本周出题的加分记录
        current_week_topics = PointAction.query.filter(
            PointAction.user_id == proposed_by,
            PointAction.action_type == '出题',
            func.week(PointAction.created_at) == func.week(func.now())
        ).count()

        # 如果本周出题次数未超过3次，则调用封装好的函数增加2积分
        if current_week_topics < 3:
            update_user_points(user_id=proposed_by, points=2, action_type='出题', topic_id=topic_id)

        return jsonify({'message': 'Topic created successfully', 'id': new_topic.topic_id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()  # 回滚数据库会话
        print(f"SQLAlchemy Error: {str(e)}")  # 打印详细错误信息
        return jsonify({'message': 'Failed to create topic', 'error': str(e)}), 500

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")  # 捕获其他异常并打印错误
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500



# 获取所有选题，并返回认领用户和提出者的用户名而不是ID
def get_all_topics():
    try:
        topics = Topic.query.all()
        result = []
        for topic in topics:
            # 初始化认领者和提出者用户名为 None
            claimed_by_username = None
            proposed_by_username = None

            # 获取认领者用户名
            if topic.claimed_by:
                # 通过用户名查找
                user = User.query.get(topic.claimed_by)
                if user:
                    claimed_by_username = user.username  # 使用用户名 # 调试信息

            # 获取提出者用户名
            if topic.proposed_by:
                # 通过 proposed_by 字段的用户ID获取对应的用户名
                proposer = User.query.get(topic.proposed_by)
                if proposer:
                    proposed_by_username = proposer.username  # 获取用户名

            result.append({
                'topic_id': topic.topic_id,
                'direction_id': topic.direction_id,
                'topic_name': topic.topic_name,
                'topic_description': topic.topic_description,
                'proposed_by': proposed_by_username,  # 返回用户名而不是ID
                'claimed_by': claimed_by_username,    # 返回用户名而不是ID
                'submission_link': topic.submission_link,
                'status': topic.status,
                'submitted_at': topic.submitted_at
            })

        return jsonify(result), 200
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch topics', 'error': str(e)}), 500


# 根据 topic_id 获取特定的选题
def get_topic_by_id(topic_id):
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
    try:
        topic = Topic.query.get(topic_id)
        if not topic:
            return jsonify({'message': 'Topic not found'}), 404

        # 更新选题字段
        topic.direction_id = data.get('direction_id', topic.direction_id)
        topic.topic_name = data.get('topic_name', topic.topic_name)
        topic.topic_description = data.get('topic_description', topic.topic_description)
        topic.proposed_by = data.get('proposed_by', topic.proposed_by)
        topic.claimed_by = data.get('claimed_by', topic.claimed_by)
        topic.submission_link = data.get('submission_link', topic.submission_link)
        topic.status = data.get('status', topic.status)

        # 提交选题的更新
        db.session.commit()

        # 获取提出者和认领者ID
        proposed_by = topic.proposed_by
        claimed_by = topic.claimed_by

        #取消选题时
        # 检查是否取消选题操作
        if data.get('claimed_by') is None and data.get('status') == '待认领':
            proposed_by = topic.proposed_by

            # 查询用户本周出题次数
            current_week_topics = Topic.query.filter(
                Topic.proposed_by == proposed_by,
                Topic.claimed_by.is_(None),# 选题状态更改为待认领
                func.week(Topic.created_at) == func.week(func.now())
            ).count()

            # 如果用户本周出题少于等于3次，则增加2积分
            if current_week_topics <= 3:
                update_user_points(user_id=proposed_by, points=2, action_type='出题', topic_id=topic_id)

        # 认领题目时
        # 如果认领人与提出者相同，则删除该题目于出题人的出题加分记录，同时扣除之前的出题所加积分
        if data.get('claimed_by') and proposed_by == claimed_by:
            # 查询用户本周出题且待认领数量
            current_week_topics = Topic.query.filter(
                Topic.proposed_by == proposed_by,
                Topic.claimed_by.is_(None), # 选题状态为待认领
                func.week(Topic.created_at) == func.week(func.now())
            ).count()
            # 如果用户本周出题且待认领数量少于等于3次，则删除加分记录并扣除积分
            if current_week_topics < 3:
                # 删除加分记录
                delete_user_point_action(user_id=claimed_by, topic_id=topic_id)
                # 更新用户积分
                user = User.query.get(claimed_by)
                user.available_points -= 2
                user.total_points -= 2

                db.session.add(user)
                db.session.commit()

        # 提交作品时为提出者和认领者加分
        if data.get('submission_link'):

            # 提出者加分
            # 查询该题目是否已经被提交过
            previous_submission = PointAction.query.filter_by(topic_id=topic_id, action_type='题目被完成').first()

            # 如果提出者不等于认领者，才能加分
            if proposed_by != claimed_by:
                # 查询提出者本周累计加分是否超过15分
                if not previous_submission:
                    current_week_proposed_points = db.session.query(func.sum(PointAction.points)).filter(
                        PointAction.user_id == proposed_by,
                        PointAction.action_type == '题目被完成',
                        func.week(PointAction.created_at) == func.week(func.now())
                    ).scalar() or 0 # 使用 scalar() 获取聚合值，防止 None

                    # 如果提出者的本周积分未超过15分，则增加5分
                    if current_week_proposed_points < 15:
                        points_to_add = min(5, 15 - current_week_proposed_points)
                        update_user_points(user_id=proposed_by, points=points_to_add, action_type='题目被完成', topic_id=topic_id)

            #认领者加分
            # 查询认领者本周累计加分是否超过15分
            current_week_claimed_points = db.session.query(func.sum(PointAction.points)).filter(
                PointAction.user_id == claimed_by,
                PointAction.action_type == '提交作品',
                func.week(PointAction.created_at) == func.week(func.now())
            ).scalar() or 0  # 使用 scalar() 获取聚合值，防止 None

            # 如果认领者的本周积分未超过15分，则增加15分
            if current_week_claimed_points < 15:
                points_to_add = min(15, 15 - current_week_claimed_points)
                update_user_points(user_id=claimed_by, points=points_to_add, action_type='提交作品', topic_id=topic_id)

        return jsonify({'message': 'Topic updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"SQLAlchemy Error: {str(e)}")
        return jsonify({'message': 'Failed to update topic', 'error': str(e)}), 500


# 删除选题
def delete_topic_record(topic_id):
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
