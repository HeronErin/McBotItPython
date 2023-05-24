import socket, threading, time, json, io, enum
import python_nbt.nbt as nbt
from typing import Callable
END_TOKEN  = b"This is the ending text of the nbt stream1234567899876543210\x00\x00\x00\x00"
def read_from_nbt_file(_file) -> nbt.TAG:
    """
	Read NBTTagCompound from a NBT packet   thanks to https://github.com/TowardtheStars/Python-NBT/blob/master/python_nbt/nbt.py
	"""
    _file = io.BytesIO(_file)
    _type = nbt.NBTTagByte(buffer=_file).value
    _name = nbt.NBTTagString(buffer=_file).value
    return nbt.TAGLIST[_type](buffer=_file)

def handlePackets(packet, client, appendHandler):
	appendHandler(packet, client)

class InputKeys(enum.Enum):
	FORWARD = "forward"
	BACKWORD = "back"
	LEFT = "left"
	RIGHT = "right"
	SNEAK = "sneak"
	LEFT_CLICK = "left click"
	RIGHT_CLICK = "right click"



class Client(threading.Thread):
	""" Base Client, just connects and allows you to send packets, nothing special here. Only use through the Player class"""

	send : Callable[dict, None]
	recv : Callable[int, dict]
	def __init__(self, pingTime: float, port: int, packetHandler = None, appendHandler=None):
		assert not(appendHandler is not None and packetHandler is not None)
		self.appendHandler = appendHandler
		if packetHandler is None: packetHandler = lambda x, y: handlePackets(x, y, self.appendHandler)
		self.packetHandler = packetHandler
		


		self.withStatementDeph = 0
		self.pingTime = pingTime
		self.socket = socket.create_connection(("127.0.0.1", port))
		self.running = True


		self.stealControl = False
		self.hasControl = False

		self.send = lambda x: self.socket.sendall(json.dumps(x).encode("utf-8")+b"\n")
		self.recv = lambda x: [json.loads(b.decode("utf-8")) for b in self.socket.recv(x).split(b"\n") if len(b)]

		threading.Thread.__init__(self)
		self.start()

	def run(self):
		""" Don't call me"""
		
		while self.running: 
			if self.stealControl:
				self.hasControl = True
				while self.hasControl:
					time.sleep(self.pingTime/4)
			else:
				self.send({"cmd": "keep alive"})

				for resp in self.recv(1024*1024):
					self.packetHandler(resp, self)
				time.sleep(self.pingTime)



	def __enter__(self):
		self.withStatementDeph+=1
		if self.withStatementDeph == 1:
			self.stealControl = True
			while not self.hasControl:
				time.sleep(self.pingTime/3)

	def __exit__(self, *_):
		self.withStatementDeph-=1
		if self.withStatementDeph == 0:
			self.stealControl = False
			self.hasControl = False

	def kill(self):
		self.running = False
		self.join()

	def wait(self):
		"""Wait for all workers to finish"""

		with self:
			self.send({"cmd": "wait for workers"})
			for r in self.recv(1024):
				if "job" in r:
					return
				elif "err" in r:
					raise Exception(str(r))


	def disconnect(self):
		self.send({"cmd": "disconnect"})


	def displayChatMessage(self, msg):
		"""Shows the user a client side message"""
		self.send({"cmd": "print to chat", "msg": msg})

	def sendPublicChatMessage(self, msg):
		self.send({"cmd": "send public chat message", "msg": msg})

	def clearCommandHooks(self):
		self.send({"cmd": "clear registered game commands"})
	def removeCommand(self, cmd):
		self.send({"cmd": "remove registered game command", "command": cmd})
	def listCommands(self):
		with self:
			self.send({"cmd": "get registered game commands"})
			return self.recv(1024*1024)
	def holdFor(self, key, delay = 0.1, wait=True):
		assert type(key) is InputKeys
		
		self.send({"cmd": "hold button for time", "key": key.value, "delay": int(delay*1000)})
		if wait: self.wait()
	def keyDown(self, key):
		assert type(key) is InputKeys
		self.send({"cmd": "hold button", "key": key.value})
	def keyUp(self, key):
		assert type(key) is InputKeys
		self.send({"cmd": "release button", "key": key.value})
	def clearKeys(self):
		self.send({"cmd": "release all buttons"})


	def rotate(self, pitch, yaw, speed=0.6, wait=True):
		"""Smoothly rotates player"""
		self.send({"cmd": "realistic rot","time_per_90":speed, "pitch": pitch, "yaw":yaw})
		if wait:
			self.wait()


				
	def useItem(self):
		"""Use item? Uses buckets but not some other items"""
		self.send({"cmd": "use item"})
	
	def rightClickBlock(self):
		"""Do things like open chests"""
		self.send({"cmd": "right click block"})

	
	def place(self, x, y, z, slot, speed=0.6, wait=True):
		"""Places item from HOTBAR slot"""
		with self:
			self.send({"cmd": "normal place", "x":x, "y":y, "z": z, "slot":slot-1, "time_per_90": speed})
			if wait: self.wait()


	
	def printerPlace(self, x, y, z, slot):
		"""Places item from HOTBAR slot, WARNING: might get you banned"""

		self.send({"cmd": "printer place", "x":x, "y":y, "z": z, "slot":slot-1})

	
	def mine(self, x, y, z,speed, wait=True):
		"""Mines block"""

		with self:
			self.send({"cmd": "normal break", "x":x, "y":y, "z": z, "time_per_90": speed})
			if wait: self.wait()
	def setHotbarSlot(self, slot):
		self.send({"cmd": "set hotbar slot", "slot": slot-1})
	
	def goto(self, x, y, z, wait=True):
		"""Use baritone to path to locations"""
		with self:
			self.send({"cmd": "baritone goto normal", "x":x, "y":y, "z": z})
			if wait: self.wait()
	
	def gotoOnlyWalk(self, x, y, z, wait=True):
		"""Use baritone to walk to locations, does not break/place blocks and no sprinting. Use for short distences IE around farms or something"""

		with self:
			self.send({"cmd": "baritone goto only walk", "x":x, "y":y, "z": z})
			if wait: self.wait()
	
	def baritoneMine(self, x, y, z, wait=True):
		"""Tells baritone to mine a block, not stable in all situations"""

		with self:
			self.send({"cmd": "baritone break", "x":x, "y":y, "z": z})
			if wait: self.wait()
	
	def baritonePlace(self, x, y, z, id):
		"""Tells baritone to place a block, not stable in all situations"""

		with self:
			self.send({"cmd": "baritone place block", "x":x, "y":y, "z": z, "id":id})

	
	def openEntity(self):
		"""Right click entity, used for villagers"""

		self.send({"cmd": "interact with entity", "type": "open"})
	
	def closeScreen(self):
		self.send({"cmd": "close current screen"})
	# Punch entity
	def hitEntity(self):
		self.send({"cmd": "interact with entity", "type": "hit"})
	def jump(self):
		self.send({"cmd": "jump"})
	def enableElytra(self):
		self.send({"cmd": "start fall flying"})
	
	def lookTowardBlock(self, x, y, z, speed=0.6, wait=True):
		"""Look at block location, good for villagers, a block does NOT need to exist there, so it CAN be used to look at entity at a location"""

		rot = None
		with self:
			self.send({"cmd":"get rotation to get to block", "x":x, "y":y, "z":z})
			rot = self.recv(1024)[0]
			self.rotate(rot["pitch"], rot["yaw"], speed=speed, wait=wait)


	
	def getPlayerInfo(self):
		"""Get player location and other stats"""

		with self:
			self.send({"cmd":"get player info"})
			return self.recv(2048)[0]
	
	def getPlayerInventory(self):
		"""Gets player inventory and decodes the nbt"""

		with self:
			self.send({"cmd": "get player inventory"})
			return self.readNbt()
	
	def getOpenInventory(self):
		"""Gets the slot data for an open inventory. WARNING, this packet my give you stange results, using a helper class is recommended"""

		with self:
			self.send({"cmd": "get open inventory"})
			return self.readNbt()

	def getBlock(self, x, y, z):
		with self:
			self.send({"cmd": "get block", "x": x, "y": y, "z": z})
			return self.readNbt()

	def getVillagerTrades(self):
		with self:
			self.send({"cmd":"get villager trade info"})
			return self.readNbt()
	def setVillagerTrade(self, id):
		""" Selects a villagers trade based on index"""

		self.send({"cmd":"set villager trade", "slot": id})


	
	def clickInventoryButton(self, id):
		"""See https://wiki.vg/Protocol#Click_Container_Button"""
		self.send({"cmd": "click special inventory button", "buttonId": id})

	def readNbt(self):
		bytez = b""
		while (b:=self.socket.recv(1024*1024*1024)):
			bytez+=b
			if bytez.endswith(END_TOKEN): 
				bytez=bytez[:-len(END_TOKEN)]
				break
		return read_from_nbt_file(bytez).json_obj(full_json=False) 


	def swapSlots(self, slot1, slot2, delay):
		"""Slot numbers come from getOpenInventory() NOT getPlayerInventory(), using helper functions is recommended"""
		self.send({"cmd": "swap slots", "delay": int(delay*1000), "slot1": slot1, "slot2": slot2})
