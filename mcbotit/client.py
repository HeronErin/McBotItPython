import socket, threading, time, json, io, enum
import python_nbt.nbt as nbt
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


# Base Client, just connects and allows you to send packets, nothing special here.
class Client(threading.Thread):
	def __init__(self, pingTime, port, packetHandler = None, appendHandler=None):
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
		while self.running: 
			time.sleep(self.pingTime)
			if self.stealControl:
				self.hasControl = True
				while self.hasControl:
					time.sleep(self.pingTime)
			else:
				self.send({"cmd": "keep alive"})

				for resp in self.recv(1024*1024):
					self.packetHandler(resp, self)



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

	# Wait for all workers to finish
	def wait(self):
		with self:
			self.send({"cmd": "wait for workers"})
			for r in self.recv(1024):
				if "job" in r:
					return
				elif "err" in r:
					raise Exception(str(r))

	# Shows the user a client side message
	def displayChatMessage(self, msg):
		self.send({"cmd": "print to chat", "msg": msg})

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

	#Smoothly rotates player
	def rotate(self, pitch, yaw, speed=0.6, wait=True):
		self.send({"cmd": "realistic rot","time_per_90":speed, "pitch": pitch, "yaw":yaw})
		if wait:
			self.wait()


	# Use item? Uses buckets but not some other items			
	def useItem(self):
		self.send({"cmd": "use item"})
	# Do things like open chests
	def rightClickBlock(self):
		self.send({"cmd": "right click block"})

	# Places item from HOTBAR slot
	def place(self, x, y, z, slot, speed=0.6, wait=True):
		with self:
			self.send({"cmd": "normal place", "x":x, "y":y, "z": z, "slot":slot-1, "time_per_90": speed})
			if wait: self.wait()
	# Mines block
	def mine(self, x, y, z,speed, wait=True):
		with self:
			self.send({"cmd": "normal break", "x":x, "y":y, "z": z, "time_per_90": speed})
			if wait: self.wait()

	# Use baritone to path to locations
	def goto(self, x, y, z, wait=True):
		with self:
			self.send({"cmd": "baritone goto normal", "x":x, "y":y, "z": z})
			if wait: self.wait()
	# Use baritone to walk to locations, does not break/place blocks and no sprinting. Use for short distences IE around farms or something
	def gotoOnlyWalk(self, x, y, z, wait=True):
		with self:
			self.send({"cmd": "baritone goto only walk", "x":x, "y":y, "z": z})
			if wait: self.wait()
	# Tells baritone to mine a block, not stable in all situations
	def baritoneMine(self, x, y, z, wait=True):
		with self:
			self.send({"cmd": "baritone break", "x":x, "y":y, "z": z})
			if wait: self.wait()
	# Tells baritone to place a block, not stable in all situations
	def baritonePlace(self, x, y, z, id):
		with self:
			self.send({"cmd": "baritone place block", "x":x, "y":y, "z": z, "id":id})

	# Right click entity, used for villagers
	def openEntity(self):
		self.send({"cmd": "interact with entity", "type": "open"})
	
	def closeScreen(self):
		self.send({"cmd": "close current screen"})
	# Punch entity
	def hitEntity(self):
		self.send({"cmd": "interact with entity", "type": "hit"})
	def jump(self):
		self.send({"cmd": "jump"})
	# Look at block location, good for villagers, a block does NOT need to exist there, so it CAN be used to look at entity at a location
	def lookTowardBlock(self, x, y, z, speed=0.6, wait=True):
		rot = None
		with self:
			self.send({"cmd":"get rotation to get to block", "x":x, "y":y, "z":z})
			rot = self.recv(1024)[0]
		self.rotate(rot["pitch"], rot["yaw"], speed=speed, wait=wait)


	# Get player location and other stats
	def getPlayerInfo(self):
		with self:
			self.send({"cmd":"get player info"})
			return self.recv(2048)[0]
	# Gets player inventory and decodes the nbt
	def getPlayerInventory(self):
		with self:
			self.send({"cmd": "get player inventory"})
			return self.readNbt()
	# Gets the slot data for an open inventory. WARNING, this packet my give you stange results, using a helper class is recommended
	def getOpenInventory(self):
		with self:
			self.send({"cmd": "get open inventory"})
			return self.readNbt()

	def getVillagerTrades(self):
		with self:
			self.send({"cmd":"get villager trade info"})
			return self.readNbt()
	def setVillagerTrade(self, id):
		self.send({"cmd":"set villager trade", "slot": id})


	# See https://wiki.vg/Protocol#Click_Container_Button
	def clickInventoryButton(self, id):
		self.send({"cmd": "click special inventory button", "buttonId": id})

	def readNbt(self):
		bytez = b""
		while (b:=self.socket.recv(1024*1024*1024)):
			bytez+=b
			if bytez.endswith(END_TOKEN): 
				bytez=bytez[:-len(END_TOKEN)]
				break
		return read_from_nbt_file(bytez).json_obj(full_json=False) 

	# Slot numbers come from getOpenInventory() NOT getPlayerInventory(), using helper functions is recommended
	def swapSlots(self, slot1, slot2, delay):
		self.send({"cmd": "swap slots", "delay": int(delay*1000), "slot1": slot1, "slot2": slot2})
