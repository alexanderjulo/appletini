from flask import Blueprint, render_template, redirect, url_for, flash, request
from flaskext.login import login_required

from textile import textile

from www import db

page = Blueprint('page', __name__)

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(80))
	title = db.Column(db.String(80))
	body_plain = db.Column(db.Text)
	body_textile = db.Column(db.Text)

	def __init__(self, path, title, body):
		self.path = path
		self.title = title
		self.body_plain = body
		self.body_textile = textile(body)

	def __repr__(self):
		return '<Page: %r>' % self.path


@page.route('/admin/page/')
@login_required
def pageindex():
	return pageadmin()

@page.route('/admin/page/add/')
@login_required
def pageadd():
	return render_template('pages/edit.html')

@page.route('/admin/page/delete/<int:id>/')
@login_required
def pagedel(id):
	page = Page.query.filter_by(id=id).first_or_404()
	db.session.delete(page)
	db.session.commit()
	flash('Page deleted.')
	return redirect(url_for('page.pageindex'))

@page.route('/admin/page/post', methods=['POST'])
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
	return redirect(url_for('page.pageindex'))

@page.route('/admin/page/edit/<int:id>/')
@login_required
def pageadmin(id=None):
	if id is None:
		pages = Page.query.order_by('id').all()
		return render_template('pages/index.html', pages=pages)
	else:
		page = Page.query.filter_by(id=id).first_or_404()
		return render_template('pages/edit.html', page=page)

@page.route('/<path>/')
def pageshow(path):
	page = Page.query.filter_by(path=path).first_or_404()
	return render_template('pages/show.html', page=page)
