from flask import render_template, redirect, url_for, flash
from flaskext.login import login_required

from textile import textile

from www import www, db

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


@www.route('/admin/page/')
@login_required
def pageindex():
	return pageadmin()

@www.route('/admin/page/add/')
@login_required
def pageadd():
	return render_template('pages/edit.html')

@www.route('/admin/page/delete/<int:id>/')
@login_required
def pagedel(id):
	page = Page.query.filter_by(id=id).first_or_404()
	db.session.delete(page)
	db.session.commit()
	flash('Page deleted.')
	return redirect(url_for('pageindex'))

@www.route('/admin/page/post/', methods=['POST'])
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

@www.route('/admin/page/edit/<int:id>/')
@login_required
def pageadmin(id=None):
	if id is None:
		pages = Page.query.order_by('id').all()
		return render_template('pages/index.html', pages=pages)
	else:
		page = Page.query.filter_by(id=id).first_or_404()
		return render_template('pages/edit.html', title=page.title, path=page.path, body=page.body, id=page.id)

@www.route('/<path>/')
def pageshow(path):
	page = Page.query.filter_by(path=path).first_or_404()
	return render_template('pages/show.html', content=textile(page.body), title=page.title)
