# app/comments/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Comment, Course, CourseInstructor
from sqlalchemy.exc import IntegrityError

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('', methods=['POST'])
@jwt_required()
def post_comment():
    data = request.get_json()
    user_id = get_jwt_identity()
    course_id = data.get('course_id')
    course_instructor_id = data.get('course_instructor_id')
    parent_comment_id = data.get('parent_comment_id')
    content = data.get('content')

    if not content:
        return jsonify({'message': 'Content is required.'}), 400

    if (course_id is None and course_instructor_id is None) or (course_id and course_instructor_id):
        return jsonify({'message': 'Provide either course_id or course_instructor_id, not both.'}), 400

    if parent_comment_id:
        parent = Comment.query.get(parent_comment_id)
        if not parent:
            return jsonify({'message': 'Parent comment not found.'}), 404

    # Validate course or course-instructor exists
    if course_id:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'message': 'Course not found.'}), 404
    if course_instructor_id:
        course_instructor = CourseInstructor.query.get(course_instructor_id)
        if not course_instructor:
            return jsonify({'message': 'Course-Instructor pair not found.'}), 404

    new_comment = Comment(
        user_id=user_id,
        course_id=course_id,
        course_instructor_id=course_instructor_id,
        parent_comment_id=parent_comment_id,
        content=content
    )

    try:
        db.session.add(new_comment)
        db.session.commit()
        comment_data = {
            'id': new_comment.id,
            'user_id': new_comment.user_id,
            'course_id': new_comment.course_id,
            'course_instructor_id': new_comment.course_instructor_id,
            'parent_comment_id': new_comment.parent_comment_id,
            'content': new_comment.content,
            'created_at': new_comment.created_at.isoformat()
        }
        return jsonify(comment_data), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Failed to post comment.'}), 400

@comments_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_comments(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Resource not found'}), 404

    comments = Comment.query.filter_by(course_id=course_id, parent_comment_id=None).all()
    comments_list = []

    for comment in comments:
        sub_comments = [{
            'id': sub.id,
            'user_id': sub.user_id,
            'course_id': sub.course_id,
            'course_instructor_id': sub.course_instructor_id,
            'parent_comment_id': sub.parent_comment_id,
            'content': sub.content,
            'created_at': sub.created_at.isoformat()
        } for sub in comment.children]

        comment_data = {
            'id': comment.id,
            'user_id': comment.user_id,
            'course_id': comment.course_id,
            'course_instructor_id': comment.course_instructor_id,
            'parent_comment_id': comment.parent_comment_id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'sub_comments': sub_comments
        }
        comments_list.append(comment_data)

    return jsonify(comments_list), 200

@comments_bp.route('/courses/<int:course_id>/instructors/<int:instructor_id>', methods=['GET'])
def get_course_instructor_comments(course_id, instructor_id):
    course_instructor = CourseInstructor.query.filter_by(course_id=course_id, instructor_id=instructor_id).first()
    if not course_instructor:
        return jsonify({'message': 'Resource not found'}), 404

    comments = Comment.query.filter_by(course_instructor_id=course_instructor.id, parent_comment_id=None).all()
    comments_list = []

    for comment in comments:
        sub_comments = [{
            'id': sub.id,
            'user_id': sub.user_id,
            'course_id': sub.course_id,
            'course_instructor_id': sub.course_instructor_id,
            'parent_comment_id': sub.parent_comment_id,
            'content': sub.content,
            'created_at': sub.created_at.isoformat()
        } for sub in comment.children]

        comment_data = {
            'id': comment.id,
            'user_id': comment.user_id,
            'course_id': comment.course_id,
            'course_instructor_id': comment.course_instructor_id,
            'parent_comment_id': comment.parent_comment_id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'sub_comments': sub_comments
        }
        comments_list.append(comment_data)

    return jsonify(comments_list), 200


