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

from www import tweaks
from www import main
from www import user
from www import page
from www.blog import blog
www.register_blueprint(blog, url_prefix='/blog')
from www.contact import contact
www.register_blueprint(contact, url_prefix='/contact')
