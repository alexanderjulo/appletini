from www import www, db

class Menu(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	link = db.Column(db.String(), unique=True)
	
	def __init__(self, name, link):
		self.name = name
		self.link = link

def insert_entry(name, link):
	entry = Menu.query.filter_by(link=link).first()
	if entry is None:
		entry = Menu(name=name, link=link)
		db.session.add(entry)
		db.session.commit()
		return True
	else:
		return False

def remove_entry(link):
	entry = Menu.query.filter_by(link=link).first()
	if entry is None:
		return False
	else:
		db.session.delete(entry)
		db.session.commit()
		return True

@www.context_processor
def inject_menu():
	menu = Menu.query.all()
	return dict(menu=menu)
