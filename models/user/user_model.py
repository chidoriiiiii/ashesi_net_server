from config.db import db
from flask_login import UserMixin
from sqlalchemy import text as sa_text
from sqlalchemy.dialects.postgresql import UUID
from models.associations import saves, likes, follows
from datetime import datetime


class User(db.Model, UserMixin):

    user_id = db.Column(UUID(as_uuid=True), primary_key=True,
                        server_default=sa_text("uuid_generate_v4()"))
    email_address = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(128))
    microsoft_id = db.Column(db.String)
    bio = db.Column(db.String(140))
    avatar_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # new fields
    student_id = db.Column(db.String)
    favorite_food= db.Column(db.String)
    favorite_movie= db.Column(db.String)
    year_group = db.Column(db.String)
    major = db.Column(db.String)
    residency = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    
    # relationships
    posts = db.relationship('Post', backref='author', lazy=False)
    comments = db.relationship('Comment', backref='author')
    saves = db.relationship('Post', secondary=saves, lazy='dynamic',
                            backref=db.backref('saved', lazy='dynamic'))

    likes = db.relationship('Post',
                            secondary=likes,
                            lazy='dynamic',
                            backref=db.backref('liked', lazy='dynamic')
                            )

    follows = db.relationship('User', secondary=follows, lazy='dynamic',
                              primaryjoin=follows.c.receiver_id == user_id,
                              secondaryjoin=follows.c.causer_id == user_id,
                              backref=db.backref('followed', lazy='dynamic'))

    # login methods
    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f'<User user_id={self.user_id} email_address={self.email_address} username={self.username} posts={self.posts} comments={self.comments}>'
