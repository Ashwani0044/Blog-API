from flask import Flask
from extensions import db, jwt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key-1234567890abcdef'

db.init_app(app)
jwt.init_app(app)

from routes.auth import auth_bp
from routes.blog import blog_bp

app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

