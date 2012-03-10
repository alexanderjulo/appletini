#!/usr/bin/env python2.7
import sys, os

sys.path.insert(0, '/home/alexex/projects/appletini')

from flup.server.fcgi import WSGIServer
from www import www

class ApacheUberspaceRewriteFix(object):
				def __init__(self, app):
								self.app = app
				def __call__(self, environ, start_response):
								environ['SCRIPT_NAME'] = ''
								return self.app(environ, start_response)

if __name__ == '__main__':
				WSGIServer(ApacheUberspaceRewriteFix(www)).run()