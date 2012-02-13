from flask import redirect, url_for, render_template, request, flash
from flaskext.login import login_user, logout_user, login_required, current_user
from flaskext.mail import Message

from datetime import datetime

from www import www, db, login, mail
from user import User

@www.route('/admin/user/')
@login_required
def userlist():
	pass

@www.route('/admin/user/add/')
@login_required
def useradd():
	return useredit()

@www.route('/admin/user/edit/<int:id>/')
@login_required
def useredit(id=None):
	pass
	
@www.route('/admin/user/delete/<int:id>/')
@login_required
def userdel(id):
	pass
	
@www.route('/admin/user/post', methods=['POST'])
@login_required
def userpost():
	pass


# projects page
@www.route('/projects/')
def projectindex():
	return render_template('comingsoon.html', what='Projects')



# contact app
@www.route('/contact', methods=['GET', 'POST'])
def contact():
	if request.method == 'POST':
		if request.form['name'] == '':
			flash('Please enter a valid name.')
		if request.form['email'] == '':
			flash('Please enter a valid e-mail-address.')
		elif request.form['text'] == '':
			flash('Please enter a valid message.')
		else:
			msg = Message('Contact form input',
				sender = (request.form['name'], request.form['email']),
				recipients = ['alexander.jung-loddenkemper@julo.ch'],
				body = request.form['text'],
			)
			mail.send(msg)
			flash('Message sent.')
			return redirect(url_for('home'))
	return render_template('contact.html')


# stuff independent of the sections

# home page
@www.route('/')
def home():
	return redirect(url_for('postindex'))

# 404 page
@www.errorhandler(404)
def page_not_found(error):
	return render_template('pagenotfound.html'), 404
