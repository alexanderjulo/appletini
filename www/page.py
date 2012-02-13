from flask import render_template

from textile import textile

from www import www, db

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(80))
	title = db.Column(db.String(80))
	body = db.Column(db.Text)

	def __init__(self, path="", title="", body=""):
		self.path = path
		self.title = title
		self.body = body

	def __repr__(self):
		return '<Page: %r>' % self.path

@www.route('/<path>/')
def pageshow(path):
	page = Page.query.filter_by(path=path).first_or_404()
	return render_template('pages/show.html', content=textile(page.body), title=page.title)
