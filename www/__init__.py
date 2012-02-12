from flask import Flask
www = Flask(__name__)
www.config.from_pyfile('../config.cfg')

from flaskext.login import LoginManager
login = LoginManager()
login.setup_app(www, add_context_processor=True)
login.login_view = 'login'

from flaskext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(www)

from flaskext.mail import Mail
mail = Mail(www)

from www import user
from www import main
from www import page