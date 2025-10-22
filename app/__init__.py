from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
socketio = SocketIO()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Конфигурация
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///chat.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация расширений
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    migrate.init_app(app, db)

    # Регистрация blueprint'ов
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Регистрация WebSocket событий
    from app.socket_events import register_socket_events
    register_socket_events(socketio)

    return app