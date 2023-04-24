from config.db import db
from sqlalchemy import text as sa_text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class Post(db.Model):
    post_id = db.Column(UUID(as_uuid=True), primary_key=True,
                        server_default=sa_text("uuid_generate_v4()"))
    media_url = db.Column(db.String)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'))
   
    
    # relationships

    comments = db.relationship('Comment', backref='post', lazy=True)


class Comment(db.Model):
    comment_id = db.Column(UUID(as_uuid=True), primary_key=True,
                           server_default=sa_text("uuid_generate_v4()"))
    parent_id = db.Column(UUID(as_uuid=True),
                          db.ForeignKey('comment.comment_id'))
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('post.post_id'))
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# class Saved(db.Model):
#     saver_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'))
#     post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('post.post_id'))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)


# class Liked(db.Model):
#     creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'))
#     post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('post.post_id'))
#     comment_id = db.Column(
#         UUID(as_uuid=True), db.ForeignKey('comment.comment_id'))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
