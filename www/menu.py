from www import www, db

if www.config['WWW_MENU_PAGE']:
	from www.page import Page

menu = {'blueprint': [], 'final': []}

def clear():
	menu['final'] = []

def register(name=None, link=None):
	if (name or link) is None:
		return False		
	elif [name, link] in menu['blueprint']:
		return False
	else:
		menu['blueprint'].append([name, link])
		return True
		
def build():
	menu['final'] = menu['blueprint']
	if www.config['WWW_MENU_PAGE']:
		entries = Page.query.filter(Page.menu != '').all()
		for entry in entries:
			entry = [entry.menu, entry.path]
			menu['final'].append(entry)

@www.context_processor
def inject_menu():
	if menu['final'] == []:
		build()
	return dict(menu=menu['final'])

