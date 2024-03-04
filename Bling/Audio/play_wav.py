'''
Generic I2S board driver.

setup and tested using UM Tiny S3 (ESP32 S3) board and
12 x 14 LED display  (ESP32 S3) with MAX98357A module.

volume control added - console must change self.volume

see README
 
'''
import asyncio
from machine import Pin,SPI,I2S
import os

# SDCard seems more consistent with imported SDCard rather than internal 
# module.
from sdcard import SDCard

from board import spi,CS,SCK,WS,SD


#default sd card setup.

sd = SDCard(spi,Pin(CS),baudrate=10000000) 

class Play_WAV():
	def __init__(self,sdc=sd):
		#SD Card needs to be mounted here?
		os.mount(sdc,'/sd')
		
		# ======= I2S CONFIGURATION =======
		SCK_PIN = SCK
		WS_PIN = WS
		SD_PIN = SD
		I2S_ID = 0
		BUFFER_LENGTH_IN_BYTES = 80000

		# ======= AUDIO CONFIGURATION =======
		WAV_SAMPLE_SIZE_IN_BITS = 16
		FORMAT = I2S.STEREO
		SAMPLE_RATE_IN_HZ = 44100

		self.audio_out = I2S(
			I2S_ID,
			sck=Pin(SCK_PIN),
			ws=Pin(WS_PIN),
			sd=Pin(SD_PIN),
			mode=I2S.TX,
			bits=WAV_SAMPLE_SIZE_IN_BITS,
			format=FORMAT,
			rate=SAMPLE_RATE_IN_HZ,
			ibuf=BUFFER_LENGTH_IN_BYTES,
		)
		#control parameters 
		self.volume=-2
		self.track=None
		self.path='/sd'
		self.stop=False
		
	async def __call__(self):
		swriter = asyncio.StreamWriter(self.audio_out)
		# allocate sample array
		# memoryview used to reduce heap allocation
		wav_samples = bytearray(10000)
		wav_samples_mv = memoryview(wav_samples)

		while True:
			if self.track is not None:
				wav = open(self.path + '/' + self.track + '.wav', "rb")
				wav.seek(44)  # advance to first byte of Data section in WAV file
				print(self.path + '/' + self.track + '.wav' + ' playing')
				while True:
					num_read = wav.readinto(wav_samples_mv)
					# end of WAV file?
					if num_read == 0 or self.stop:
						break
					else:
						#volume control
						I2S.shift(buf=wav_samples_mv[:num_read],bits=16,shift=self.volume)
						swriter.out_buf = wav_samples_mv[:num_read]
						await swriter.drain()
				self.track=None
				self.stop=False
			await asyncio.sleep(0)

