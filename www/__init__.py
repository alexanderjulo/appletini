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

from flaskext.bcrypt import Bcrypt
bcrypt = Bcrypt(www)

from www import tweaks
from www import main
from www import user
from www.menu import register
from werkzeug.utils import import_string
from flask.ext import admin
from flask.ext.admin.datastore.sqlalchemy import SQLAlchemyDatastore

'''
example config line:
WWW_BLUEPRINTS=[('www.blog',{'url_prefix': '/blog'}, ('blog', '/blog')),\
				('www.contact',{'url_prefix': '/contact'}, ('contact', '/contact')]
'''

admin_forms = {}
admin_models = []

for module, blueprint_options, menu_options in www.config['WWW_BLUEPRINTS']:
	m = import_string(module)
	www.register_blueprint(m.blueprint, **blueprint_options)
	admin_models.extend(m.admin_models)
	admin_forms.update(m.admin_forms)
	register(*menu_options)

admin_datastore = SQLAlchemyDatastore(tuple(admin_models), db.session, model_forms=admin_forms)
admin_blueprint = admin.create_admin_blueprint(admin_datastore)

def check_auth_for_admin():
	if not current_user.is_authenticated():
		return redirect(url_for('login', next=request.url))

admin_blueprint.before_request(check_auth_for_admin)
www.register_blueprint(admin_blueprint, url_prefix='/admin')
