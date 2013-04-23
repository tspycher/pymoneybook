'''
Created on Mar 2, 2013

@author: thospy
'''

import sys
import time, threading

from controller import *

try:
    import tornado.ioloop
    import tornado.web
except ImportError:
    sys.stderr.write("Looks like you have tornado not installed. (apt-get install python-tornado)")
    sys.exit(1)

class Server(object):
    controllers = ['Messages', 'Emails']
    routes = []

    def __init__(self):
        pass
    
    def _buildRoutes(self):
        for c in self.controllers: 
            self.routes.append((r"/%s/(.*)" % c.lower(), eval("%sController" % c)))
        
    def start(self, port = 8888, as_thread = False):
        self._buildRoutes()
        application = tornado.web.Application(self.routes)
        application.listen(port)
        
        if as_thread:
            threading.Thread(target=self._start).start()
            return True
        else:
            self._start()
    
    def _start(self):
        tornado.ioloop.IOLoop.instance().start()
    
    def stop(self):
        tornado.ioloop.IOLoop.instance().stop()
