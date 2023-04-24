from flask import Flask, session, request, jsonify
from flask_migrate import Migrate
from config.db import db
from config.config import config
from controllers.post_controller import post
from controllers.user_controller import _user
from controllers.auth_controller import auth
from auth.manager import login_manager, current_user
from utils.utils import to_json
from ws import socketio
from flask_cors import CORS
import os
# from models.user.user_model import User
# from models.post.post_model import Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
CORS(app, supports_credentials=True, resources={
     r"/*": {"origins": "http://localhost:3000"}})

db.init_app(app)
login_manager.init_app(app)
socketio.init_app(app, cors_allowed_origins =["http://localhost:3000"])
Migrate(app, db)


@app.route('/')
def index():
    return "<p>Welcome to ashesi_net API</p>"


app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(_user, url_prefix="/users")
app.register_blueprint(post, url_prefix="/posts")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, debug=True, host='0.0.0.0', port=port)
