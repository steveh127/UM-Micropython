#defines web page actions
from web_builder import clean_text
from wopr_as import get_WOPR

class Actions():	
	def __init__(self):
		self.wopr=get_WOPR()
		self.wopr.rgb_led1.colour=self.wopr.WHITE
		self.wopr.rgb_led2.colour=self.wopr.GREEN
		self.wopr.rgb_led3.colour=self.wopr.BLUE
		self.wopr.rgb_led4.colour=self.wopr.YELLOW
		self.wopr.rgb_led5.colour=self.wopr.RED
			
	def show_colour(self,values):
		self.wopr.rgb_led1.on() if 'White' in values else self.wopr.rgb_led1.off()
		self.wopr.rgb_led2.on() if 'Green' in values else self.wopr.rgb_led2.off()
		self.wopr.rgb_led3.on() if 'Blue'  in values else self.wopr.rgb_led3.off()
		self.wopr.rgb_led4.on() if 'Yellow'in values else self.wopr.rgb_led4.off()
		self.wopr.rgb_led5.on() if 'Red'   in values else self.wopr.rgb_led5.off()
		
	def flash_colour(self,values):
		if 'White' in values:
			self.wopr.rgb_led1.to_flash=True
			return
		if 'Blue'  in values:
			self.wopr.rgb_led3.to_flash=True
			return
		if 'Green' in values:
			self.wopr.rgb_led2.to_flash=True
			return
		if 'Red'   in values:
			self.wopr.rgb_led5.to_flash=True
			return
		if 'Yellow'   in values:
			self.wopr.rgb_led4.to_flash=True
			return
			
	def show_message(self,values):
		self.wopr.clock_running=False
		text=clean_text(values[0]).upper()
		self.wopr.show_string(text)
		
	def start_clock(self,values):
		self.wopr.clock_running=True
		
	def stop_clock(self,values):
		if self.wopr.clock_running:
			self.wopr.clock_running=False
			self.wopr.display.clear()
	
	def beep_now(self,values):
		self.wopr.to_beep=True
	
	def clear_all(self,values):
		self.wopr.clock_running=False
		self.wopr.clear_leds()
		for led in self.wopr.rgb_leds:
			led.off()
	
	def show_ip(self,values):
		self.wopr.clock_running=False
		self.wopr.display.value = ''
		self.wopr.show_IP=True
		
	def time_set(self,values):
		self.wopr.set_time()
	
	def toggle_24(self,values):
		if self.wopr.twenty4:
			self.wopr.twenty4 = False 
		else:
			self.wopr.twenty4 = True
		self.wopr.save_config()
			
	def toggle_Summer(self,values):
		self.wopr.daylight_saving = not self.wopr.daylight_saving
		# if self.wopr.daylight_saving:
			# self.wopr.daylight_saving = False 
		# else:
			# self.wopr.daylight_saving = True
		self.wopr.save_config()
			
	def show_temp(self,values):
		self.wopr.clock_running=False
		self.wopr.string = str(self.sensors.temperature) + 'C'
			
	#information functions - not called as actions
	
	def get_24(self):
		if self.wopr.twenty4:
			return '24hr'
		else:
			return '12hr'
	
	def get_DS(self):
		if self.wopr.daylight_saving:
			return 'Summertime'
		else:
			return 'Greenwich Mean Time'
	

	
	

	
