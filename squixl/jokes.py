"""Send GET request expecting JSON in the response body and print and decode it."""
import asyncio
import network
import mrequests
from config import SSID,PSWD

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
	
async def jokes():
	jokes = await get_jokes()
	if jokes is not None:	
		for i in range(5):
			print(jokes[i]['setup'])
			print(jokes[i]['punchline'])
			print()
	else:
		print('no jokes')
	await asyncio.sleep(10)
		
asyncio.run(jokes())
