from extensions import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import Users
from bcrypt import hashpw, gensalt, checkpw

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    if not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify(message='All fields required'), 400

    existing_user = Users.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify(message='Email already exists'), 400

    hashed_password = hashpw(data['password'].encode('utf-8'), gensalt())

    user = Users(
        username=data['username'],
        email=data['email'],
        password=hashed_password.decode('utf-8')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(message='User registered successfully'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = Users.query.filter_by(email= data.get('email')).first()

    if user and checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    return jsonify(message='Invalid credentials'), 401