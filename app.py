#!/usr/bin/env python
import json
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, rooms

import eventlet
eventlet.monkey_patch()

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

command_namespace = '/commands'


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route("/send/<room>", methods=["POST"])
def commands(room):
    post_data = json.loads(request.data)
    emit('command',
         post_data,
         room=room,
         namespace=command_namespace)
    return json.dumps({'success': True})


@socketio.on('my_room_event', namespace=command_namespace)
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('command',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('connect', namespace=command_namespace)
def connect():
    emit('command', {'data': 'Connected', 'count': 0})


@socketio.on('join', namespace=command_namespace)
def join(message):
    join_room(message['room'])
    emit('command',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': 'test'})
