from app.configs import database, migrations
from app import routes
from environs import Env
from flask import Flask

env = Env()
env.read_env()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
    app.config["SQLACHEMY_TRACK_MODIFICATIONS"] = False

    database.init_app(app)
    migrations.init_app(app)
    routes.init_app(app)

    return app
