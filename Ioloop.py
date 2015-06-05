#select or epoll 
import Select
import socket
import select
import time
import string
import HttpConnection
import Netutil
class connection(object):
	def __init__(self, host, sfd):
		self.host = host
		self.sfd = sfd
		self.status = ''
class Ioloop_(object):
	def __init__(self):
		self.events = {}
		self.fd_handlers = {}
		self._instance = None
		self.stop = False
	def start(self):
		while not self.stop:
			self.events = self._instance.poll()
			if self.events:
				for fd in self.events.keys():
					sfd, handler_func = self.fd_handlers[fd]
					#in sequence 
					handler_func(sfd, self);
	def create_instantce(self):
		self._instance = Select._select()
	def registor_events(self, fd, event):
		self._instance.register(fd, select.EPOLLOUT)
	
	def add_handler(self, sfd, handler_func):
		self.fd_handlers[sfd.fileno()] =(sfd, handler_func)
		pass
	
