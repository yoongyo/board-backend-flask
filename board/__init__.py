from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import production
from sqlalchemy import MetaData
from flask_cors import CORS
from flask_socketio import SocketIO


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
# socketio = SocketIO()


def create_app():
    app = Flask(__name__)


    CORS(app, resources={r"*": {"origins": "*"}})

    # app.config.from_envvar('APP_CONFIG_FILE')
    app.config.from_object(production)
    db.init_app(app)

    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


    from . import models
    from .views import main_views
    app.register_blueprint(main_views.bp)

    # app.config['SECRET_KEY'] = 'secret!'
    # app = socketio.init_app(app, cors_allowed_origins="*")

    return app



