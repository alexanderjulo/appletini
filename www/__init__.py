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
from werkzeug.utils import import_string

'''
example config line:
WWW_BLUEPRINTS=[('www.blog.blog',{'url_prefix': '/blog'}),\
				('www.contact.contact',{'url_prefix': '/contact'})]
'''

for blueprint, options in www.config['WWW_BLUEPRINTS']:
    blueprint_obj = import_string(blueprint)
    www.register_blueprint(blueprint_obj, **options)
