# app/instructors/routes.py
from flask import Blueprint, jsonify, request
from ..models import db, Instructor, CourseInstructor, Course
from flask_jwt_extended import jwt_required

instructors_bp = Blueprint('instructors', __name__)

@instructors_bp.route('/<int:instructor_id>', methods=['GET'])
def get_instructor(instructor_id):
    instructor = Instructor.query.get(instructor_id)
    if not instructor:
        return jsonify({'message': 'Resource not found'}), 404

    courses = [{
        'id': ci.course.id,
        'course_code': ci.course.course_code,
        'name': ci.course.name,
        'description': ci.course.description,
        'created_at': ci.course.created_at.isoformat()
    } for ci in instructor.courses]

    instructor_data = {
        'id': instructor.id,
        'name': instructor.name,
        'profile_url': instructor.profile_url,
        'created_at': instructor.created_at.isoformat(),
        'courses': courses
    }
    return jsonify(instructor_data), 200

