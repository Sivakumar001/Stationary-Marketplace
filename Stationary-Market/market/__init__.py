from flask import Flask
from flask_sqlalchemy import SQLAlchemy #database
from flask_bcrypt import Bcrypt #encryption
from flask_login import LoginManager #login

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marketdata.db"
app.config["SECRET_KEY"] = "32c2f3c386577b45afdfcb22"

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category="info"
db = SQLAlchemy(app)

from market import routes
