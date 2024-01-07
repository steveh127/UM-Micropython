#defines setup actions
from web_builder import clean_text
from wopr_as import get_WOPR
from time import sleep
import network

class Actions():	
	def __init__(self):
		self.wopr=get_WOPR()
		self.wopr.rgb_led1.colour=self.wopr.WHITE
		self.wopr.rgb_led2.colour=self.wopr.GREEN
		self.wopr.rgb_led3.colour=self.wopr.BLUE
		self.wopr.rgb_led4.colour=self.wopr.YELLOW
		self.wopr.rgb_led5.colour=self.wopr.RED
		self.SSID=''
		self.PSWD=''
		self.wopr.display._show('192.168.4.1',justify='C')
		self.wopr.display.update()
			
	def show_colour(self,values):
		self.wopr.rgb_led1.on() if 'White' in values else self.wopr.rgb_led1.off()
		self.wopr.rgb_led2.on() if 'Green' in values else self.wopr.rgb_led2.off()
		self.wopr.rgb_led3.on() if 'Blue'  in values else self.wopr.rgb_led3.off()
		self.wopr.rgb_led4.on() if 'Yellow'in values else self.wopr.rgb_led4.off()
		self.wopr.rgb_led5.on() if 'Red'   in values else self.wopr.rgb_led5.off()
		
	def beep_now(self,values):
		self.wopr.buzzer.init(self.wopr.beep_freq)
		sleep(self.wopr.beep_length) 
		self.wopr.buzzer.deinit()
	
	def save_config(self,values):
		self.SSID=values['SSID'][0]
		self.PSWD=values['PSWD'][0]
		self._save_net_config()
		
		self.wopr.offset=int(values['UTC_offset'][0])
		H2412=values['HR12OR24'][0]
		if H2412 == '24hr':
			self.wopr.twenty4=True
		else:
			self.wopr.twenty4=False
		DS=values['DS'][0]
		if DS == 'On':
			self.wopr.daylight_saving=True
		else:
			self.wopr.daylight_saving=False
		self.wopr.save_config()
		self.wopr.display.clear()
		self.wopr.display._show('RESTART NOW')
		self.wopr.display.update()
		
	
	def _save_net_config(self):
		with  open('net_config.py','w') as net_config:
			net_config.write('SSID=\'' + self.SSID + '\'\n')
			net_config.write('PSWD=\'' + self.PSWD + '\'\n')

		
	def get_ds(self):
		if self.wopr.daylight_saving:
			return 'On'
		else:
			return 'Off'
		
	def get_1224(self):
		if self.wopr.twenty4:
			return '24hr'
		else:
			return '12hr'
	
	def get_offset(self):
		return str(self.wopr.offset)

	def get_SSID(self):
		return self.SSID
	
	def get_PSWD(self):
		return self.PSWD
			
	def get_best_net(self):
		if not self.SSID:
			st = network.WLAN(network.STA_IF)
			st.active(True)
			best_net=(st.scan()[0][0]).decode('UTF-8')
			st.active(False)
			self.SSID=best_net
		return self.SSID
