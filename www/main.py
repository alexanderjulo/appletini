from flask import redirect, url_for, render_template, request, flash
from sqlalchemy import desc
from flaskext.login import login_user, logout_user, login_required, current_user
from flaskext.mail import Message

from werkzeug.contrib.atom import AtomFeed

from textile import textile
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

# own blog stuff

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60))
	body_plain = db.Column(db.Text)
	body_textile = db.Column(db.Text)
	created = db.Column(db.DateTime)
	
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __init__(self, title, body, author):
		self.title = title
		self.body_plain = body
		self.body_textile = textile(body)
		self.created = datetime.utcnow()
		self.author_id = author

	def __repr__(self):
		return '<Post: %r>' % self.title
		
@www.route('/blog/')
def postindex():
	return postpage(1)
	
@www.route('/blog/<int:page>/')
def postpage(page):
	posts = Post.query.join('author').order_by(desc('created')).paginate(page, per_page=6)
	return render_template('blog/index.html', posts=posts)
	
@www.route('/blog/post/<int:id>/')
def postshow(id):
	post = Post.query.join('author').filter_by(id=id).first_or_404()
	return render_template('blog/show.html', post=post)
	
# atom feed for my blog
@www.route('/blog/atom/')
def postatom():
	feed = AtomFeed('julo.ch', feed_url=request.url, url=request.host_url, subtitle='It\'s mine.')
	for post in Post.query.order_by(desc('created')).limit(10).all():
		author = User.query.get(post.author)
		post.author_name = author.name
		feed.add(post.title, post.body_textile, content_type='html', author=post.author_name, url=url_for('postshow', id=post.id), id=post.id, updated=post.created, published=post.created)
	return feed.get_response()
	
@www.route('/admin/post/add/')
@login_required
def postadd():
	return postedit()
	
@www.route('/admin/post/edit/<int:id>/')
@login_required
def postedit(id=None):
	if id is None:
		return render_template('blog/edit.html')
	else:
		post = Post.query.filter_by(id=id).first_or_404()
		return render_template('blog/edit.html', body=post.body_plain, title=post.title, id=post.id)

@www.route('/admin/post/post', methods=['POST'])
@login_required
def postpost():
	if request.form['id'] == '':
		post = Post(title=request.form['title'], body=request.form['body'], author=current_user.get_id())
		db.session.add(post)
	else:
		post = Post.query.filter_by(id=request.form['id']).first_or_404()
		post.title = request.form['title']
		post.body_plain = request.form['body']
		post.body_textile = textile(request.form['body'])
	db.session.commit()
	flash('Post saved.')
	return redirect(url_for('postindex'))

@www.route('/admin/post/delete/<int:id>/')
@login_required
def postdel(id):
	post = Post.query.filter_by(id=id).first_or_404()
	db.session.delete(post)
	db.session.commit()
	flash('Post deleted.')
	return redirect(url_for('postindex'))


# stuff independent of the sections

# home page
@www.route('/')
def home():
	return redirect(url_for('postindex'))

# 404 page
@www.errorhandler(404)
def page_not_found(error):
	return render_template('pagenotfound.html'), 404
