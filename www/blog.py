from flask import render_template, request, redirect, url_for, flash
from flaskext.login import login_required

from werkzeug.contrib.atom import AtomFeed

from sqlalchemy import desc
from textile import textile

from www import www, db

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

@www.route('/blog/')
def postindex():
	return postpage(1)

@www.route('/blog/<int:page>/')
def postpage(page):
	posts = Post.query.order_by(desc('created')).paginate(page, per_page=6)
	return render_template('blog/index.html', posts=posts)

@www.route('/blog/post/<int:id>/')
def postshow(id):
	post = Post.query.get_or_404(id)
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