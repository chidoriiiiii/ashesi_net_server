from flask import Blueprint, request, session
from sqlalchemy import and_, desc
import psycopg2
from sqlalchemy.orm import selectinload, joinedload
from config.db import db, conn
from models.post.post_model import Post, Comment
from models.associations import likes, follows, saves
from utils.utils import to_json, upload_image
from faker import Faker
from models.user.user_model import User
from datetime import datetime
from sqlalchemy.sql import func
from io import BytesIO
import json


post = Blueprint('post', __name__)



@post.route("/", methods=["POST"])
def create_post():
    req = json.loads(request.data)
    print(req) 
    return {
        'msg': "hello"
    }
    
    # content = req.get('content')
    # media_content = req.get('media_content')
    # author_id = session.get('_user_id') 

    # if(media_content):
    #     blob = upload_image(media_content)
    #     post = Post(
    #         # title=title,
    #         content=content,
    #         author_id=author_id,
    #         media_url=blob.media_link)
    # else:
    #     post = Post(
    #         # title=title,
    #         content=content,
    #         author_id=author_id,
    #     )

    # db.session.add(post)
    # db.session.commit()
    
    
    # #Query Created Post 
    
    # cur = conn.cursor()
    # query = f'''
    #             SELECT post.post_id, post.media_url, post.title, post.content, post.created_at, "user".avatar_url, "user".username, "user".user_id, 
    #                 (select count(*) from likes where post_id = post.post_id) as like_count,
    #                 (SELECT COUNT(*) FROM comment WHERE post_id = post.post_id) AS comment_count,
    #                 CASE WHEN l.creator_id IS NOT NULL THEN true ELSE false END AS liked, 
    #                 CASE WHEN s.saver_id IS NOT NULL THEN true ELSE false END AS saved
    #             FROM post 
    #             JOIN "user" ON post.author_id = "user".user_id 
    #             LEFT JOIN likes l ON post.post_id = l.post_id AND l.creator_id = '{author_id}'
    #             LEFT JOIN saves s ON post.post_id = s.post_id AND s.saver_id = '{author_id}'
    #             WHERE post.post_id = '{post.post_id}'
    #             ORDER BY post.created_at DESC;
    # '''
    # cur.execute(query)
    # row = cur.fetchone()
    # print(row)
    # post = {
    #     'post_id': row[0],
    #     'media_url': row[1],
    #     'title': row[2],
    #     'content': row[3],
    #     'created_at': row[4],
    #     'author': {
    #         'avatar_url': row[5],
    #         'username': row[6],
    #         'user_id': row[7]
    #     },
    #     'likes_count': row[8],
    #     'comments_count': row[9],
    #     'has_liked': row[10],
    #     'has_saved': row[11]
    # }
    
    # cur.close()

    return post


@post.route("/<post_id>", methods=["GET"])
def retreive_post(post_id):
    user_id = session.get('_user_id')
    try:
        cur = conn.cursor()
        query = f'''
                    SELECT post.post_id, post.media_url, post.title, post.content, post.created_at, "user".avatar_url, "user".username, "user".user_id, 
                        (select count(*) from likes where post_id = post.post_id) as like_count,
                        (SELECT COUNT(*) FROM comment WHERE post_id = post.post_id) AS comment_count,
                        CASE WHEN l.creator_id IS NOT NULL THEN true ELSE false END AS liked, 
                        CASE WHEN s.saver_id IS NOT NULL THEN true ELSE false END AS saved
                    FROM post 
                    JOIN "user" ON post.author_id = "user".user_id 
                    LEFT JOIN likes l ON post.post_id = l.post_id AND l.creator_id = '{user_id}'
                    LEFT JOIN saves s ON post.post_id = s.post_id AND s.saver_id = '{user_id}'
                    WHERE post.post_id = '{post_id}'
                    ORDER BY post.created_at DESC;
        '''
        cur.execute(query)
        row = cur.fetchone()
        post = {
            'post_id': row[0],
            'media_url': row[1],
            'title': row[2],
            'content': row[3],
            'created_at': row[4],
            'author': {
                'avatar_url': row[5],
                'username': row[6],
                'user_id': row[7]
            },
            'likes_count': row[8],
            'comments_count': row[9],
            'has_liked': row[10],
            'has_saved': row[11]
        }

        return post
    except psycopg2.Error as e:
        print("Error: ", e)
        conn.rollback()
    finally:
        cur.close()
    # post_alchemy = Post.query.filter_by(post_id=post_id).one()
    # post_comment_count = len(post.comments) 


@post.route("/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    Post.query.filter_by(post_id=post_id).delete()
    return {'msg': "successfully deleted post"}, 204


@post.route("/<post_id>/like", methods=["POST"])
def create_like(post_id):
    creator_id = session.get("_user_id")
    like = likes.insert().values(creator_id=creator_id, post_id=post_id)

    db.session.execute(like)
    db.session.commit()

    return {"msg": "like successfully created"}, 200


@post.route("/<post_id>/unlike", methods=["DELETE"])
def delete_like(post_id):
    creator_id = session.get("_user_id")
    delete = likes.delete().where(
        (likes.c.post_id == post_id) & (
            likes.c.creator_id == creator_id))

    db.session.execute(delete)
    db.session.commit()

    return {'msg': "successfully deleted like"}, 204


@post.route("/<post_id>/save", methods=["POST"])
def create_save(post_id):
    saver_id = session.get("_user_id")
    save = saves.insert().values(saver_id=saver_id, post_id=post_id)

    db.session.execute(save)
    db.session.commit()

    return {"msg": "save successfully created"}, 200


@post.route("/<post_id>/unsave", methods=["DELETE"])
def delete_save(post_id):
    saver_id = session.get("_user_id")
    # cur = conn.cursor
    # query = f'''
    #     DELETE FROM saves where saver_id = CAST({saver_id} as UUID) and post_id = CAST({post_id} as UUID);
    # '''
    # cur.execute(query)
    # cur.close()
    save = saves.delete().where(
        (saves.c.saver_id == saver_id) &
        (saves.c.post_id == post_id)
    )

    db.session.execute(save)
    db.session.commit()

    return {"msg": f"successfully deleted save"}, 200


@post.route("/<post_id>/comment", methods=["POST"])
def create_comment(post_id):
    req = json.loads(request.data)

    author_id = session.get("_user_id")
    parent_id = req.get('parent_id')
    content = req.get('content')

    comment = Comment(
        author_id=author_id,
        parent_id=parent_id,
        content=content,
        post_id=post_id)
    db.session.add(comment)
    db.session.commit()

    return to_json(comment)


@post.route("/<post_id>/comment/all", methods=["GET"])
def retrieve_comments(post_id):
    limit = 10
    cursor = int(request.args.get('cursor'))
    offset = cursor * limit

    next_cursor = cursor + 1

    cur = conn.cursor()
    query = f'''

  SELECT c.comment_id, c.content, c.created_at, u.avatar_url, u.username, u.user_id, COALESCE(r.reply_count, 0) AS reply_count, c.post_id
FROM comment c
JOIN "user" u ON c.author_id = u.user_id
LEFT JOIN (
  SELECT parent_id, COUNT(*) AS reply_count
  FROM comment
  WHERE parent_id IS NOT NULL
  GROUP BY parent_id
) r ON c.comment_id = r.parent_id
WHERE c.post_id = '{post_id}' AND c.parent_id IS NULL
ORDER BY c.created_at DESC
OFFSET {offset} LIMIT {limit}; 
    '''
    cur.execute(query)
    comments = []
    for row in cur.fetchall():
        comment_dict = {
            'comment_id': row[0],
            'content': row[1],
            'created_at': row[2],
            'author': {
                'avatar_url': row[3],
                'username': row[4],
                'user_id': row[5]
            },
            'reply_count': row[6],
            'post_id': row[7]
        }
        comments.append(comment_dict)

    # comments = Comment.query.filter_by(
    #     post_id=post_id).offset(offset).limit(limit).all()
    has_next = False if len(comments) < limit else True
    # print(comments)

    cur.close()
    
    return {'data':comments, 'has_next': has_next,
            'next_cursor': next_cursor}


@post.route("/<post_id>/<comment_id>/reply/all", methods=["GET"])
def retrieve_replies(post_id, comment_id):
    # limit = 10
    # cursor = int(request.args.get('cursor'))
    # offset = cursor * limit

    # next_cursor = cursor + 1

    cur = conn.cursor()
    query = f'''

    SELECT 
    comment.comment_id, 
    comment.content, 
    comment.created_at, 
    "user".avatar_url, 
    "user".username, 
    "user".user_id,
    comment.post_id
    FROM comment 
    JOIN "user" ON comment.author_id = "user".user_id
    WHERE comment.post_id = '{post_id}'and comment.parent_id = '{comment_id}'
    ORDER BY comment.created_at DESC
    Limit {10};
    '''
    cur.execute(query)
    comments = []
    for row in cur.fetchall():
        comment_dict = {
            'comment_id': row[0],
            'content': row[1],
            'created_at': row[2],
            'author': {
                'avatar_url': row[3],
                'username': row[4],
                'user_id': row[5],
            },
            
            'reply_count': 0,
            'post_id': row[6]
        }
        comments.append(comment_dict)

    # comments = Comment.query.filter_by(
    #     post_id=post_id).offset(offset).limit(limit).all()
    # print(comments)

    cur.close()
    
    return {'data':comments}

@post.route("/feed", methods=["GET"])
def retrieve_feed():
    limit = 10
    user_id = session.get("_user_id")
    cursor = int(request.args.get('cursor'))
    sorting_factor = request.args.get('sort')
    offset = cursor * limit

    next_cursor = cursor + 1

    cur = conn.cursor()
    try:
        if (sorting_factor == "recent"):
            query = f'''
                    SELECT post.post_id, post.media_url, post.title, post.content, post.created_at, "user".avatar_url, "user".username, "user".user_id, 
                        (select count(*) from likes where post_id = post.post_id) as like_count,
                        (SELECT COUNT(*) FROM comment WHERE post_id = post.post_id) AS comment_count,
                        CASE WHEN l.creator_id IS NOT NULL THEN true ELSE false END AS liked, 
                        CASE WHEN s.saver_id IS NOT NULL THEN true ELSE false END AS saved
                    FROM post 
                    JOIN "user" ON post.author_id = "user".user_id 
                    LEFT JOIN likes l ON post.post_id = l.post_id AND l.creator_id = '{user_id}'
                    LEFT JOIN saves s ON post.post_id = s.post_id AND s.saver_id = '{user_id}'
                    ORDER BY post.created_at DESC
                    OFFSET {offset} Limit {limit};
            '''
            cur.execute(query)
            posts = []
            for row in cur.fetchall():
                post_dict = {
                    'post_id': row[0],
                    'media_url': row[1],
                    'title': row[2],
                    'content': row[3],
                    'created_at': row[4],
                    'author': {
                        'avatar_url': row[5],
                        'username': row[6],
                        'user_id': row[7]
                    },
                    'likes_count': row[8],
                    'comments_count': row[9], 
                    'has_liked': row[10],
                    'has_saved': row[11]
                }

                posts.append(post_dict)

            has_next = False if len(posts) < limit else True
        

        elif (sorting_factor == "Top"):
            pass

        
        return {'data': posts , 'has_next': has_next,
                'next_cursor': next_cursor}

    except psycopg2.Error as e:
        print("Error: ", e)
        conn.rollback()
        return {'data': []}
    finally:
        cur.close()
        # conn.close() 

@post.route("/addFake", methods=["GET"])
def add_fake():

    fake = Faker()

    # Create 10 dummy posts
    for i in range(20):
        post = Post(
            media_url=fake.image_url(),
            title=fake.sentence(),
            content=fake.paragraph(),
            created_at=datetime.utcnow(),
            author_id=User.query.order_by(func.random()).first().user_id
        )
        db.session.add(post)

    db.session.commit()
