from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO()


def create_app(debug=False):
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'secret!'
    app.debug = debug

    from .command import commands
    app.register_blueprint(commands, url_prefix='/api')

    from .view import view
    app.register_blueprint(view, url_prefix='/')
    
    socketio.init_app(app)
    return app
