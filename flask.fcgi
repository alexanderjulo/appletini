#!/usr/bin/env python2
from flup.server.fcgi import WSGIServer
from werkzeug.contrib.fixers import LighttpdCGIRootFix
from main import www

if __name__ == '__main__':
	WSGIServer(LighttpdCGIRootFix(www)).run()
