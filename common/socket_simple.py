import network
from socket import socket
import asyncio

class Socket():
	def __init__(self,address):
		self.target,self.port = address
		self._get_network()
		self.conn=None
		self.data=None
	
	def _get_socket(self,*,block=True):
		s = socket() #defaults are AF_INET, SOCK_STREAM
		s.setblocking(block)
		return s
		
	def _get_network(self):
		from net_config import SSID, PSWD
		from time import sleep
		net = network.WLAN(network.STA_IF)
		net.active(True)
		while True:
			try:
				net.connect(SSID,PSWD)
			except:
				pass
			sleep(0.1)		
			if net.isconnected():
				break
		print('Connection successful')
		print(net.ifconfig()[0])
		self.ip = net.ifconfig()[0]
		
	def send(self,payload,target=None):
		if self.conn:
			self.conn.write(payload)
		else:
			s = self._get_socket()
			s.connect((target,self.port))
			s.write(payload)
			s.close()
	
	async def listen(self):
		s = self._get_socket(block=False)
		s.bind(('',self.port))
		s.listen(3)
		print('Socket listening on port ' + str(self.port))
		self.conn = None
		self.data = None
		while True:
			while self.conn is None:
				try:
					self.conn, addr = s.accept()
				except:
					await asyncio.sleep(0.1)
			print('Got a connection from ' + str(addr[0]))
			self.source = str(addr[0])
			self.data = self.conn.recv(1024)
			while self.data is not None:
				await asyncio.sleep(0.1)
			self.conn.close()
			self.conn=None
			await asyncio.sleep(0)
	
	async def process_data(self,action):
		print('process data')
		while True:
			if self.data is not None:
				action(self.data)
				self.data = None
			await asyncio.sleep(0.2)

#MASTER=('192.168.1.89',1415)
	
# async def main():	
	# sock = Socket(('',1415))
	# html = Socket(('',80))
	# asyncio.create_task(sock.listen())
	# asyncio.create_task(html.listen())
	# asyncio.create_task(sock.process_data())
	# while True:
		# await asyncio.sleep(5)
		# #sock.send('Just a Test','192.168.1.187')
		
	
	
# asyncio.run(main())
		
