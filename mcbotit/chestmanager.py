from mcbotit import InputKeys
import time
class ChestManager:
	def __init__(self, player):
		self.player = player
		self.chests = {}
	def openChest(self, x, y, z, maxWait=5):
		self.player.lookTowardBlock(x, y, z)
		self.player.holdFor(InputKeys.RIGHT_CLICK,0.1)
		
		start = time.time()
		while time.time()-start < maxWait:
			try:
				self.player.inventoryManager.getOpenChest()
				break
			except AssertionError:
				time.sleep(0.1)
		if time.time()-start > maxWait:
			raise Exception("Can't open chest")
	def openAndIndex(self, x, y, z, maxWait = 5):
		self.openChest(x, y, z, maxWait)
		self.indexOpenChest(x, y, z)
		self.player.closeScreen()


	def indexOpenChest(self, x, y, z):
		self.chests[(x, y, z)] = self.player.inventoryManager.getOpenChest()


	def search(self, id):
		for chestPos, chest in self.chests.items():
			for row in range(3, chest.maxRows):
				for col in range(0, chest.maxCols):
					if (item:=chest.getSlot(row, col))["type"] == id:
						return item, chestPos