from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager


app = Flask(__name__)


app.config.update(
    ADMIN = os.environ.get('ADMIN')
)

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@host/db'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Migrate(app,db)

#LOGINMANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


#BLUEPRINTS
from src.users.views import users
app.register_blueprint(users)
from src.core.views import core
app.register_blueprint(core)

