import gc
import network
from socket_simple import Socket
import uasyncio as asyncio

#the next two imports define the application
from wopr_as import get_WOPR
from web_pages import links
############################################

from net_config import SSID

def extract(request):	
	request = str(request)
	#print(request)
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
		item = extracted['item'][0]
		if item in extracted:
			return (item,extracted[item])
		else:
			#if no item specified return complete extracted dictionary
			#for use with single submit button on a form
			return (item,extracted)
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
	
def web_write(request):
	web_page = get_web_page(request)
	html.send('HTTP/1.1 200 OK\n')
	html.send('Content-Type: text/html\n')
	html.send('Connection: close\n\n')
	html.send(web_page)

if not SSID:
	import net_setup

else:
	html = Socket(('',80))
	if html.status == 'disconnected':
		with  open('net_config.py','w') as net_config:
			net_config.write('SSID=\'\'\n')
			net_config.write('PSWD=\'\'\n')
		from time import sleep
		wopr=get_WOPR()
		while True:
			wopr.display.clear()
			wopr.display._show('NO NETWORK')
			wopr.display.update()
			sleep(1)
			wopr.display.clear()
			wopr.display._show('RESTART NOW')
			wopr.display.update()
			sleep(1)
	else:
		get_web_page = current_web_page(links)
		async def main():
			#do application specific setup
			wopr=get_WOPR()
			wopr.IP=html.ip
			wopr.show_IP=True
			wopr.set_time()
			await wopr.check()
			###############################
			asyncio.create_task(html.listen())
			asyncio.create_task(html.process_data(web_write))
			while True:
				await asyncio.sleep(10)
			
		asyncio.run(main())
				
