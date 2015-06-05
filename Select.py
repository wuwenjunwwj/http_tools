import select
import socket
import time
import string
import HttpConnection
class _select(object):
	def __init__(self):
		self.rset = set()
		self.wset = set()
		self.xset = set()
		pass
	def register(self, fd, events):
		if fd in self.rset or fd in self.wset or fd in self.xset:
			print fd, self.rset, self.wset, self.xset
			raise IOError("fd %s already registered" % fd)
		if events & select.EPOLLOUT:
			self.rset.add(fd)
		if events & select.EPOLLIN:
			self.wset.add(fd)
		if events & (select.EPOLLERR |select.EPOLLHUP):
			self.error_fds.add(fd)
	def unregister(self, fd):
		if fd in self.rset:
			self.rset.remove(fd)
		if fd in self.wset:
			self.wset.remove(fd)
		if fd in self.xset:
			self.xset.remove(fd)
		pass
	def poll(self):
		print "in this poll",self.rset  
		(rset_ready, wset_ready, xset_ready) = select.select(self.rset, self.wset, self.xset)
		events={}
		if rset_ready:
			for fd in rset_ready:
				print 'fd=',fd
				events[fd] = events.get(fd, 0) | select.EPOLLOUT
			print 'some fd can read',rset_ready
		if wset_ready:
				events[fd] = events.get(fd, 0) | select.EPOLLIN 
				print 'some fd can write'
		if xset_ready:
				events[fd] = events.get(fd, 0) | select.EPOLLERR |select.EPOLLHUP
		return events
	def close(self, fd):
		pass
	def fileno(self):
		pass
