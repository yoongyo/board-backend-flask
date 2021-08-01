from board import create_app, socketio
from flask_socketio import SocketIO

app = create_app()

socketio.run(app)
