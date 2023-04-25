from flask import request
from flask_socketio import SocketIO, emit
from firebase_admin import credentials, firestore, initialize_app
import json

cred = credentials.Certificate('config/key.json')
initialize_app(cred)

db = firestore.client()
socketio = SocketIO()

notification_ref = db.collection('notification')


@socketio.on('connect')
def socket_connect(data):
    print(f"someone connected to the socket {request.sid}")


@socketio.on('disconnet')
def socket_disconnet(data):
    print(f"someone disconneted from socket {request.sid}")


@socketio.on('new_post')
def handle_new_post(data):
    print(data)
    # data['media_content'] = b''.join([bytes([x]) for x in data['media_content']]).decode('utf-16', errors='replace')
    notification = json.loads(data)
    notification_ref.document().set(notification)
    emit('new_post', json.dumps(data), braodcast=True, include_self=True)
