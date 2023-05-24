from mcbotit import Player, chestmanager, MapSchematic, InputKeys
from functools import lru_cache
import time, math, sys, json, os, random

from mcbotit import Chest1Inventory, Chest2Inventory, Chest3Inventory, Chest4Inventory, Chest5Inventory, Chest6Inventory



PORT = 16256
player = Player(PORT, keepAliveTime=0.05)

blockBase = (-64, 147, -64)
chestStandLoc = (-63, 147, -63)

build_segment_size = 3
chests = (
	(14652, 81, 3390),
	(14652, 80, 3390),
	(14652, 79, 3390),

	(14652, 81, 3389),
	(14652, 80, 3389),
	(14652, 79, 3389),

	(14652, 81, 3387),
	(14652, 80, 3387),
	(14652, 79, 3387),

	(14652, 79, 3385),
	)


supportingBlock = "minecraft:cobblestone_slab"

schematic = MapSchematic("mapart.nbt")

def fround(x):
	return math.floor(x) if 0 < x else math.ceil(x)


blockDict = {} if not os.path.exists("rowExistsInfo.json") else json.load(open("rowExistsInfo.json", "r"))
def hasRowCached(row):
	if (ret:=blockDict.get(str(row))):
		return ret
	else:
		ret = player.getBlock(blockBase[0]+row, blockBase[1], blockBase[2])["id"]!="minecraft:air"
		blockDict[str(row)] = ret
		json.dump(blockDict, open("rowExistsInfo.json", "w"))
		return ret
def getItemToSlot(idd, hotbar = 1):
	playerinv = player.inventoryManager.getOpenPlayerInventory()
	base = playerinv.getSlot(0, hotbar-1)
	if base["type"] != idd:

		for row in range(0, 4):
			for col in range(0, 9):
				if (slot:=playerinv.getSlot(row, col))["type"] == idd:
					player.swapSlots(slot["id"], base["id"]     )
					print(slot, "a")
					return
def eatFood():
	while player.lastHunger != 20:
		player.setHotbarSlot(9)
		player.useItem()
		time.sleep(2)

def safeShift(rot, lenn, start=None):
	start = (player.lastX, player.lastY, player.lastZ) if start is None else start
	player.rotate(*rot)


	player.keyDown(InputKeys.SNEAK)
	try:
		while abs(start[0]-player.lastX)+abs(start[2]-player.lastZ) <= lenn:
			getItemToSlot(supportingBlock)

			player.holdFor(InputKeys.BACKWORD, 0.9, wait=False)
			time.sleep(1)
			player.holdFor(InputKeys.RIGHT_CLICK, 0.1, wait=False)
			time.sleep(0.55)
	finally:
		player.keyUp(InputKeys.SNEAK)
def lookwalk(x, z, required_distance_squared = 3):
	oldPing = player.client.pingTime
	player.client.pingTime = 0.01
	def tmp():
		with player.client:
			player.client.send({"cmd":"get rotation to get to block", "x":x, "y":player.lastY, "z":z})
			rot = player.client.recv(1024)[0]
			player.client.rotate(0, rot["yaw"])
	tmp()
	player.keyDown(InputKeys.FORWARD)
	try:
		while (player.lastX-x)**2 + (player.lastZ-z)**2 > required_distance_squared:
			tmp()

			time.sleep(0.01)
	finally:
		player.keyUp(InputKeys.FORWARD)
		player.client.pingTime=oldPing

def outline():
	player.setHotbarSlot(1)
	# (-64, 6, -64)
	# lookwalk(blockBase[0], blockBase[2]-1)
	safeShift((80, 90), 128, start=(blockBase[0], blockBase[1]+1, blockBase[2]-1))
	safeShift((80, 180), 129, start=(blockBase[0]+128, blockBase[1]+1, blockBase[2]-1)) # (64, 7, -65)
	safeShift((80, -90), 128, start=(blockBase[0]+128, blockBase[1]+1, blockBase[2]+128)) # (64, 7, 64)
	safeShift((80, 0), 129, start=(blockBase[0]-1, blockBase[1]+1, blockBase[2]+128)) # -65, 7, 64)

def makeRowBatch(rows):

	if rows:
		lookwalk(chestStandLoc[0], chestStandLoc[2], required_distance_squared=4)


		# Calculate cost to build rows
		costsL = [schematic.getRowCosts(row) for row in rows]
		costs = {}
		for cost in costsL: 
			for k, v in cost.items():
				costs[k] = costs.get(k, 0) + v
				costs[supportingBlock] = costs.get(supportingBlock, 0) + v
		
		print(costs)
		# exit()
		currentChest = None
		openChest = None

		# Clear inv of blocks not required
		if any([slot["id"].endswith("_carpet") and not(slot["id"] in costs) for slot in player.client.getPlayerInventory()]):
			result, currentChest = chestManager.search("minecraft:air")
			chestManager.openChest(*currentChest)

			openChest = player.inventoryManager.getOpenChest()

			for row in range(0, 4):
				for col in range(0, 9):
					slot = openChest.getSlot( row, col)
					if slot["type"].endswith("_carpet") and not(slot["type"] in costs):
						player.swapSlots(slot["id"], result["id"])
						time.sleep(0.1)

						chestManager.indexOpenChest(*currentChest)		
						dumpChestData()


		#Compare player inventory to required material
		def compareCosts():
			playerInvCount = {}
			for slot in player.client.getPlayerInventory():
				playerInvCount[slot["id"]] = playerInvCount.get(slot["id"], 0) + slot["Count"]
			return {k: v-playerInvCount.get(k, 0) for k, v in costs.items() if v-playerInvCount.get(k, 0) > 0}
		
		# Get required material from chest area
		while len((trueCosts:=compareCosts()).items()):
			print(trueCosts)
			for id in trueCosts.keys():
				if openChest is not None:
					items =[s for s in openChest.search(id) if s["type"] == id and s["id"] < openChest.playerInvEnd-(4*9)]
					if len(items):
						slot = openChest.searchPlayerInv("minecraft:air")
						if slot is None:
							raise Exception("Inventory full")
						player.swapSlots(slot["id"], items[0]["id"])

						time.sleep(0.5)
						openChest = player.inventoryManager.getOpenChest()
						chestManager.indexOpenChest(*currentChest)		
						dumpChestData()

						

						
						break

				result, currentChest = chestManager.search(id)
				player.closeScreen()
				chestManager.openChest(*currentChest)
				

				openChest = player.inventoryManager.getOpenChest()
				

				slot = openChest.searchPlayerInv("minecraft:air")
				if slot is None:
					raise Exception("Inventory full")
				player.swapSlots(slot["id"], result["id"])

				openChest = player.inventoryManager.getOpenChest()

				chestManager.indexOpenChest(*currentChest)		
				dumpChestData()


				time.sleep(0.5)
				break

		player.closeScreen()

		# walk to build area
		lookwalk(blockBase[0], blockBase[2]-1)
		lookwalk(blockBase[0]+rows[len(rows)//2], blockBase[2]-1, required_distance_squared=1)

		# precompute next rows while in render distance
		for i in range(len(rows)*2):hasRowCached(rows[-1]+i+1)

		

		first = True
		for blocks in zip(*(schematic.getRow(row) for row in rows)):
			eatFood()
			while True:
				doBreak = True
				for block in blocks:
					blockPos = block[0][0]+blockBase[0], block[0][1]-1+blockBase[1], block[0][2]+blockBase[2]-1

					if player.getBlock(*blockPos)["id"] != supportingBlock:
						doBreak = False
						getItemToSlot(supportingBlock, hotbar=1)
						time.sleep(0.1)
						player.client.printerPlace(*blockPos,1)
						time.sleep(0.3)
						getItemToSlot(supportingBlock, hotbar=1)
				for i, block in enumerate(blocks):
					blockPos = block[0][0]+blockBase[0], block[0][1]+blockBase[1], block[0][2]+blockBase[2]-1
					hotbar = [slot for slot in player.client.getPlayerInventory() if slot["id"] == block[1] and slot["Slot"] < 8]
					open_hotbar = [slot for slot in player.client.getPlayerInventory() if slot["id"] == "minecraft:air" and slot["Slot"] < 8]
					useSlot = random.randrange(1, 8) if len(open_hotbar) == 0 else open_hotbar[0]["Slot"]

					if player.getBlock(*blockPos)["id"] != block[1]:
						

						doBreak = False
						if len(hotbar) == 0:
							getItemToSlot(block[1], hotbar=useSlot+1)
							time.sleep(0.2)
							player.client.printerPlace(*blockPos,useSlot+1)
						else:

							time.sleep(0.1)
							player.client.printerPlace(*blockPos,hotbar[0]["Slot"]+1)
						time.sleep(0.1)
						
				if doBreak:
					break

			# Walk one block
			player.rotate(50, 0)
			if not first:
				beforeZ = math.floor(player.lastZ)
				oldPing = player.client.pingTime
				player.client.pingTime = 0.04
				try:
					player.keyDown(InputKeys.FORWARD)
					while abs(player.lastZ-beforeZ) < 0.9:
						time.sleep(0.05)
				finally:
					player.keyUp(InputKeys.FORWARD)
					player.client.pingTime = oldPing
			first = False
		
		lookwalk(blockBase[0]+rows[len(rows)//2], blockBase[2]-1)
		lookwalk(blockBase[0]-1, blockBase[2]-1)
		

			

			



def fixSneak(): player.clearKeys()





def dumpChestData():
	out = {}
	for chestPos, chest in chestManager.chests.items():
		out[json.dumps(chestPos)] = chest.serialize()
	f = open("chests.json", "w")
	f.write(json.dumps(out))
	f.close()

chestManager = chestmanager.ChestManager(player)

if __name__ == "__main__":
	fixSneak()
	if sys.argv[-1] == "unsneak":
		fixSneak()
	elif sys.argv[-1] == "outline":
		outline()
	elif sys.argv[-1] == "index":
		lookwalk(chestStandLoc[0], chestStandLoc[2])
		for chest in chests:
			chestManager.openAndIndex(*chest)		
		dumpChestData()



	elif sys.argv[-1] == "build":
		if os.path.exists("chests.json"):
			for k, v in json.load(open("chests.json", "r")).items():
				# print(,v["requiredType"], v)

				chestManager.chests[tuple(json.loads(k))] = {
						"chest-1": Chest1Inventory, "chest-2":Chest2Inventory, "chest-3": Chest3Inventory, "chest-4": Chest4Inventory, "chest-5": Chest5Inventory, "chest-6": Chest6Inventory
					}[v["container type"]](player.client, v)

			workingOn = []
			for row in range(128):
				if not hasRowCached(row):
					workingOn.append(row)
				if len(workingOn) == build_segment_size:
					makeRowBatch(workingOn)
					workingOn.clear()
					eatFood()


				
			makeRowBatch(workingOn)

	

# print(hasRowCached(0))






# player.hackerPlace(*blockBase, 1)





# print(schematic)

# # indexChests()

player.kill()