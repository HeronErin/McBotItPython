from mcbotit import Player, chestmanager, MapSchematic, InputKeys
from functools import lru_cache
import time, math, sys, json, os, random

from mcbotit import Chest1Inventory, Chest2Inventory, Chest3Inventory, Chest4Inventory, Chest5Inventory, Chest6Inventory

#

PORT = 15198
player = Player(PORT, keepAliveTime=0.05)

blockBase = (14400, 78, 3392)
chestStandLoc = ( 14398.6, 78, 3387.8)

build_segment_size = 4
chests = (
	(14400, 80, 3386),
	(14400, 79, 3386),
	(14400, 80, 3389),
	(14400, 79, 3389),


	(14396, 79, 3386),
	(14396, 80, 3389),
	(14396, 79, 3389),

	(14399, 78, 3389),
	(14398, 78, 3389),
	(14397, 78, 3389),

	(14399, 78, 3386),
	(14398, 78, 3386),
	(14397, 78, 3386),

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


def autoMerge():
	playerinv = player.inventoryManager.getOpenPlayerInventory()

	for row in range(0, 4):
		for col in range(0, 9):
			slot=playerinv.getSlot(row, col)
			if slot["type"] == "minecraft:air": continue
			for row2 in range(0, 4):
				for col2 in range(0, 9):
					if col == col2 and row == row2: continue
					slot2=playerinv.getSlot(row2, col2)
					if slot2["type"] == slot["type"] and slot["count"] + slot2["count"] <= 64:
						player.swapSlots(slot["id"], slot2["id"])

						return autoMerge()


def getItemToSlot(idd, hotbar = 1):
	playerinv = player.inventoryManager.getOpenPlayerInventory()
	base = playerinv.getSlot(0, hotbar-1)
	if base["type"] != idd:

		for row in range(0, 4):
			for col in range(0, 9):
				if (slot:=playerinv.getSlot(row, col))["type"] == idd:
					player.swapSlots(slot["id"], base["id"]     )
					# print(slot, "a")
					return
def eatFood():
	while player.lastHunger != 20:
		player.setHotbarSlot(9)
		player.useItem()
		time.sleep(2)
def repairStep():
	t = time.time()
	with player.client:
		for block in schematic.blocks.items():
			# print(block)
			blockPos = block[0][0]+blockBase[0], block[0][1]+blockBase[1], block[0][2]+blockBase[2]-1
			
			if math.sqrt((blockPos[0]-player.lastX)**2 + (blockPos[1]-player.lastY)**2 + (blockPos[2]-player.lastZ)**2) <= 4.5:
				requiredType = block[1] if block[0][1] == 1 else supportingBlock

				if requiredType == "minecraft:cobblestone": continue

				t2 = time.time()
				realBlock = player.getBlock(*blockPos)
				if requiredType != realBlock["id"]:
					
					if realBlock["id"] != "minecraft:air":
						player.mine(*blockPos)
					getItemToSlot(requiredType, hotbar=2)
					time.sleep(0.1)
					player.client.printerPlace(*blockPos,2)
	print(time.time()-t)

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
	vt = time.time()
	if rows:
		autoMerge()
		lookwalk(blockBase[0]-1, blockBase[2]-1, required_distance_squared=4)
		lookwalk(chestStandLoc[0], chestStandLoc[2], required_distance_squared=2)


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

				re = chestManager.search(id)
				if re is None: raise Exception(f"Missing "+id)
				result, currentChest = re
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
			with player.client:
				while True:
					doBreak = True

					for block in blocks:
						blockPos = block[0][0]+blockBase[0], block[0][1]-1+blockBase[1], block[0][2]+blockBase[2]-1

						if player.getBlock(*blockPos)["id"] == "minecraft:air":
							doBreak = False
							getItemToSlot(supportingBlock, hotbar=1)
							time.sleep(0.1)
							player.client.printerPlace(*blockPos,1)
							time.sleep(0.07)
							# getItemToSlot(supportingBlock, hotbar=1)
					for i, block in enumerate(blocks):
						blockPos = block[0][0]+blockBase[0], block[0][1]+blockBase[1], block[0][2]+blockBase[2]-1
						hotbar = [slot for slot in player.client.getPlayerInventory() if slot["id"] == block[1] and slot["Slot"] < 8]
						open_hotbar = [slot for slot in player.client.getPlayerInventory() if slot["id"] == "minecraft:air" and slot["Slot"] < 8]
						useSlot = random.randrange(1, 8) if len(open_hotbar) == 0 else open_hotbar[0]["Slot"]

						if player.getBlock(*blockPos)["id"] =="minecraft:air":
							

							doBreak = False
							if len(hotbar) == 0:
								getItemToSlot(block[1], hotbar=useSlot+1)
								time.sleep(0.255)
								player.client.printerPlace(*blockPos,useSlot+1)
							else:

								time.sleep(0.065)
								player.client.printerPlace(*blockPos,hotbar[0]["Slot"]+1)
							time.sleep(0.09)
							
					time.sleep(0.15)
					if doBreak:
						break
			if not first:
				# Walk one block
				player.rotate(50, 0, speed = 0.1)

				
				oldPing = player.client.pingTime
				player.client.pingTime = 0.04

				time.sleep(0.08)
				beforeZ = math.floor(player.lastZ)
				try:
					player.keyDown(InputKeys.FORWARD)
					while abs(player.lastZ-beforeZ) < 0.9:
						time.sleep(0.05)
				finally:
					player.keyUp(InputKeys.FORWARD)
					player.client.pingTime = oldPing
			first = False



		lookwalk(blockBase[0], blockBase[2])

		z = time.time()-vt
		print(f"Finished with row(s), took: {z}s or {z/len(rows)}s per row. Finished with row {rows[-1]}. Estimated time left {(128-rows[-1])/len(rows)*z}")


			

			



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
	elif sys.argv[-1] == "costs":
		costs = {}
		for block in schematic.blocks.items():
			costs[block[-1]] = costs.get(block[-1], 0)+1
		for k, v in costs.items():
			print(k,"items:", v,"stacks:", v/64,"rows", v/64/9,"chests:", v/64/9/3)
	elif sys.argv[-1] == "repair":
		repairStep()
						# print(requiredType, realBlock["id"])	
						

# print(hasRowCached(0))






# player.hackerPlace(*blockBase, 1)





# print(schematic)

# # indexChests()

player.kill()
