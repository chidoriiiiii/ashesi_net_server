from flask_login import LoginManager, current_user
from models.user.user_model import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()
