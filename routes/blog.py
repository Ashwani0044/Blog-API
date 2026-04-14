from extensions import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Posts
from datetime import datetime

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():

    data = request.json
    user_id = int(get_jwt_identity())

    post = Posts(user_id=user_id, title=data['title'], content=data['content'], created_at=datetime.utcnow())
    db.session.add(post)
    db.session.commit()
    return jsonify(message='Post created successfully'), 201

@blog_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    user_id = int(get_jwt_identity())
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
    except (TypeError, ValueError):
        return jsonify(message='page and per_page must be integers'), 400

    if page < 1 or per_page < 1:
        return jsonify(message='page and per_page must be positive integers'), 400

    pagination = Posts.query.filter_by(user_id=user_id).order_by(Posts.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items

    return jsonify(
        posts=[
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at.isoformat() if post.created_at else None,
            }
            for post in posts
        ],
        meta={
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
        },
    )

@blog_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    data = request.json
    user = int(get_jwt_identity())
    post = Posts.query.filter_by(id=post_id, user_id=user).first()
    if not post:
        return jsonify(message='Post not found'), 404
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify(message='Post updated successfully')

@blog_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user = int(get_jwt_identity())
    post = Posts.query.filter_by(id=post_id, user_id=user).first()
    if not post:
        return jsonify(message='Post not found'), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify(message='Post deleted successfully')

@blog_bp.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    user = int(get_jwt_identity())
    post = Posts.query.filter_by(id=post_id, user_id=user).first()
    if not post:
        return jsonify(message='Post not found'), 404
    return jsonify(id=post.id, title=post.title, content=post.content, created_at=post.created_at)
