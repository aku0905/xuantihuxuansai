# user_model.py

from backend.db import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    total_points = db.Column(db.Integer, default=0)
    available_points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<User {self.user_id} - {self.username}>"

# 根据用户名获取用户
# 该函数通过用户名查询数据库，返回第一个匹配的用户对象
# 参数:
#   username (str): 需要查询的用户名
# 返回:
#   User: 匹配的用户对象，如果没有找到则返回None
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

# 创建新用户
def create_user(data):
    new_user = User(
        username=data['username'],
        password=data['password'],
    )
    db.session.add(new_user)
    db.session.commit()

# 更新用户
def update_user(user_id, data):
    user = User.query.get(user_id)
    if user:
        user.username = data.get('username', user.username)
        user.password = data.get('password', user.password)
        db.session.commit()

# 删除用户
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()


# 根据用户ID获取用户名
# 该函数通过用户ID查询数据库，返回对应的用户名
# 参数:
#   user_id (int): 需要查询的用户ID
# 返回:
#   str: 对应的用户名，如果没有找到则返回None
def get_username_by_user_id(user_id):
    user = User.query.get(user_id)
    if user:
        return user.username
    else:
        return None
