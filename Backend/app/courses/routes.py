# app/courses/routes.py
from flask import Blueprint, jsonify, request
from ..models import db, Course, CourseInstructor, Instructor
from flask_jwt_extended import jwt_required

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    courses_list = [{
        'id': course.id,
        'course_code': course.course_code,
        'name': course.name,
        'description': course.description,
        'created_at': course.created_at.isoformat()
    } for course in courses]
    return jsonify(courses_list), 200

@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Resource not found'}), 404

    instructors = [{
        'course_instructor_id': ci.id,
        'id': ci.instructor.id,
        'name': ci.instructor.name,
        'profile_url': ci.instructor.profile_url,
        'created_at': ci.instructor.created_at.isoformat()
    } for ci in course.instructors]

    course_data = {
        'id': course.id,
        'course_code': course.course_code,
        'name': course.name,
        'unit': course.unit,
        'description': course.description,
        'created_at': course.created_at.isoformat(),
        'instructors': instructors
    }
    return jsonify(course_data), 200


@courses_bp.route('/search', methods=['GET'])
def search_courses():
    search_query = request.args.get('q', '').lower()  # Get the search query from the request (default to empty string if not provided)

    if not search_query:
        return jsonify({'message': 'No search query provided'}), 400

    # Search for courses by matching the keyword against course name, code, or description
    courses = Course.query.filter(
        (Course.name.ilike(f'%{search_query}%')) |  # Case-insensitive match for name
        (Course.course_code.ilike(f'%{search_query}%')) |  # Case-insensitive match for course code
        (Course.description.ilike(f'%{search_query}%'))  # Case-insensitive match for description
    ).all()

    courses_list = [{
        'id': course.id,
        'course_code': course.course_code,
        'name': course.name,
        'description': course.description,
        'created_at': course.created_at.isoformat()
    } for course in courses]

    return jsonify(courses_list), 200

