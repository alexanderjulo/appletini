from flask import Blueprint, request, flash, redirect, url_for, render_template
from flaskext.mail import Message

from www import www, mail

blueprint = Blueprint('contact', __name__)
admin_models = []
admin_forms = {}

@blueprint.route('/', methods=['GET', 'POST'])
def main():
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
				recipients = [www.config['WWW_CONTACT_MAIL']],
				body = request.form['text'],
			)
			mail.send(msg)
			flash('Message sent.')
			return redirect(url_for('home'))
	return render_template('contact.html')

