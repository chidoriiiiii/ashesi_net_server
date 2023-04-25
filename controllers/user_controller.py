from flask import Blueprint, request, session
from models.user.user_model import User
from models.associations import follows
from utils.utils import to_json
from config.db import db, conn
import psycopg2
import json

_user = Blueprint('user', __name__)


@_user.route('/')
def retreive_all_users():
    users = db.session.query(User).all()
    for user in users:
        print(user)
    return to_json(users)


@_user.route("/<user_id>", methods=["GET"])
def retreive_user(user_id):
    print(session.get("_user_id"))
    user = User.query.filter_by(user_id=user_id).one()
    return to_json(user)


@_user.route("/<user_id>", methods=["PATCH"])
def update_user(user_id):
    user = json.loads(request.data)
    user_exists = User.query.get(user_id)
    if not user_exists:
        return {'msg': 'couldn"t update because user not found'}, 404

    user_exists.bio = user.get('bio') if user.get('bio') else user_exists.bio
    user_exists.major = user.get('major') if user.get('major') else user_exists.major
    user_exists.year_group = user.get('year_group') if user.get('year_group') else user_exists.year_group
    user_exists.favorite_food = user.get('favorite_food') if user.get('favorite_food') else user_exists.favorite_food
    user_exists.favorite_movie = user.get('favorite_movie') if user.get('favorite_movie') else user_exists.favorite_movie
    user_exists.residency = user.get('residency') if user.get('residency') else user_exists.residency


    db.session.add(user_exists)
    db.session.commit()

    return to_json(user_exists); 

@_user.route("/<user_id>/setup", methods=["PATCH"])
def setup_profile(user_id):
    user = json.loads(request.data)
    user_exists = User.query.get(user_id)
    if not user_exists:
        return {'msg': 'couldn"t update because user not found'}, 404

    user_exists.student_id = user.get('student_id') if user.get('student_id') else user_exists.student_id
    user_exists.date_of_birth = user.get('date_of_birth') if user.get('date_of_birth') else user_exists.date_of_birth
    user_exists.bio = user.get('bio') if user.get('bio') else user_exists.bio
    user_exists.major = user.get('major') if user.get('major') else user_exists.major
    user_exists.year_group = user.get('year_group') if user.get('year_group') else user_exists.year_group
    user_exists.favorite_food = user.get('favorite_food') if user.get('favorite_food') else user_exists.favorite_food
    user_exists.favorite_movie = user.get('favorite_movie') if user.get('favorite_movie') else user_exists.favorite_movie
    user_exists.residency = user.get('residency') if user.get('residency') else user_exists.residency


    db.session.add(user_exists)
    db.session.commit()
    return to_json(user_exists); 

@_user.route("/<user_id>/follow", methods=["POST"])
def create_follow(user_id):
    causer_id = session.get('_user_id')
    follow = follows.insert().values(causer_id=causer_id, receiver_id=user_id)

    db.session.execute(follow)
    db.session.commit()

    return {"msg": "follow successfully created"}, 200


@_user.route("/<user_id>/unfollow", methods=["DELETE"])
def delete_follow(user_id):
    causer_id = session.get("_user_id")
    delete = follows.delete().where(
        (follows.c.causer_id == causer_id) & (
            follows.c.receiver_id == user_id))

    db.session.execute(delete)
    db.session.commit()

    return {'msg': "successfully deleted like"}, 204

@_user.route("/bookmarks", methods=["GET"])
def retreive_bookmarks():
    user_id = session.get('_user_id')
    cur = conn.cursor()

    limit = 10
    cursor = int(request.args.get('cursor'))
    offset = cursor * limit
    next_cursor = cursor + 1

    query = f'''
        SELECT post.post_id, post.media_url, post.title, post.content, post.created_at, "user".avatar_url, "user".username, "user".user_id, 
                             (select count(*) from likes where post_id = post.post_id) as like_count,
                            (SELECT COUNT(*) FROM comment WHERE post_id = post.post_id) AS comment_count,
                            CASE WHEN l.creator_id IS NOT NULL THEN true ELSE false END AS liked, 
                            CASE WHEN s.saver_id IS NOT NULL THEN true ELSE false END AS saved
        FROM post
        JOIN saves ON saves.post_id = post.post_id
        JOIN "user" ON saves.saver_id= "user".user_id
        LEFT JOIN likes l ON post.post_id = l.post_id AND l.creator_id = '{user_id}'
        LEFT JOIN saves s ON post.post_id = s.post_id AND s.saver_id = '{user_id}'
        WHERE "user".user_id = '{user_id}'
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
    
    return {'data': posts , 'has_next': has_next,
            'next_cursor': next_cursor}

   
@_user.route("/created", methods=["GET"])
def retrieve_created():
    user_id = session.get('_user_id')
    cur = conn.cursor()

    limit = 10
    cursor = int(request.args.get('cursor'))
    offset = cursor * limit
    next_cursor = cursor + 1

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
        WHERE post.author_id = '{user_id}'
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
    
    return {'data': posts , 'has_next': has_next,
            'next_cursor': next_cursor}
    

@_user.route('/suggestions', methods=["GET"])
def retrieve_suggestions():
    user_id = session.get('_user_id')
    query = f'''
        SELECT "user".user_id, username, avatar_url, email_address 
        FROM "user"
        LEFT JOIN (
            SELECT receiver_id AS user_id
            FROM follows
            WHERE causer_id = '{user_id}'
            UNION
            SELECT causer_id AS user_id
            FROM follows
            WHERE receiver_id= '{user_id}' 
        ) AS following
        ON "user".user_id = following.user_id
        WHERE following.user_id IS NULL
        AND "user".user_id != '{user_id}' 
    '''
    
    cur = conn.cursor()

    try:
        cur.execute(query)  
        suggestions = []
        for row in cur.fetchall():
            sugg_dict= {
                'user_id': row[0],
                'username': row[1],
                'avatar_url': row[2],
                'email_address': row[3],
            }

            suggestions.append(sugg_dict)

        return suggestions; 

    except psycopg2.Error as e:
        print("Error: ", e)
        conn.rollback()
    finally:
        cur.close()
        

@_user.route('/search', methods=["GET"])
def search_users():
    user_id = session.get('_user_id')
    query = request.query_string.decode('utf-8')
    query = query.split("=")[1]
    print(query)

    query = f'''
        SELECT "user".user_id, username, avatar_url, email_address 
        FROM "user"
        WHERE "user".user_id != '{user_id}'
        AND "user".email_address Like '{query}%'
    '''
    
    cur = conn.cursor()

    try:
        cur.execute(query)  
        suggestions = []
        for row in cur.fetchall():
            sugg_dict= {
                'user_id': row[0],
                'username': row[1],
                'avatar_url': row[2],
                'email_address': row[3],
            }

            suggestions.append(sugg_dict)

        return suggestions; 

    except psycopg2.Error as e:
        print("Error: ", e)
        conn.rollback()
    finally:
        cur.close()