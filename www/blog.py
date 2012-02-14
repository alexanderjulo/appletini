from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskext.login import login_required, current_user

from werkzeug.contrib.atom import AtomFeed

from sqlalchemy import desc
from textile import textile
from datetime import datetime

from www import www, db

blog = Blueprint('blog', __name__)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60))
	body_plain = db.Column(db.Text)
	body_textile = db.Column(db.Text)
	created = db.Column(db.DateTime)

	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, title, body, author):
		self.title = title
		self.body_plain = body
		self.body_textile = textile(body)
		self.created = datetime.utcnow()
		self.author_id = author

	def __repr__(self):
		return '<Post: %r>' % self.title

@blog.route('/')
def postindex():
	return postpage(1)

@blog.route('/<int:page>/')
def postpage(page):
	posts = Post.query.order_by(desc('created')).paginate(page, per_page=6)
	return render_template('blog/index.html', posts=posts)

@blog.route('/post/<int:id>/')
def postshow(id):
	post = Post.query.get_or_404(id)
	return render_template('blog/show.html', post=post)

# atom feed for my blog
@blog.route('/atom/')
def postatom():
	feed = AtomFeed(www.config['WWW_TITLE'], feed_url=request.url, url=request.host_url, subtitle=www.config['WWW_SLOGAN'])
	for post in Post.query.order_by(desc('created')).limit(10).all():
		feed.add(post.title, post.body_textile, content_type='html', author=post.author.name, url=url_for('blog.postshow', id=post.id), id=post.id, updated=post.created, published=post.created)
	return feed.get_response()

@blog.route('/post/add/')
@login_required
def postadd():
	return postedit()

@blog.route('/post/<int:id>/edit/')
@login_required
def postedit(id=None):
	if id is None:
		return render_template('blog/edit.html')
	else:
		post = Post.query.filter_by(id=id).first_or_404()
		return render_template('blog/edit.html', body=post.body_plain, title=post.title, id=post.id)

@blog.route('/post/post', methods=['POST'])
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
	return redirect(url_for('blog.postindex'))

@blog.route('/admin/post/<int:id>/delete/')
@login_required
def postdel(id):
	post = Post.query.filter_by(id=id).first_or_404()
	db.session.delete(post)
	db.session.commit()
	flash('Post deleted.')
	return redirect(url_for('blog.postindex'))
