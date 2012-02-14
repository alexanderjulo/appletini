from flask import redirect, url_for, render_template

from www import www

# stuff independent of the sections

# home page
@www.route('/')
def home():
	return redirect(url_for('blog.postindex'))

# 404 page
@www.errorhandler(404)
def page_not_found(error):
	return render_template('pagenotfound.html'), 404
