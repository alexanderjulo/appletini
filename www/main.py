from flask import redirect, url_for, render_template, request, flash
from flaskext.login import login_required

from www import www, mail

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

# stuff independent of the sections

# home page
@www.route('/')
def home():
	return redirect(url_for('postindex'))

# 404 page
@www.errorhandler(404)
def page_not_found(error):
	return render_template('pagenotfound.html'), 404
