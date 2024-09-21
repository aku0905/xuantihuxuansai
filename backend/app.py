from flask import Flask, request
from flask_cors import CORS

from routes.user_route import user_bp
from routes.topic_route import topic_bp
from routes.direction_route import direction_bp
from routes.reward_route import reward_bp
from routes.redemption_route import redemption_bp
from routes.pointactions_route import pointactions_bp

from backend.db import db
from config import Config


# 创建 Flask 应用
app = Flask(__name__)

# 加载配置
app.config.from_object(Config)

#  初始化实例对象
db.init_app(app)

# 允许跨域请求，支持凭证（cookies, HTTP认证等）
CORS(app, supports_credentials=True)

# 注册蓝图 (Blueprints)
app.register_blueprint(user_bp)
app.register_blueprint(topic_bp)
app.register_blueprint(direction_bp)
app.register_blueprint(reward_bp)
app.register_blueprint(redemption_bp)
app.register_blueprint(pointactions_bp)


# 定义根路径路由
@app.route('/')
def home():
    return "Welcome to the Flask API!"

# 允许多个来源进行跨域请求的处理
ALLOWED_ORIGINS = ['http://localhost:8082', 'http://127.0.0.1:5000']

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

if __name__ == '__main__':
    # 使用 app.app_context() 来确保数据库与应用程序上下文正确连接
    with app.app_context():
        db.create_all()  # 如果数据库表不存在，则创建它们
    app.run(debug=True, host='0.0.0.0')  # 设置为 0.0.0.0 以允许外部访问

