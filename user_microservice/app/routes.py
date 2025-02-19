from flask import Blueprint, jsonify, request
from flask import current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from .models import User
from . import db, limiter, cache
import logging

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Log the request payload for debugging
    logging.info(f"Login request data: {data}")

    # Validate that username and password are provided
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data['username']
    password = data['password']

    # Log the extracted username and password
    logging.info(f"Extracted username: {username}, password: {password}")

    user = User.query.filter_by(username=username).first()
    if user:
        # Log the user's password hash for debugging
        logging.info(f"User's password hash: {user.password_hash}")

        if user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            return jsonify(access_token=access_token), 200
        else:
            logging.error("Invalid password")
    else:
        logging.error("User not found")

    return jsonify({"error": "Invalid credentials"}), 401

@bp.route('/users', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)  # Cache for 60 seconds
@jwt_required()
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = User.query.paginate(page=page, per_page=per_page)
    return jsonify({
        'users': [{'id': user.id, 'username': user.username, 'email': user.email} for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    })

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    current_app.logger.info(f'Creating user: {data["username"]}')
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201

@bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@bp.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({
        "error": e.name,
        "message": e.description,
    }), e.code

@bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": "Resource not found"}), 404

@bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": "Something went wrong"}), 500