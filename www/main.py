from flask import redirect, url_for, render_template, request, flash
from sqlalchemy import desc
from flaskext.login import login_user, logout_user, login_required, current_user
from flaskext.mail import Message

from werkzeug.contrib.atom import AtomFeed

from textile import textile
from datetime import datetime

from www import www, db, login, mail
from user import User

@www.route('/admin/user')
@login_required
def userlist():
	pass

@www.route('/admin/user/add')
@login_required
def useradd():
	return useredit()

@www.route('/admin/user/edit/<int:id>')
@login_required
def useredit(id=None):
	pass
	
@www.route('/admin/user/delete/<int:id>')
@login_required
def userdel(id):
	pass
	
@www.route('/admin/user/post', methods=['POST'])
@login_required
def userpost():
	pass


# projects page
@www.route('/projects')
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
	body = db.Column(db.Text)
	created = db.Column(db.DateTime)
	
	author = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __init__(self, title, body, author):
		self.title = title
		self.body = body
		self.created = datetime.utcnow()
		self.author = author

	def __repr__(self):
		return '<Post: %r>' % self.title
		
@www.route('/blog')
def postindex():
	posts = Post.query.order_by(desc('created')).all()
	for post in posts:
		author = User.query.get(post.author)
		post.author_name = author.firstname + ' ' + author.lastname
		post.body = textile(post.body)
	return render_template('blog/index.html', posts=posts)
	
@www.route('/blog/post/<int:id>')
def postshow(id):
	post = Post.query.get_or_404(id)
	author = User.query.get(post.author)
	post.author_name = author.firstname + ' ' + author.lastname
	post.body = textile(post.body)
	return render_template('blog/show.html', post=post)
	
# atom feed for my blog
@www.route('/blog/atom')
def postatom():
	feed = AtomFeed('julo.ch', feed_url=request.url, url=request.host_url, subtitle='It\'s mine.')
	for post in Post.query.order_by(desc('created')).limit(10).all():
		author = User.query.get(post.author)
		post.author_name = author.firstname + ' ' + author.lastname
		feed.add(post.title, textile(post.body), content_type='html', author=post.author_name, url=url_for('postshow', id=post.id), id=post.id, updated=post.created, published=post.created)
	return feed.get_response()
	
@www.route('/admin/post/add')
@login_required
def postadd():
	return postedit()
	
@www.route('/admin/post/edit/<int:id>')
@login_required
def postedit(id=None):
	if id is None:
		return render_template('blog/edit.html')
	else:
		post = Post.query.filter_by(id=id).first_or_404()
		return render_template('blog/edit.html', body=post.body, title=post.title, id=post.id)

@www.route('/admin/post/post', methods=['POST'])
@login_required
def postpost():
	if request.form['id'] == '':
		post = Post(title=request.form['title'], body=request.form['body'], author=current_user.get_id())
		db.session.add(post)
	else:
		post = Post.query.filter_by(id=request.form['id']).first_or_404()
		post.title = request.form['title']
		post.body = request.form['body']
	db.session.commit()
	flash('Post saved.')
	return redirect(url_for('postindex'))

@www.route('/admin/post/delete/<int:id>')
@login_required
def postdel(id):
	post = Post.query.filter_by(id=id).first_or_404()
	db.session.delete(post)
	db.session.commit()
	flash('Post deleted.')
	return redirect(url_for('postindex'))



# own textile flatpages stuff
class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(80))
	title = db.Column(db.String(80))
	body = db.Column(db.Text)
	
	def __init__(self, path, title, body):
		self.path = path
		self.title = title
		self.body = body
		
	def __repr__(self):
		return '<Page: %r>' % self.path

@www.route('/admin/page')
@login_required
def pageindex():
	return pageadmin()
	
@www.route('/admin/page/add')
@login_required
def pageadd():
	return render_template('pages/edit.html')
	
@www.route('/admin/page/delete/<int:id>')
@login_required
def pagedel(id):
	page = Page.query.filter_by(id=id).first_or_404()
	db.session.delete(page)
	db.session.commit()
	flash('Page deleted.')
	return redirect(url_for('pageindex'))

@www.route('/admin/page/post', methods=['POST'])
@login_required
def pagepost():
	if request.form['id'] == '':
		page = Page(path=request.form['path'], title=request.form['title'], body=request.form['body'])
		db.session.add(page)
	else:
		page = Page.query.filter_by(id=request.form['id']).first_or_404()
		page.path = request.form['path']
		page.title = request.form['title']
		page.body = request.form['body']
	db.session.commit()
	flash('Page saved.')
	return redirect(url_for('pageindex'))

@www.route('/admin/page/edit/<int:id>')
@login_required
def pageadmin(id=None):
	if id is None:
		pages = Page.query.order_by('id').all()
		return render_template('pages/index.html', pages=pages)
	else:
		page = Page.query.filter_by(id=id).first_or_404()
		return render_template('pages/edit.html', title=page.title, path=page.path, body=page.body, id=page.id)

@www.route('/<path>')
def pageshow(path):
	page = Page.query.filter_by(path=path).first_or_404()
	return render_template('pages/show.html', content=textile(page.body), title=page.title)


# stuff independent of the sections

# home page
@www.route('/')
def home():
	return redirect(url_for('postindex'))

# create non existent tables
db.create_all()

# 404 page
@www.errorhandler(404)
def page_not_found(error):
	return render_template('pagenotfound.html'), 404
	
# run the developement server
if __name__ == '__main__':
    www.run(host='0.0.0.0')
