from .client import Client, InputKeys
from .inventoryHelper import *
from threading import Thread
from typing import Callable
class Player:
	_prevY = 0
	lastX : float
	lastY : float
	lastZ : float
	lastHunger : int
	lastHealth : float
	lastYaw : float
	lastPitch : float
	isFalling : bool
	lastVelocity : tuple[float, float, float]
	inventoryManager: InventoryManager

	def handlePackets(self, packet: dict, client: Client):
		""" Called internally when a packed comes in after a keepalive is send"""

		if packet.get("cmd") == "alert":
			if packet.get("usedCommand") is not None:
				cmd = packet["usedCommand"].split(" ")[0]
				print(cmd)
				if not cmd in self.clientCommands:
					print("ERROR", packet, "is not a valid command")
				else:
					func, doThread = self.clientCommands[cmd]
					if doThread:
						Thread(target=func, args=(self, packet["usedCommand"], )).start()
					else:
						client.withStatementDeph+=1
						try:
							func(self, packet["usedCommand"])
						finally:
							client.withStatementDeph-=1
		elif packet.get("cmd") == "keep going":

			self.lastX = packet["x"]
			self.lastY = packet["y"]
			self.lastZ = packet["z"]
			self.lastHunger = packet["hunger"]
			self.lastHealth = packet["health"]
			self.lastYaw = packet["yaw"]
			self.lastPitch = packet["pitch"]
			self.isFalling = self.lastY < self._prevY
			self._prevY=self.lastY

			# print(self.lastY, self.isFalling, "falling")
			self.lastVelocity = (packet["velx"], packet["vely"], packet["velz"])

	def __init__(self, port: int, keepAliveTime=0.1):
		"""Port should come from the game's chat. KeepAliveTime is the time between keepalive packets, AKA updates in player info. """

		self.client = Client(keepAliveTime, port, appendHandler=self.handlePackets)
		self.clientCommands = {}

		self.inventoryManager = InventoryManager(self.client)


	def registerCommandHook(self, command: str, desc: str, hook : Callable[["Player", str], None], spinIntoThread=True):
		"""hook should be a function/lambda with these arguments: player, command"""

		self.client.send({"cmd": "register game command", "command": command, "desc": desc})
		self.clientCommands[command] = (hook, spinIntoThread)
	def clearCommands(self):
		""" Remove all registered commands"""
		self.client.clearCommandHooks()
		self.clientCommands = {}
	def removeCommand(self, command : str):
		""" Clear all client commands"""

		self.client.removeCommand(command)
		del self.clientCommands[command]


	def disconnect(self):
		self.client.disconnect()

	def print(self, msg : str):
		""" Displays a message to the client, not the public"""

		self.client.displayChatMessage(str(msg))
	def sendMessage(self, msg : str):
		""" Sends a chat message to the PUBLIC"""

		self.client.sendPublicChatMessage(msg)

	def closeScreen(self):
		""" Close an open gui, like a chest"""

		self.client.closeScreen()
	def kill(self):
		""" stop connection thread """
		self.client.kill()
	def wait(self):
		"""wait for running jobs to finish"""

		self.client.wait()
	def holdFor(self, key:InputKeys, delay = 0.1, wait=True):
		self.client.holdFor(key, delay, wait)
	def keyDown(self, key: InputKeys):
		self.client.keyDown(key)
	def keyUp(self, key):
		self.client.keyUp(key)
	def clearKeys(self):
		self.client.clearKeys()
	def rotate(self, pitch: float, yaw: float, speed=0.6, wait=True):
		"""Smoothly and realisticly rotates between to a point, speed is the time for 90 degrees in secounds"""

		self.client.rotate(pitch, yaw, speed, wait)


	def getPlayerInfo(self) -> dict:
		return self.client.getPlayerInfo()

	def setHotbarSlot(self, slot: int):
		assert slot <= 9
		assert slot != 0
		self.client.setHotbarSlot(slot)

				
	def useItem(self):
		"""Use item? Uses buckets but not some other items"""

		self.client.useItem()

	def rightClickBlock(self):
		"""Do things like open chests"""

		self.client.rightClickBlock()

	
	def place(self, x: int, y:int, z:int, slot: int, speed=0.6, wait=True):
		"""Places item from HOTBAR slot"""

		assert slot <= 9
		assert slot != 0
		self.client.place(x, y, z, slot, speed, wait)
	
	def mine(self,  x: int, y: int, z: int, speed=0.6, wait=True):
		"""Mines block"""

		self.client.mine(x, y, z, speed, wait)


	def getBlock(self, x:int, y:int, z:int) -> dict:
		"""Get info from loaded block"""

		return self.client.getBlock(x, y, z)

	
	def goto(self, x: int, y: int, z: int, wait=True):
		"""Use baritone to path to locations"""

		self.client.goto(x, y, z, wait)
	
	def gotoOnlyWalk(self, x: int, y : int, z : int, wait=True):
		"""Use baritone to walk to locations, does not break/place blocks and no sprinting. Use for short distences IE around farms or something"""

		self.client.gotoOnlyWalk(x, y, z, wait)
	
	def baritoneMine(self, x : int, y : int, z : int, wait=True):
		"""Tells baritone to mine a block, not stable in all situations"""
		self.client.baritoneMine(x, y, z, wait)
	
	def baritonePlace(self, x: int, y : int, z : int, id : str):
		"""Tells baritone to place a block, not stable in all situations"""

		self.client.baritonePlace(x, y, z, id)

	def printerPlace(self,  x: int, y : int, z : int, slot : int):
		"""Places item from HOTBAR slot, WARNING: might get you banned"""

		assert slot <= 9
		assert slot != 0
		self.client.place(x, y, z, slot)


	
	def openEntity(self):
		"""Right click entity, used for villagers"""

		self.client.openEntity()

	def hitEntity(self):
		"""Punch entity"""

		self.client.hitEntity()
	def jump(self):
		self.client.jump()

	def lookTowardBlock(self, x: int, y: int, z: int, speed=0.6, wait=True):
		"""Look at block location, good for villagers, a block does NOT need to exist there, so it CAN be used to look at entity at a location"""

		self.client.lookTowardBlock(x, y, z, speed, wait)

	
	def swapSlots(self, slot1: int, slot2: int, delay=0.2):
		"""Slot numbers come from an inventory NOT getPlayerInventory(), using helper functions is recommended"""
		self.client.swapSlots(slot1, slot2, delay)