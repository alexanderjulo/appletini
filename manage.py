from www import www, db

from www.user import User

from flaskext.script import Manager
manager = Manager(www)

@manager.option('-n', '--name', dest='name', default='admin')
@manager.option('-m', '--mail', dest='mail', default='admin@alexex/www')
@manager.option('-p', '--password', dest='password', default='')
def setup(name, mail, password):
	initdb()
	if password == '':
		print "You need at least to supply a password with '-p'."
		return
	else:
		user = User(name=name, password=password, mail=mail)
		db.session.add(user)
		db.session.commit()
		print("added user %s. Log in with e-mail %s and your password." % (name, mail))
	
@manager.command
def initdb():
	db.create_all()
	
@manager.command
def dropdb():
	db.drop_all()

if __name__ == '__main__':
	manager.run()