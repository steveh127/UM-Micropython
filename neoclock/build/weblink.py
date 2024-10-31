#version of web link that creates and uses local access point
#for device configuration.
import gc
import network
from socket import socket
import uasyncio as asyncio

from web_pages import links

def get_http_socket():
	ap = network.WLAN(network.AP_IF)
	ap.active(True)	
	ap.config(essid='CLOCK') #insecure version only for temporary use
	print(ap.ifconfig())
	s = socket() #defaults are AF_INET, SOCK_STREAM
	s.setblocking(False)
	s.bind(('', 80))
	s.listen(5)
	return s

def extract(request):	
	request = str(request)
	if '?' in request:
		(_,options)=request.split('?',1)
		(options,_)=options.split(' ',1)
		if '&' in options:
			options=options.split('&')
		else:
			options=[options]
		extracted={}
		for option in options:
			key,value = option.split('=')
			if key in extracted:
				extracted[key].append(value)
			else:
				extracted[key]=[value]
		if 'submit' in extracted:
			return ('submit',extracted)
		item = extracted['item'][0]
		if item in extracted:
			return (item,extracted[item])
		else:
			return (item,[])
	return('',[])

#closure to manage web pages
def current_web_page(link_list):
	current=link_list['home']
	links = link_list
	def get(request):
		nonlocal current
		item,values = extract(request)
		print(item + ' ' + str(values))
		#check if item is a new page request
		for key in links:
			if key==item:
				if isinstance(links[item],dict):
					try:
						current=links[item][values[0]]
					#if nothing selected nothing happens
					except IndexError as e:
						pass
				else:
					current=links[item]	
		#take required action (if any)
		current.action(item,values)
		#write web page to maintain dynamic content
		gc.collect()
		return current.write(item,values)	
	return get

async def main():
	get_web_page=current_web_page(links)
	socket = get_http_socket()
	conn = None
	request=''
	while True:
		while not conn:
			try:
				conn, addr = socket.accept()
				conn.setblocking(True)
			except:
				await asyncio.sleep(0.1)
		print('Got a connection from' + str(addr))
		request = conn.recv(1024)
		web_page = get_web_page(request)
		conn.send('HTTP/1.1 200 OK\n')
		conn.send('Content-Type: text/html\n')
		conn.send('Connection: close\n\n')
		conn.sendall(web_page)
		conn.setblocking(False)
		conn.close()
		conn = None
		
asyncio.run(main())
		
