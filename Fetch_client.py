import Ioloop 
import socket
import Netutil
import select
import HttpConnection
import Queue
import thread
import Fetcher
class Fetch_Client(object):
	def __init__(self):
		self.work_mode = 'seeds'
		self.io_mode = 'select'
		self.link_mode = False
		self.seeds = ''
		self.fetcher_ = Fetcher.Fetcher()
		self.stop = False
	def set_io_mode(self,io_mode):
		self.io_mode = io_mode
	def set_work_mode(self, io_mode):
		self.work_mode = io_mode
	def set_link_mode(self, link_mode):
		self.link_mode = link_mode
	def set_seed_file(self,seed_file):
		self.seeds = seed_file
		if self.seeds:
			self.load_seeds(seeds)
	def load_seeds(self,seed_file):
		pass
	def put_request(self,url):
		self.fetcher_.put_request(url)
		
	def run(self):
		thread.start_new_thread(self.fetcher_.begin,())
		while not self.stop:
			pass
	def stop(self):
		self.stop = True

if __name__ =="__main__":
	url = "www.baidu.com"
	fetch_client = Fetch_Client()
	fetch_client.put_request(url)
	fetch_client.run()
