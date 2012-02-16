from flask import Blueprint, render_template, request, url_for

from werkzeug.contrib.atom import AtomFeed

from wtforms import Form
from wtforms.fields import TextField, TextAreaField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.admin.wtforms import DateTimePickerWidget

from sqlalchemy import desc
from sqlalchemy.ext.hybrid import hybrid_property
from textile import textile
from datetime import datetime

from www import db
from user import User

blog = Blueprint('blog', __name__)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60))
	body_markup = db.Column(db.Text)
	body_html = db.Column(db.Text)
	created = db.Column(db.DateTime)

	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

	@hybrid_property
	def body(self):
		return self.body_markup

	@body.setter
	def body(self, body):
		self.body_markup = body
		self.body_html = textile(body)

	def __repr__(self):
		return '<Post: %r>' % self.title

def all_users():
	return User.query.all()

class PostForm(Form):
	title = TextField()
	created = DateTimeField(widget=DateTimePickerWidget())
	author = QuerySelectField(query_factory=all_users)
	body = TextAreaField()

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
		feed.add(post.title, post.body_html, content_type='html', author=post.author.name, url=url_for('blog.postshow', id=post.id), id=post.id, updated=post.created, published=post.created)
	return feed.get_response()
