# config.py
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://backend_user:dev_password@localhost/academisync'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev_jwt_secret_key')

    HUNTER_API_KEY = os.environ.get('HUNTER_API_KEY', 'default_hunter_api_key')
    HUNTER_API_URL = os.environ.get('HUNTER_API_URL', 'https://api.hunter.io/v2/email-verifier')

    PERMITTED_EMAIL_DOMAINS = os.environ.get(
        'PERMITTED_EMAIL_DOMAINS',
        'school_email_domain.edu'
    ).split(',')

    TEST_ACCOUNTS = os.environ.get(
        'TEST_ACCOUNTS',
        'teststudent@university.edu'
    ).split(',')