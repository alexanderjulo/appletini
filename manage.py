from www import www, db

from flaskext.script import Manager
manager = Manager(www)

@manager.command
def initdb():
	db.create_all()
	
@manager.command
def dropdb():
	db.drop_all()

if __name__ == '__main__':
	manager.run()