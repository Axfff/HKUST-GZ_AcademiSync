# app/utils.py
from passlib.hash import bcrypt

def hash_password(password):
    return bcrypt.hash(password)

def verify_password(password, password_hash):
    return bcrypt.verify(password, password_hash)

