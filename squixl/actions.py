import asyncio
import network
from time import sleep

import mrequests

from config import SSID,PSWD
from squixl_text import screen as scr
from fonts import *

async def actions(widget):
	if widget.name == 'b1':
		setup,punchline = get_joke()
		#if widget.blue:
		scr.write(setup,380, 460, BLUE,rotation=-90,font=serif24B)
		#widget.blue = False
		#else:
		scr.write(punchline,430, 460, GREEN,rotation=-90,font=serif24B)
		#widget.blue = True
		await asyncio.sleep(0.5)
		return
	if widget.name == 'test':
		value = widget.value
		if widget.on:
			scr.write("Testing " + str(value),300, 70, YELLOW,rotation=-30)
			widget.value += 1
		else:
			scr.write("Testing "  + str(value - 1), 300, 70, scr.background,rotation=-30)
		await asyncio.sleep(0.5)
		return
	if widget.name == 'close':
		scr.buzz()
		await asyncio.sleep(0.5)
		scr.deinit()
		return
	if widget.name in ('red','blue','green'):
		if widget.on:
			if widget.name == 'red':
				scr.write("SQUiXL !",100,100, RED,font=serif64I)
			if widget.name == 'blue':
				scr.write("SQUiXL !",100,100, BLUE,font=serif64I)
			if widget.name == 'green':
				scr.write("SQUiXL !",100,100, GREEN,font=serif64I)
		return
	if widget.name in ('cat','mouse','dog'):
		print(widget.name)
		await asyncio.sleep(5)
		return				
	else:
		await asyncio.sleep(0.2)
		
def get_jokes():
	net = network.WLAN(network.STA_IF)
	net.active(True)
	net.config(reconnects=0)
	i = 0
	while i < 60:
		try:
			net.connect(SSID,PSWD)
		except OSError as e:
			sleep(0.1)
			i += 1
		if net.isconnected():
			break
	else:
		return None
		
	url = "https://official-joke-api.appspot.com/jokes/random/5get"
	request = mrequests.get(url, headers={b"Accept": b"application/json"})
	
	#disconnect from network
	net.disconnect()
	if request.status_code == 200:
		jokes = request.json()
	else:
		print("Request failed. Status: {}".format(request.status_code))
		request.close()
		return None
	request.close()
	return jokes
	
class Get_Joke():
	def __init__(self):
		self.jokes = None
		self.get_more_jokes()
	
	def get_more_jokes(self):
		while self.jokes is None:
			self.jokes = get_jokes()
			sleep(0.5)
		self.n = 0
	
	def __call__(self):
		joke = self.jokes[self.n]
		self.n += 1
		if self.n == 5:
			self.jokes = None
			self.get_more_jokes()
		return  joke['setup'],joke['punchline']		

get_joke = Get_Joke()	
	

	
	
