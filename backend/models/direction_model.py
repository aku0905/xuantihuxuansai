from backend.db import db  # 引入全局的 db 实例，而不是重新创建 SQLAlchemy 实例


class Direction(db.Model):
    __tablename__ = 'topic_directions'
    direction_id = db.Column(db.Integer, primary_key=True)
    direction_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)

# 获取所有方向
def get_all_directions():
    return Direction.query.all()

# 根据 direction_id 获取特定方向
def get_direction_by_id(direction_id):
    return Direction.query.get(direction_id)

# 创建新的方向
def create_direction(data):
    new_direction = Direction(
        direction_name=data['direction_name'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(new_direction)
    db.session.commit()

# 更新现有的方向
def update_direction(direction_id, data):
    direction = Direction.query.get(direction_id)
    if direction:
        direction.direction_name = data.get('direction_name', direction.direction_name)
        direction.start_date = data.get('start_date', direction.start_date)
        direction.end_date = data.get('end_date', direction.end_date)
        db.session.commit()

# 删除方向
def delete_direction(direction_id):
    direction = Direction.query.get(direction_id)
    if direction:
        db.session.delete(direction)
        db.session.commit()
