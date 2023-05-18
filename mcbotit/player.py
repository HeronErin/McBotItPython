from .client import Client
from .inventoryHelper import *
class Player:
	def __init__(self, port, keepAliveTime=0.1):
		self.clientConnection = Client(keepAliveTime, port)
		
