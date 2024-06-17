	#sort out daylight saving - 4th Sunday in March & October		
	def _set_ds(self):
		(_,month,day,dow,_,_,_,_) = self.rtc.datetime()
		if month in [11,12,1,2,3]:
			self.ds = False
		if month in [4,5,6,7,8,9,10]:
			self.ds = True	
		if month == 3 and dow == 6 and day > 24:
			self.ds = True
		if month == 3 and (day + (6 - dow)) > 30:
			self.ds = True		
		if month == 10 and dow == 6 and day > 24:
			self.ds = False	
		if month == 10 and (day + (6 - dow)) > 30:
			self.ds = False
