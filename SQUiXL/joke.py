import asyncio
import network
from time import sleep

import mrequests

from config import SSID,PSWD

async def get_jokes():
	net = network.WLAN(network.STA_IF)
	net.active(True)
	net.config(reconnects=0)
	i = 0
	while i < 60:	
		try:
			net.connect(SSID,PSWD)
		except OSError as e:
			asyncio.sleep(0.1)
			i += 1
		if net.isconnected():
			print('connected')
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
		asyncio.run(self.get_more_jokes())
		self.n = 0
	
	async def get_more_jokes(self):
		while self.jokes is None:
			self.jokes = await get_jokes()
			await asyncio.sleep(0.5)
		self.n = 0
	
	async def __call__(self):
		joke = self.jokes[self.n]
		self.n += 1
		if self.n == 5:
			self.n = 0
			#self.jokes = None
			#await self.get_more_jokes()
		return  joke['setup'],joke['punchline']		

# async def main():
	# joke = Get_Joke()
	# for i in range(6):
		# print(await joke())
		# print()

# asyncio.run(main())
