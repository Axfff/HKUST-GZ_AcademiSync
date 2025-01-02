# app/auth/routes.py
import requests
from flask import Blueprint, request, jsonify
from ..models import db, User
from ..utils import hash_password, verify_password
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from config import Config

auth_bp = Blueprint('auth', __name__)

def is_email_permitted(email: str) -> bool:
    """
    Check if the given email address is either in the list of test accounts
    or belongs to a permitted domain.

    Args:
        email (str): The email address to check.

    Returns:
        bool: True if the email is a test account or its domain is in the permitted list, False otherwise.
    """
    # Check if the email is in the test accounts
    if email in Config.TEST_ACCOUNTS:
        return True

    try:
        # Extract domain from the email address
        domain = email.split('@')[1]
        # Check if the domain is in the permitted list
        return domain in Config.PERMITTED_EMAIL_DOMAINS
    except IndexError:
        # Handle cases where the email is malformed (e.g., no @ symbol)
        return False

def verify_email_with_hunter(email):
    """Function to verify email using Hunter.io API."""
    # Check if the email is in the test accounts
    if email in Config.TEST_ACCOUNTS:
        return True

    params = {
        'email': email,
        'api_key': Config.HUNTER_API_KEY
    }
    response = requests.get(Config.HUNTER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data') and data['data']['status'] == 'valid':
            return True
    return False

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password_hash = data.get('password_hash')
    name = data.get('name')

    if not email or not password_hash or not name:
        return jsonify({'message': 'Missing required fields.'}), 400

    # Check whether email is permitted
    if not is_email_permitted(email):
        return jsonify({'message': 'Please use a school email address for registration. Registration is not available if you are not an official student.'}), 400

    # Check if the username already exists
    if User.query.filter_by(name=name).first():
        return jsonify({'message': 'Username already taken. Please choose another one.'}), 400

    # Check email validity using Hunter.io
    if not verify_email_with_hunter(email):
        return jsonify({'message': 'Invalid or non-existent email.'}), 400

    # Proceed with user registration if email and username are valid
    new_user = User(email=email, password_hash=password_hash, name=name)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registration successful.'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Email already exists.'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password_hash = data.get('password_hash')

    if not email or not password_hash:
        return jsonify({'message': 'Missing email or password_hash.'}), 400

    user = User.query.filter_by(email=email).first()
    if user and password_hash == user.password_hash:
        token = create_access_token(identity=str(user.id))
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'created_at': user.created_at.isoformat()
        }
        return jsonify({'token': token, 'user': user_data}), 200
    else:
        return jsonify({'message': 'Invalid email or password_hash.'}), 401
