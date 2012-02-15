from flask import Flask, redirect, request, url_for
www = Flask(__name__)
www.config.from_pyfile('../config.cfg')

from flaskext.login import LoginManager, current_user
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
from www.page import page, Page, PageForm
www.register_blueprint(page)
from www.blog import blog, Post, PostForm
www.register_blueprint(blog, url_prefix='/blog')
from www.contact import contact
www.register_blueprint(contact, url_prefix='/contact')

from flask.ext import admin
from flask.ext.admin.datastore.sqlalchemy import SQLAlchemyDatastore
admin_datastore = SQLAlchemyDatastore((Page, Post), db.session, model_forms={'Post': PostForm, 'Page': PageForm})
admin_blueprint = admin.create_admin_blueprint(admin_datastore)

def check_auth_for_admin():
	if not current_user.is_authenticated():
		return redirect(url_for('login', next=request.url))

admin_blueprint.before_request(check_auth_for_admin)
www.register_blueprint(admin_blueprint, url_prefix='/admin')
