from extensions import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Follows, Posts, Comments, Likes
from datetime import datetime

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():

    data = request.json
    user_id = int(get_jwt_identity())

    if not data.get('title') or not data.get('content'):
        return jsonify(message='Title and content required'), 400

    post = Posts(user_id=user_id, title=data['title'], content=data['content'], created_at=datetime.utcnow(), image_url=data.get('image_url'))
    db.session.add(post)
    db.session.commit()
    return jsonify(message='Post created successfully'), 201

@blog_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    user_id = int(get_jwt_identity())

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')

    if page < 1 or per_page < 1:
        return jsonify(message='page and per_page must be positive integers'), 400

    per_page = min(per_page, 50)

    query = Posts.query.filter_by(user_id=user_id)

    if search:
        query = query.filter(Posts.title.ilike(f"%{search}%"))

    pagination = query.order_by(Posts.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        data=[
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at.isoformat() if post.created_at else None,
                'likes': Likes.query.filter_by(post_id=post.id).count(),
                'comments': Comments.query.filter_by(post_id=post.id).count(),
                'image_url': post.image_url
            }
            for post in pagination.items
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

    if not data.get('title') or not data.get('content'):
        return jsonify(message='Title and content required'), 400
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
    return jsonify(id=post.id, title=post.title, content=post.content,
                    created_at=post.created_at.isoformat() if post.created_at else None,
                      image_url=post.image_url)


# Comments routes

@blog_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    user_id = int(get_jwt_identity())
    data = request.json

    if not data.get('content'):
        return jsonify(message='Content required'), 400

    post = Posts.query.get(post_id)
    if not post:
        return jsonify(message='Post not found'), 404

    comment = Comments(
        content=data['content'],
        user_id=user_id,
        post_id=post_id
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify(message='Comment added'), 201

@blog_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    post = Posts.query.get(post_id)
    if not post:
        return jsonify(message='Post not found'), 404

    comments = Comments.query.filter_by(post_id=post_id).order_by(Comments.created_at.desc()).all()

    return jsonify([
        {
            "id": c.id,
            "content": c.content,
            "user_id": c.user_id,
            "created_at": c.created_at.isoformat()
        }
        for c in comments
    ])

@blog_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    user_id = int(get_jwt_identity())
    data = request.json

    comment = Comments.query.filter_by(id=comment_id, user_id=user_id).first()
    if not comment:
        return jsonify(message='Comment not found'), 404

    comment.content = data.get('content', comment.content)
    db.session.commit()

    return jsonify(message='Comment updated')

@blog_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = int(get_jwt_identity())

    comment = Comments.query.filter_by(id=comment_id, user_id=user_id).first()
    if not comment:
        return jsonify(message='Comment not found'), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify(message='Comment deleted')


# Likes routes
@blog_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def toggle_like(post_id):
    user_id = int(get_jwt_identity())
    post = Posts.query.get(post_id)
    if not post:
        return jsonify(message='Post not found'), 404
    
    existing_like = Likes.query.filter_by(user_id=user_id, post_id=post_id).first()

    if(existing_like):
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify(message='Post unliked')
    
    like = Likes(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    return jsonify(message='Post liked')

@blog_bp.route('/posts/<int:post_id>/likes', methods=['GET'])
def get_likes(post_id):
    count = Likes.query.filter_by(post_id=post_id).count()
    return jsonify(post_id=post_id, likes=count)

# Follow routes

@blog_bp.route('/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def toggle_follow(user_id):
    current_user_id = int(get_jwt_identity())

    if current_user_id == user_id:
        return jsonify(message='You cannot follow yourself'), 400
    
    existing_follow = Follows.query.filter_by(follower_id=current_user_id, followed_id=user_id).first()

    if existing_follow:
        db.session.delete(existing_follow)
        db.session.commit()
        return jsonify(message='User unfollowed')
    
    follow = Follows(follower_id=current_user_id, followed_id=user_id)
    db.session.add(follow)
    db.session.commit()
    return jsonify(message='User followed')

@blog_bp.route('/users/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):

    # followers_count = Follows.query.filter_by(followed_id=user_id).count()
    # return jsonify(user_id=user_id, followers=followers_count)
    followers = Follows.query.filter_by(followed_id=user_id).all()
    return jsonify(user_id=user_id, followers=[
    {"user_id": f.follower_id}
    for f in followers
])

@blog_bp.route('/users/<int:user_id>/following', methods=['GET'])
def get_following(user_id):
    following = Follows.query.filter_by(follower_id=user_id).all()
    return jsonify(user_id=user_id, following=[
        {"user_id": f.followed_id}
        for f in following
    ])


# feed logic 
@blog_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if page < 1 or per_page < 1:
        return jsonify(message='page and per_page must be positive integers'), 400

    per_page = min(per_page, 50)

    followed_users = Follows.query.filter_by(follower_id=user_id).with_entities(Follows.followed_id).subquery()

    pagination = Posts.query.filter(Posts.user_id.in_(followed_users) | Posts.user_id == user_id).order_by(Posts.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        data=[
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at.isoformat() if post.created_at else None,
                'likes': Likes.query.filter_by(post_id=post.id).count(),
                'comments': Comments.query.filter_by(post_id=post.id).count(),
            }
            for post in pagination.items
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