from flask import request, redirect, render_template, flash, url_for
from flaskext.login import login_user, logout_user, login_required, current_user

from hashlib import md5

from www import www, db, login

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True)
	mail = db.Column(db.String, unique=True)
	password = db.Column(db.String(32))
	active = db.Column(db.Boolean)
	authenticated = db.Column(db.Boolean)
	
	author = db.relationship('Post', backref='author')

	def __init__(self, mail, password, name):
		self.name = name
		self.mail = mail
		self.password = md5(password).hexdigest()
		self.active = True
		self.authenticated = False

	def __repr__(self):
		return '<User: %s>' % self.name

	def authenticate(self, password):
		if self.password == md5(password).hexdigest():
			return True
		else:
			return False

	# the loginmanager specific stuff
	def is_authenticated(self):
		return self.authenticated

	def is_active(self):
		return self.active

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id	


@login.user_loader
def user_loader(id):
		return User.query.get(id)


@www.route('/login', methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		user = User.query.filter_by(mail=request.form['email']).first()
		if user is None:
			flash('Login failed.')
		elif user.authenticate(request.form['password']):
			user.authenticated = True
			db.session.commit()
			login_user(user)
			flash('Login succeeded.')
			return redirect(request.args.get("next") or url_for('home'))
		else:
			flash('Login failed.')
	return render_template('login.html')


@www.route('/logout/')
@login_required
def logout():
	current_user.authenticated = False
	db.session.commit()
	logout_user()
	flash('Logout succeeded.')
	return redirect(url_for('home'))
