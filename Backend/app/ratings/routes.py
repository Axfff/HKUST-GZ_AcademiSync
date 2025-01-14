# app/ratings/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Rating, RatingDimension, Course, CourseInstructor
from sqlalchemy.exc import IntegrityError

ratings_bp = Blueprint('ratings', __name__)

@ratings_bp.route('', methods=['POST'])
@jwt_required()
def submit_rating():
    data = request.get_json()
    user_id = get_jwt_identity()
    course_id = data.get('course_id')
    course_instructor_id = data.get('course_instructor_id')
    ratings = data.get('ratings')

    if (course_id is None and course_instructor_id is None) or (course_id and course_instructor_id):
        return jsonify({'message': 'Provide either course_id or course_instructor_id, not both.'}), 400

    if not ratings or not isinstance(ratings, list):
        return jsonify({'message': 'Ratings must be a list of rating inputs.'}), 400

    # Validate course or course-instructor exists
    if course_id:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'message': 'Course not found.'}), 404
    if course_instructor_id:
        course_instructor = CourseInstructor.query.get(course_instructor_id)
        if not course_instructor:
            return jsonify({'message': 'Course-Instructor pair not found.'}), 404

    # Process each rating
    for rating_input in ratings:
        dimension_id = rating_input.get('rating_dimension_id')
        score = rating_input.get('score')

        if not dimension_id or not score:
            return jsonify({'message': 'Each rating must have a rating_dimension_id and score.'}), 400

        if not (1 <= score <= 5):
            return jsonify({'message': 'Score must be between 1 and 5.'}), 400

        # Check if rating dimension exists
        dimension = RatingDimension.query.get(dimension_id)
        if not dimension:
            return jsonify({'message': f'Rating dimension {dimension_id} not found.'}), 404

        # Optionally, enforce one rating per user per dimension per course/course-instructor
        existing_rating = Rating.query.filter_by(
            user_id=user_id,
            rating_dimension_id=dimension_id,
            course_id=course_id,
            course_instructor_id=course_instructor_id
        ).first()
        if existing_rating:
            existing_rating.score = score
        else:
            new_rating = Rating(
                user_id=user_id,
                rating_dimension_id=dimension_id,
                score=score,
                course_id=course_id,
                course_instructor_id=course_instructor_id
            )
            db.session.add(new_rating)

    try:
        db.session.commit()
        return jsonify({'message': 'Ratings submitted successfully.'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Failed to submit ratings.'}), 400

@ratings_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_ratings(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Resource not found'}), 404

    dimensions = RatingDimension.query.all()
    ratings_data = []

    for dimension in dimensions:
        avg_score = db.session.query(db.func.avg(Rating.score)).filter(
            Rating.course_id == course_id,
            Rating.rating_dimension_id == dimension.id
        ).scalar()
        avg_score = round(avg_score, 2) if avg_score else None
        ratings_data.append({
            'dimension_id': dimension.id,
            'dimension_name': dimension.name,
            'average_score': avg_score
        })

    response = {
        'course_id': course_id,
        'ratings': ratings_data
    }
    return jsonify(response), 200

@ratings_bp.route('/courses/<int:course_id>/instructors/<int:instructor_id>', methods=['GET'])
def get_course_instructor_ratings(course_id, instructor_id):
    course_instructor = CourseInstructor.query.filter_by(course_id=course_id, instructor_id=instructor_id).first()
    if not course_instructor:
        return jsonify({'message': 'Resource not found'}), 404

    dimensions = RatingDimension.query.all()
    ratings_data = []

    for dimension in dimensions:
        avg_score = db.session.query(db.func.avg(Rating.score)).filter(
            Rating.course_instructor_id == course_instructor.id,
            Rating.rating_dimension_id == dimension.id
        ).scalar()
        avg_score = round(avg_score, 2) if avg_score else None
        ratings_data.append({
            'dimension_id': dimension.id,
            'dimension_name': dimension.name,
            'average_score': avg_score
        })

    response = {
        'course_instructor_id': course_instructor.id,
        'ratings': ratings_data
    }
    return jsonify(response), 200

@ratings_bp.route('/my-ratings', methods=['GET'])
@jwt_required()
def get_my_ratings():
    user_id = get_jwt_identity()
    course_id = request.args.get('course_id', type=int)
    course_instructor_id = request.args.get('course_instructor_id', type=int)

    if (course_id is None and course_instructor_id is None) or (course_id and course_instructor_id):
        return jsonify({'message': 'Provide either course_id or course_instructor_id, not both.'}), 400

    # Validate course or course-instructor exists
    if course_id:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'message': 'Course not found.'}), 404
    if course_instructor_id:
        course_instructor = CourseInstructor.query.get(course_instructor_id)
        if not course_instructor:
            return jsonify({'message': 'Course-Instructor pair not found.'}), 404

    dimensions = RatingDimension.query.all()
    ratings_data = []

    for dimension in dimensions:
        rating = Rating.query.filter_by(
            user_id=user_id,
            rating_dimension_id=dimension.id,
            course_id=course_id,
            course_instructor_id=course_instructor_id
        ).first()

        ratings_data.append({
            'dimension_id': dimension.id,
            'dimension_name': dimension.name,
            'score': rating.score if rating else None
        })

    response = {
        'course_id': course_id,
        'course_instructor_id': course_instructor_id,
        'ratings': ratings_data
    }
    return jsonify(response), 200
