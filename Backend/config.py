# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://backend_user:dev_password@localhost/academisync')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev_jwt_secret_key')

    HUNTER_API_KEY = 'hunter_api_key'
    HUNTER_API_URL = 'https://api.hunter.io/v2/email-verifier'

    PERMITTED_EMAIL_DOMAINS = ['university.edu.cn']
    TEST_ACCOUNTS = ['teststudent@university.edu']


