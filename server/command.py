#!/usr/bin/env python
import json, os
from server import socketio
from threading import Lock
from flask import Blueprint, session, request
from flask_socketio import emit, join_room, rooms

import eventlet
eventlet.monkey_patch()

commands = Blueprint('commands', __name__)

thread = None
thread_lock = Lock()

command_namespace = '/commands'


@commands.route("/")
def test():
    return 'api test'


@commands.route("/send/<room>", methods=["POST"])
def command(room):
    post_data = json.loads(request.data)
    emit('command',
         post_data,
         room=room,
         namespace=command_namespace)
    return json.dumps({'success': True})


# For testing
@socketio.on('my_room_event', namespace=command_namespace)
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('command',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('connect', namespace=command_namespace)
def connect():
    emit('command', {'data': 'Connected'})


@socketio.on('join', namespace=command_namespace)
def join(message):
    join_room(message['room'])
    emit('command',
         {'room': rooms})