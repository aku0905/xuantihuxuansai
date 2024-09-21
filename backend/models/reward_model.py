from backend.db import db
from datetime import datetime

class Reward(db.Model):
    __tablename__ = 'rewards'

    # 允许扩展现有的表
    __table_args__ = {'extend_existing': True}

    reward_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 商品唯一标识符，自增主键
    name = db.Column(db.String(255), nullable=False)  # 商品名称
    description = db.Column(db.Text)  # 商品描述
    points_required = db.Column(db.Integer, nullable=False)  # 所需积分
    stock = db.Column(db.Integer, nullable=False)  # 商品库存
    image_url = db.Column(db.String(255))  # 商品图片的URL链接
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)  # 商品创建时间，默认当前时间

    def __init__(self, name, description, points_required, stock, image_url=None):
        self.name = name
        self.description = description
        self.points_required = points_required
        self.stock = stock
        self.image_url = image_url

    def to_dict(self):
        """Convert the reward object to a dictionary for easy serialization."""
        return {
            'reward_id': self.reward_id,
            'name': self.name,
            'description': self.description,
            'points_required': self.points_required,
            'stock': self.stock,
            'image_url': self.image_url,
            'created_at': self.created_at
        }
