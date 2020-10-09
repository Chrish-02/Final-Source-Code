from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

db = SQLAlchemy(app)

from application import routes