from www import www

@www.context_processor
def inject_config():
	title = www.config['WWW_TITLE']
	slogan = www.config['WWW_SLOGAN']
	return dict(title=title, slogan=slogan)