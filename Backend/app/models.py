# app/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import CheckConstraint, UniqueConstraint, func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    comments = db.relationship('Comment', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    follows = db.relationship('Follow', backref='user', lazy=True)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())

    instructors = db.relationship('CourseInstructor', backref='course', lazy=True)
    ratings = db.relationship('Rating', backref='course', lazy=True)
    comments = db.relationship('Comment', backref='course', lazy=True)
    follows = db.relationship('Follow', backref='course', lazy=True)

class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    profile_url = db.Column(db.Text, unique=True)
    created_at = db.Column(db.DateTime, default=func.now())

    courses = db.relationship('CourseInstructor', backref='instructor', lazy=True)
    # ratings = db.relationship('Rating', backref='instructor', lazy=True)

class CourseInstructor(db.Model):
    __tablename__ = 'course_instructors'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id', ondelete='CASCADE'), nullable=False)
    semester = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now())

    __table_args__ = (UniqueConstraint('course_id', 'instructor_id', 'semester', name='_course_instructor_semester_uc'),)

    ratings = db.relationship('Rating', backref='course_instructor', lazy=True)
    comments = db.relationship('Comment', backref='course_instructor', lazy=True)

class RatingDimension(db.Model):
    __tablename__ = 'rating_dimensions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())

    ratings = db.relationship('Rating', backref='rating_dimension', lazy=True)

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=True)
    course_instructor_id = db.Column(db.Integer, db.ForeignKey('course_instructors.id', ondelete='CASCADE'), nullable=True)
    rating_dimension_id = db.Column(db.Integer, db.ForeignKey('rating_dimensions.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    __table_args__ = (
        CheckConstraint('score >= 1 AND score <= 5', name='check_score_range'),
        # Enforce that either course_id or course_instructor_id is present, but not both
        CheckConstraint(
            '(course_id IS NOT NULL AND course_instructor_id IS NULL) OR (course_id IS NULL AND course_instructor_id IS NOT NULL)',
            name='check_course_or_instructor'
        ),
    )

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=True)
    course_instructor_id = db.Column(db.Integer, db.ForeignKey('course_instructors.id', ondelete='CASCADE'), nullable=True)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    children = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)
    likes = db.relationship('Like', backref='comment', lazy=True)

    __table_args__ = (
        CheckConstraint(
            '(course_id IS NOT NULL AND course_instructor_id IS NULL) OR (course_id IS NULL AND course_instructor_id IS NOT NULL)',
            name='check_comment_course_or_instructor'
        ),
    )

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    __table_args__ = (UniqueConstraint('user_id', 'comment_id', name='_user_comment_like_uc'),)

class Follow(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    __table_args__ = (UniqueConstraint('user_id', 'course_id', name='_user_course_follow_uc'),)

