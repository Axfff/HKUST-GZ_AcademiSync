# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .models import db
from flask import jsonify
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    # app/__init__.py (Add the following inside create_app function)
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Invalid input'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'message': 'Unauthorized'}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'message': 'Internal server error'}), 500

    # Register Blueprints
    from .auth.routes import auth_bp
    from .users.routes import users_bp
    from .courses.routes import courses_bp
    from .instructors.routes import instructors_bp
    from .ratings.routes import ratings_bp
    from .comments.routes import comments_bp
    from .likes.routes import likes_bp
    from .follows.routes import follows_bp

    app.register_blueprint(auth_bp, url_prefix='/v1/api/auth')
    app.register_blueprint(users_bp, url_prefix='/v1/api/users')
    app.register_blueprint(courses_bp, url_prefix='/v1/api/courses')
    app.register_blueprint(instructors_bp, url_prefix='/v1/api/instructors')
    app.register_blueprint(ratings_bp, url_prefix='/v1/api/ratings')
    app.register_blueprint(comments_bp, url_prefix='/v1/api/comments')
    app.register_blueprint(likes_bp, url_prefix='/v1/api/likes')
    app.register_blueprint(follows_bp, url_prefix='/v1/api/follows')

    return app



