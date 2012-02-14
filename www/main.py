from flask import redirect, url_for, render_template, request, flash
from flaskext.mail import Message

from www import www, mail

# projects page
@www.route('/projects/')
def projectindex():
	return render_template('comingsoon.html', what='Projects')

# stuff independent of the sections

# home page
@www.route('/')
def home():
	return redirect(url_for('postindex'))

# 404 page
@www.errorhandler(404)
def page_not_found(error):
	return render_template('pagenotfound.html'), 404
