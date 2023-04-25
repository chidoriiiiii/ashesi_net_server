from flask import Blueprint, redirect, request, session, jsonify
from config.config import config
from config.db import db
from utils.utils import to_json
from auth.oauth import oauth
from models.user.user_model import User
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['POST'])
def login():
    req = json.loads(request.data)

    email_address = req.get('email_address')
    password = req.get('password')

    user_exists = User.query.filter_by(email_address=email_address).first()
    if not user_exists:
        return {"msg": f"Error user with email {email_address} doesn't exist"}, 404

    if check_password_hash(
            pwhash=user_exists.password_hash, password=password):
        login_user(user_exists)
        return to_json(user_exists), 200


@auth.route("/signup", methods=['POST'])
def signup():
    req = json.loads(request.data)

    email_address = req.get('email_address')
    student_id = req.get('student_id')
    username = req.get('username')
    password = req.get('password')

    user_exists = User.query.filter_by(email_address=email_address).first()
    if user_exists:
        return {"msg": f"Error user with email {email_address} already exists"}, 400

    password_hash = generate_password_hash(password=password, method='sha256')
    me = User(
        student_id = student_id,
        email_address=email_address,
        username=username,
        password_hash=password_hash,
        avatar_url = 'https://cdn.dribbble.com/users/6142/screenshots/5679189/media/1b96ad1f07feee81fa83c877a1e350ce.png?compress=1&resize=400x300&vertical=top'
        )
    db.session.add(me)
    db.session.commit()

    login_user(me)

    return to_json(me), 200


@auth.route("/microsoft")
def auth_microsoft():
    microsoft = oauth.microsoft
    microsoft_callback = config.MICROSOFT_CALLBACK
    return microsoft.authorize_redirect(microsoft_callback)


@auth.route("/microsoft/callback")
def auth_microsoft_callback():
    microsoft = oauth.microsoft
    token = microsoft.authorize_access_token()
    user_info = token['userinfo']

    user_exits = User.query.filter_by(
        microsoft_id=user_info.get('oid')).first()
    if not user_exits:
        me = User(
            email_address=user_info.get('email'),
            username=user_info.get('name'),
            microsoft_id=user_info.get('oid')
        )
        db.session.add(me)
        db.session.commit()

        login_user(me)
    else:
        login_user(user_exits)

    return redirect(os.environ.get('CLIENT_URL'))


@auth.route('/user', methods=['GET'])
def get_user():
    # print(to_json(current_user))
    if(to_json(current_user) is None):
        return {'msg': 'no user'}   
    return to_json(current_user)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')
