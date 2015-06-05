import Ioloop 
import socket
import  Netutil
import select
import HttpConnection
import Queue
import thread
def handle_recv(sfd, Ioloop_context):
	buf_size = 4096
	print "handle_recv",sfd.fileno()
	while 1:
		if Ioloop_context.events.get(sfd.fileno(), 0 ) & select.EPOLLOUT:
			print "hello,kitty"
			(header,html_part) = HttpConnection.get_header(sfd)
			left_html_part = ""
			html_page = ""
			if(header):
				print "header sfd ", sfd.fileno(), len(header)>>3
				content_length, chunked = HttpConnection.parse_header(header)
				if content_length:
					left_html_part = HttpConnection.read_fixed_body(sfd, html_part, content_length)
					print "before return "
					Ioloop_context._instance.unregister(sfd.fileno())
					return left_html_part
				elif chunked:
					HttpConnection.read_chunked_body(sfd)
					html_page ='%s%s'%(html_part, left_html_part)
				if Ioloop_context.events.get(sfd.fileno(), 0 ) & select.EPOLLIN:
					pass
					return
				if Ioloop_context.events.get(sfd.fileno(), 0 ) & (select.EPOLLERR |select.EPOLLHUP):
					pass
					return
class connection(object):
	def __init__(self, sfd, host):
		self.host = host
		self.sfd = sfd
		self.status = ''
		self.error = ''
		self.resource_queue = Queue.Queue()
class Fetcher(object):
	def __init__(self, method='select'):
		self.connections = {}
		self.ioloop_ = Ioloop.Ioloop_()
		self.ioloop_.create_instantce()
	def create_connection(self, Host, Port=80):
		if Host in self.connections.keys():
			return self.connections[Host]
		else:
			sfd = Netutil.connect_host(Host, Port)
			if not sfd:
				print 'connect_host error'
				return
			print type(sfd)
			connection_ = connection(sfd,Host)
			self.connections[Host] = connection_
			self.ioloop_.registor_events(sfd.fileno(), select.EPOLLOUT)
			self.ioloop_.add_handler(sfd, handle_recv)
			return connection_
	def add_resource(self, url):
		Host = url
		connection_ = self.create_connection(Host)
		connection_.resource_queue.put(url)
	def put_request(self, url):
		self.add_resource(url)
		pass
	def begin(self):
		print 'begin'
		thread.start_new_thread(self.ioloop_.start,())
		self.fetch_loop()
		
	def fetch_loop(self):
		while 1:
			for host,connection in self.connections.items():
				request_str = 'GET / HTTP/1.1\r\nHost:www.baidu.com\r\nConnection:keep-alive\r\n\r\n'
				connection.sfd.send(request_str)
				del(self.connections[host])

