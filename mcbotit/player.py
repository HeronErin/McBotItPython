from .client import Client
from .inventoryHelper import *
class Player:
	def handlePackets(self, packet, client):
		if packet.get("cmd") == "alert":
			if packet.get("usedCommand") is not None:
				cmd = packet["usedCommand"].split(" ")[0]
				if not cmd in self.clientCommands:
					print("ERROR", packet, "is not a valid command")
				else:
					self.clientCommands[cmd](self, packet["usedCommand"])
	def __init__(self, port, keepAliveTime=0.1):
		self.client = Client(keepAliveTime, port, appendHandler=self.handlePackets)
		self.clientCommands = {}

		self.inventoryManager = InventoryManager(self.client)


	def registerCommandHook(self, command, desc, hook):
		self.client.send({"cmd": "register game command", "command": command, "desc": desc})
		self.clientCommands[command] = hook
	def clearCommands(self):
		self.client.clearCommandHooks()
		self.clientCommands = {}
	def removeCommand(self, command):
		self.client.removeCommand(command)
		del self.clientCommands[command]

	def print(self, msg):
		self.client.displayChatMessage(str(msg))
	def closeScreen(self):
		self.client.closeScreen()
	def kill(self):
		self.client.kill()
	def wait(self):
		self.client.wait()
	def holdFor(self, key, delay = 0.1, wait=True):
		self.client.holdFor(key, delay, wait)
	def keyDown(self, key):
		self.client.keyDown(key)
	def keyUp(self, key):
		self.client.keyUp(key)
	def clearKeys(self):
		self.client.clearKeys()
	def rotate(self, pitch, yaw, speed=0.6, wait=True):
		self.client.rotate(pitch, yaw, speed, wait)

	# Use item? Uses buckets but not some other items			
	def useItem(self):
		self.client.useItem()
	# Do things like open chests
	def rightClickBlock(self):
		self.client.rightClickBlock()

	# Places item from HOTBAR slot
	def place(self, x, y, z, slot, speed=0.6, wait=True):
		self.client.place(x, y, z, slot, speed, wait)
	# Mines block
	def mine(self,  x, y, z, speed=0.6, wait=True):
		self.client.mine(x, y, z, speed, wait)

	def getBlock(self, x, y, z):
		return self.client.getBlock(x, y, z)

	# Use baritone to path to locations
	def goto(self, x, y, z, wait=True):
		self.client.goto(x, y, z, wait)
	# Use baritone to walk to locations, does not break/place blocks and no sprinting. Use for short distences IE around farms or something
	def gotoOnlyWalk(self, x, y, z, wait=True):
		self.client.gotoOnlyWalk(x, y, z, wait)
	# Tells baritone to mine a block, not stable in all situations
	def baritoneMine(self, x, y, z, wait=True):
		self.client.baritoneMine(x, y, z, wait)
	# Tells baritone to place a block, not stable in all situations
	def baritonePlace(self, x, y, z, id):
		self.client.baritonePlace(x, y, z, id)

	# Right click entity, used for villagers
	def openEntity(self):
		self.client.openEntity()
	# Punch entity
	def hitEntity(self):
		self.client.hitEntity()
	def jump(self):
		self.client.jump()
	# Look at block location, good for villagers, a block does NOT need to exist there, so it CAN be used to look at entity at a location
	def lookTowardBlock(self, x, y, z, speed=0.6, wait=True):
		self.client.lookTowardBlock(x, y, z, speed, wait)

	# Slot numbers come from getOpenInventory() NOT getPlayerInventory(), using helper functions is recommended
	def swapSlots(self, slot1, slot2, delay=0.2):
		self.client.swapSlots(slot1, slot2, delay)