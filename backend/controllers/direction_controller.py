from flask import jsonify
from backend.models.direction_model import Direction
from sqlalchemy.exc import SQLAlchemyError
from backend.db import db


# 获取所有方向
def get_directions():
    directions = Direction.query.all()
    directions_list = [{
        'direction_id': direction.direction_id,
        'direction_name': direction.direction_name,
        'start_date': direction.start_date,
        'end_date': direction.end_date,
        'description': direction.description
    } for direction in directions]

    return jsonify(directions_list), 200


# 获取单个方向
def get_direction(direction_id):
    direction = Direction.query.get(direction_id)
    if direction:
        return jsonify({
            'direction_id': direction.direction_id,
            'direction_name': direction.direction_name,
            'start_date': direction.start_date,
            'end_date': direction.end_date,
            'description': direction.description
        }), 200
    else:
        return jsonify({'message': 'Direction not found'}), 404


# 创建新方向
def create_new_direction(data):
    try:
        new_direction = Direction(
            direction_name=data['direction_name'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            description=data.get('description')
        )
        db.session.add(new_direction)
        db.session.commit()
        return jsonify({'message': 'Direction created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create direction', 'error': str(e)}), 500


# 更新现有方向
def update_existing_direction(direction_id, data):
    direction = Direction.query.get(direction_id)
    if not direction:
        return jsonify({'message': 'Direction not found'}), 404

    try:
        direction.direction_name = data.get('direction_name', direction.direction_name)
        direction.start_date = data.get('start_date', direction.start_date)
        direction.end_date = data.get('end_date', direction.end_date)
        direction.description = data.get('description', direction.description)

        db.session.commit()
        return jsonify({'message': 'Direction updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update direction', 'error': str(e)}), 500


# 删除方向
def delete_direction_record(direction_id):
    direction = Direction.query.get(direction_id)
    if not direction:
        return jsonify({'message': 'Direction not found'}), 404

    try:
        db.session.delete(direction)
        db.session.commit()
        return jsonify({'message': 'Direction deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete direction', 'error': str(e)}), 500
