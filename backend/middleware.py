# 文件解释：
#   定义了一个名为 token_required 的装饰器，用于在 Flask 应用程序中实现基于
#   JSON Web Token (JWT) 的身份验证机制。它检查请求头中的 Authorization
#   字段以获取 JWT，并使用预定义的 SECRET_KEY 来验证和解码 token。如果 token 有效，
#   装饰器将允许请求继续到被保护的路由；如果无效或缺失，将返回一个错误响应。


import jwt
from functools import wraps
from flask import request, jsonify

# 秘钥，用于解码 JWT
SECRET_KEY = "your_secret_key"

# token_required 装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 从请求头中获取 token
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # "Bearer <token>"
            print(f"Token received: {token}")
        else:
            print("No token found in headers")

        # 如果请求头中没有 token，则返回 401 错误
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # 解码 token 并提取用户信息（如 user_id）
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data['user_id']  # 假设 token 中存储了 user_id
            print(f"Decoded user_id: {user_id}")
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        # 将提取到的 user_id 传递给被装饰的函数
        return f(user_id, *args, **kwargs)

    return decorated
