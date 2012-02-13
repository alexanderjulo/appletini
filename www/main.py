from flask import redirect, url_for, render_template, request, flash
from flaskext.mail import Message

from www import www, mail

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
