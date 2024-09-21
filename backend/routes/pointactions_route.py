# pointactions_route.py

from flask import Blueprint, request, jsonify
from backend.controllers.pointactions_controcall import get_user_point_actions
from backend.middleware import token_required

pointactions_bp = Blueprint('pointactions', __name__)

# 获取用户积分记录的路由
@pointactions_bp.route('/records', methods=['GET'])
@token_required
def records(user_id):
    return get_user_point_actions(user_id)
