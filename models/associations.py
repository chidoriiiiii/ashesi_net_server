from config.db import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

saves = db.Table('saves',
                 db.Column('saver_id', UUID(as_uuid=True), db.ForeignKey(
                     'user.user_id'), primary_key=True),
                 db.Column('post_id', UUID(as_uuid=True), db.ForeignKey(
                     'post.post_id'), primary_key=True),
                 db.Column('created_at', db.DateTime,
                           default=datetime.utcnow())
                 )

likes = db.Table('likes',
                 db.Column('creator_id', UUID(as_uuid=True),
                           db.ForeignKey('user.user_id')),
                 db.Column('comment_id', UUID(as_uuid=True),
                           db.ForeignKey('comment.comment_id')),
                 db.Column('post_id', UUID(as_uuid=True), db.ForeignKey(
                     'post.post_id')),
                 db.Column('created_at', db.DateTime,
                           default=datetime.utcnow())
                 )

follows = db.Table('follows',
                   db.Column('causer_id', UUID(
                       as_uuid=True),
                       db.ForeignKey('user.user_id'),
                       primary_key=True),
                   db.Column('receiver_id', UUID(
                       as_uuid=True), db.ForeignKey('user.user_id'), primary_key=True),
                   db.Column('created_at', db.DateTime,
                             default=datetime.utcnow())
                   )
