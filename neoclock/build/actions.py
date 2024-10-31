#defines dashboard actions
from machine import Pin
from neopixel import NeoPixel
import network
from colour_config import H10C,H1C,M10C,M1C
from time import sleep

class Actions():	
	
	def __init__(self):
		self.neo = NeoPixel(Pin(2),64)
		self.neo.fill((0,0,1))
		self.neo.write()
		
		self.ssid=''
		self.pswd=''
		self.shape='blocks'
		self.H12='False'
		self.UTC_offset='0'
		
		self._show()
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
		self._show()
		self.H12=values['Time_radio'][0]
		if self.H12 == '12hr':
			self.H12='True'
		else:
			self.H12='False'
		self.UTC_offset=values['UTC_input'][0]
		self._save_net_config()		
	
	def _show(self):
		self.neo.fill((0,0,0))
		self.neo.write()
		if self.shape == 'blocks':
			self.H10 = [9,10,11,17,18,19,25,26,27]	
			self.H1  = [12,13,14,20,21,22,28,29,30]
			self.M10 = [33,34,35,41,42,43,49,50,51]
			self.M1  = [36,37,38,44,45,46,52,53,54]
		if self.shape == 'circles':
			self.H10 = [27,28,35,36]	
			self.H1  = [18,19,20,21,26,29,34,37,42,43,44,45]
			self.M10 = [9,10,11,12,13,14,17,22,25,30,33,38,41,46,49,50,51,52,53,54]
			self.M1  = [0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63]	
		if self.shape == 'random':
			self.H10 = [9,13,11,37,52,19,45,26,27]	
			self.H1  = [12,10,41,20,51,22,18,29,30]
			self.M10 = [33,54,46,14,42,43,49,50,21]
			self.M1  = [36,17,38,44,25,35,28,53,34]
		for n in self.H10:
			self.neo[n]=H10C
		for n in self.H1:
			self.neo[n]=H1C	
		for n in self.M10:
			self.neo[n]=M10C
		for n in self.M1:
			self.neo[n]=M1C		
		self.neo.write()	
					
	def _save_net_config(self):
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
	
	def show(self,values):
		self.shape=values[0]
		self._show()
