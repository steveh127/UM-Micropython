#defines dashboard actions
from machine import Pin
from neopixel import NeoPixel
import network
from colour_config import H10C,H1C,M10C,M1C
from time import sleep
from machine import Pin
import sys

class Actions():	
	
	def __init__(self):
		Pin(5,Pin.OUT).value(1)
		self.neo = NeoPixel(Pin(6),81)
		self.neo.fill((0,0,1))
		self.neo.write()
		self.ssid=''
		self.pswd=''
		self.shape='blocks'
		self.H12='False'
		self.UTC_offset='0'
		self.best_net=self._get_best_net()
	
	def process(self,strings):
		string_list=[]
		for string in strings:
			string=string.replace('+',' ')
			string_list.append(string)
		return tuple(string_list)
	
	def submit(self,values):	
		self.ssid=values['SSID_input'][0]
		self.pswd=values['PSWD_input'][0]
		if not self.pswd or not self.ssid:
			#flag error
			return
		self.ssid,self.pswd = self.process((self.ssid,self.pswd))	
		print(self.ssid + ' ' + self.pswd)
		self.shape=values['Type_radio'][0]
		self.H12=values['Time_radio'][0]
		if self.H12 == '12hr':
			self.H12='True'
		else:
			self.H12='False'
		self.UTC_offset=values['UTC_input'][0]
		self.save_net_config()
		sleep(5)
		sys.exit()			
					
	def save_net_config(self):
		net_config = open('net_config.py','w')
		net_config.write('SSID=\'' + self.ssid + '\'\n')
		net_config.write('PSWD=\'' + self.pswd + '\'\n')
		net_config.write('SHAPE=\'' + self.shape + '\'\n')
		net_config.write('H12=' + self.H12 + '\n')
		net_config.write('OFFSET=' + self.UTC_offset + '\n')
		net_config.close()
		self.neo.fill((0,1,0))
		self.neo.write()

	
	def _get_best_net(self):
		st = network.WLAN(network.STA_IF)
		st.active(True)
		best_net=(st.scan()[0][0]).decode('UTF-8')
		st.active(False)
		return best_net
	
