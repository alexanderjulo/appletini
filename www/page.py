from flask import Blueprint, render_template

from textile import textile

from www import db

page = Blueprint('page', __name__)

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(80))
	title = db.Column(db.String(80))
	body_markup = db.Column(db.Text)
	body_html = db.Column(db.Text)

	def __init__(self, path="", title="", body=""):
		self.path = path
		self.title = title
		self.body_markup = body
		self.body_html = textile(body)

	def __repr__(self):
		return '<Page: %r>' % self.path

@page.route('/<path>/')
def pageshow(path):
	page = Page.query.filter_by(path=path).first_or_404()
	return render_template('pages/show.html', page=page)
