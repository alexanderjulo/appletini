from flask import Flask
www = Flask(__name__)
www.config.from_pyfile('../config.cfg')

from flaskext.login import LoginManager, login_required
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
from www import blog
from www import contact

from flask.ext import admin
from flask.ext.admin.datastore.sqlalchemy import SQLAlchemyDatastore
admin_datastore = SQLAlchemyDatastore((user.User, page.Page, blog.Post), db.session, model_forms={'Post': blog.PostForm})
admin_blueprint = admin.create_admin_blueprint(admin_datastore)
www.register_blueprint(admin_blueprint, url_prefix='/admin', view_decorator=login_required)
