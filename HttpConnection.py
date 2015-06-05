import socket
import string
class connection:
	def __init__(self, host, sfd):
		self.host = host
		self.sfd = sfd
		self.status = ''
def get_header(sfd):
    buf_size = 4096
    html=''
    recv_buffer = sfd.recv(buf_size)
    html+= recv_buffer
    if(recv_buffer.find('\r\n\r\n')!= -1):
        header = html.split('\r\n\r\n',1)[0]
        html_part = html.split('\r\n\r\n',1)[1]
        return (header, html_part)
    else:
        return (None,None)
def parse_header(header):
    content_length = 0
    chunked = False
    if "Content-Length" in header:
        start = header.find("Content-Length")
        if(start != -1):
            end = header.find('\r\n',start)
        if(start != -1 and end != -1):
            content_length = string.atoi(header[start:end].split("Content-Length:")[1].strip())
    if "Transfer-Encoding" in header:
        start = header.find("Transfer-Encoding")
        if(start != -1):
            end = header.find('\r\n',start)
            print end
        if(start != -1 and end != -1):
            if(header[start:end].split("Transfer-Encoding:")[1].strip() == "chunked"):
                chunked = True
    return (content_length, chunked)
def read_fixed_body(sfd,html_part, content_length):
    first_bytes = len(html_part)>>3 
    left_bytes = (content_length >>3) - first_bytes
    left_html_part = ""
    if(left_bytes <= 0): return  0
    while(1):
        left_html_recv = sfd.recv(content_length-len(html_part))
        left_html_part += left_html_recv
        if((len(left_html_part) >>3) >= left_bytes):
            print "recv end----------------"
            break
    return left_html_part

def read_chunked_body(sfd):
    pass
