from flask import Flask
from flask_migrate import Migrate 
from extensions import db, jwt
from dotenv import load_dotenv
import os;

app = Flask(__name__)
migrate = Migrate(app, db)
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
@app.route('/')
def home():
    return "Welcome to the Blog API!"


db.init_app(app)
jwt.init_app(app)

from routes.auth import auth_bp
from routes.blog import blog_bp
from routes.ai import ai_bp

app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(ai_bp, url_prefix='/ai')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)

