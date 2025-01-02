# app/users/routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Follow


users_bp = Blueprint('users', __name__)

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    # user_id = str(user_id)
    # print(type(user_id), user_id)
    user = User.query.get(user_id)
    if user:
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'created_at': user.created_at.isoformat()
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found.'}), 404



@users_bp.route('/me/followed-courses', methods=['GET'])
@jwt_required()
def get_followed_courses():
    user_id = get_jwt_identity()
    follows = Follow.query.filter_by(user_id=user_id).all()
    courses = [{
        'id': follow.course.id,
        'course_code': follow.course.course_code,
        'name': follow.course.name,
        'description': follow.course.description,
        'created_at': follow.course.created_at.isoformat()
    } for follow in follows]
    return jsonify(courses), 200
