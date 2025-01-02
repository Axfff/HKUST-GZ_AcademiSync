# app/follows/routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Follow, Course
from sqlalchemy.exc import IntegrityError

follows_bp = Blueprint('follows', __name__)

@follows_bp.route('/courses/<int:course_id>', methods=['POST'])
@jwt_required()
def follow_course(course_id):
    user_id = get_jwt_identity()
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404

    existing_follow = Follow.query.filter_by(user_id=user_id, course_id=course_id).first()
    if existing_follow:
        return jsonify({'message': 'Already following the course.'}), 400

    new_follow = Follow(user_id=user_id, course_id=course_id)
    try:
        db.session.add(new_follow)
        db.session.commit()
        return jsonify({'message': 'Course followed successfully.'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Failed to follow course.'}), 400

@follows_bp.route('/courses/<int:course_id>', methods=['DELETE'])
@jwt_required()
def unfollow_course(course_id):
    user_id = get_jwt_identity()
    follow = Follow.query.filter_by(user_id=user_id, course_id=course_id).first()
    if not follow:
        return jsonify({'message': 'Follow not found.'}), 404

    try:
        db.session.delete(follow)
        db.session.commit()
        return jsonify({'message': 'Course unfollowed successfully.'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Failed to unfollow course.'}), 400




