import network
import ntptime


class Network_Tools():
	def connect(self):
		from net_config import SSID, PSWD

		#connect to network
		station = network.WLAN(network.STA_IF)
		if station.isconnected():
			return	
		print('Connecting')
		station.active(True)
		print(station.scan())
		
		while True:
			try:
				station.scan()
				station.connect(SSID,PSWD)
			except:
				pass	
			if station.isconnected():
				break	
		print('Connection successful')
		print(station.ifconfig())
	
	def disconnect(self):
		from net_config import SSID, PSWD
		#connect to network
		station = network.WLAN(network.STA_IF)
		if station.isconnected():
			station.disconnect()
	
	def set_time(self):
		self.connect()	
		NTP_SERVER = '0.ch.pool.ntp.org'
		ntptime.host = NTP_SERVER
		while True:
			try:
				ntptime.settime()
				print('Time Set')
			except OSError as e:
				print(e)
			else:
				break
	
