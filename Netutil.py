import socket
def connect_host(host, port):
	fd_handlers = {}
	try:
		sfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, e:
		print "socket error",e
		return None
	try:
		sfd.connect((host, port))
	except socket.error, e:
		print "connect error",e
		return None
	print sfd.fileno()
	return sfd
def close_fd(sfd):
	if sfd:
		sfd.close()
