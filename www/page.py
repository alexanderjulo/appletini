from flask import Blueprint, render_template

from wtforms import Form
from wtforms.fields import TextField, TextAreaField

from sqlalchemy.ext.hybrid import hybrid_property
from textile import textile

from www import db

blueprint = Blueprint('page', __name__)

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(80))
	title = db.Column(db.String(80))
	body_markup = db.Column(db.Text)
	body_html = db.Column(db.Text)

	@hybrid_property
	def body(self):
		return self.body_markup

	@body.setter
	def body(self, body):
		self.body_markup = body
		self.body_html = textile(body)

	def __repr__(self):
		return '<Page: %r>' % self.path

class PageForm(Form):
	path = TextField()
	title = TextField()
	body = TextAreaField()

@blueprint.route('/<path:path>/')
def pageshow(path):
	page = Page.query.filter_by(path=path).first_or_404()
	return render_template('pages/show.html', page=page)

admin_models = [Page]
admin_forms = {'Page': PageForm}

