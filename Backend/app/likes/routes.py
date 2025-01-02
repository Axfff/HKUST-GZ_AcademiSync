# app/likes/routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Like, Comment
from sqlalchemy.exc import IntegrityError

likes_bp = Blueprint('likes', __name__)

@likes_bp.route('/comments/<int:comment_id>', methods=['POST'])
@jwt_required()
def like_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found.'}), 404

    existing_like = Like.query.filter_by(user_id=user_id, comment_id=comment_id).first()
    if existing_like:
        return jsonify({'message': 'Already liked.'}), 400

    new_like = Like(user_id=user_id, comment_id=comment_id)
    try:
        db.session.add(new_like)
        db.session.commit()
        like_count = Like.query.filter_by(comment_id=comment_id).count()
        return jsonify({'like_count': like_count}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Failed to like comment.'}), 400

@likes_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def unlike_comment(comment_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(user_id=user_id, comment_id=comment_id).first()
    if not like:
        return jsonify({'message': 'Like not found.'}), 404

    try:
        db.session.delete(like)
        db.session.commit()
        like_count = Like.query.filter_by(comment_id=comment_id).count()
        return jsonify({'like_count': like_count}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Failed to unlike comment.'}), 400


