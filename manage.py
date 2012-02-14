from www import www, db
from www.user import User

from flaskext.script import Manager
manager = Manager(www)

@manager.command
def initdb():
	db.create_all()
	u = User("mail@danjou.de", "1234", "dAnjou")
	db.session.add(u)
	db.session.commit()
	
@manager.command
def dropdb():
	db.drop_all()

if __name__ == '__main__':
	manager.run()