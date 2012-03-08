import sys, os

link = "%s%s" % (os.getcwd(), "/appletini")

sys.path.insert(0, link)
from www import www as application
