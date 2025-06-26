import asyncio
import network

import mrequests

from config import SSID,PSWD
from squixl_text import screen as scr
from fonts import *

async def actions(widget):
	if widget.name == 'b1':
		if widget.blue:
			scr.write("Going, going, gone...",430, 350, BLUE,rotation=-90,font=serif32B)
			widget.blue = False
		else:
			scr.write("Going, going, gone...",430, 350, GREEN,rotation=-90,font=serif32B)
			widget.blue = True
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
		
async def get_jokes():
	net = network.WLAN(network.STA_IF)
	net.active(True)
	net.config(reconnects=0)
	i = 0
	while i < 30:
		try:
			net.connect(SSID,PSWD)
		except OSError as e:
			await asyncio.sleep(0.1)
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
	
# async def jokes():
	# while True:
		# jokes = await get_jokes()
		# if jokes is not None:	
			# for i in range(5):
				# print(jokes[i]['setup'])
				# print(jokes[i]['punchline'])
				# print()
		# else:
			# print('no jokes')
		# await asyncio.sleep(10)
		
# asyncio.run(jokes())
		

	
	
