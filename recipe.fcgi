#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from runserver import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress=('localhost', 9000)).run()
    #WSGIServer(application, bindAddress='192.168.1.72:80').run()
