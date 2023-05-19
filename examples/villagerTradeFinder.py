from mcbotit import Player
import threading, time



# Enchantment info
# Id: aqua_affinity          Max level: I
# Id: bane_of_arthropods     Max level: V
# Id: blast_protection       Max level: IV
# Id: channeling             Max level: I
# Id: binding_curse          Max level: I
# Id: vanishing_curse        Max level: I
# Id: depth_strider          Max level: III
# Id: efficiency             Max level: V
# Id: feather_falling        Max level: IV
# Id: fire_aspect            Max level: II
# Id: fire_protection        Max level: IV
# Id: flame                  Max level: I
# Id: fortune                Max level: III
# Id: frost_walker           Max level: II
# Id: impaling               Max level: V
# Id: infinity               Max level: I
# Id: knockback              Max level: II
# Id: looting                Max level: III
# Id: loyalty                Max level: III
# Id: luck_of_the_sea        Max level: III
# Id: lure                   Max level: III
# Id: mending                Max level: I
# Id: multishot              Max level: I
# Id: piercing               Max level: IV
# Id: power                  Max level: V
# Id: projectile_protection  Max level: IV
# Id: protection             Max level: IV
# Id: punch                  Max level: II
# Id: quick_charge           Max level: III
# Id: respiration            Max level: III
# Id: riptide                Max level: III
# Id: sharpness              Max level: V
# Id: silk_touch             Max level: I
# Id: smite                  Max level: V
# Id: soul_speed             Max level: III
# Id: sweeping               Max level: III
# Id: swift_sneak            Max level: III
# Id: thorns                 Max level: III
# Id: unbreaking             Max level: III


PORT = 20027
player = Player(PORT)

workStation = (-39, 59, -23) # Replace this with the block location of the work station

villager = (-39, 60, -24) # Replace this with the block location of the villager

enchantments = [
    ["unbreaking", 3], # Enchantment id, min level to keep
    ["silk_touch", 1],
    ["protection", 4],
    ["sharpness", 5],
    ["depth_strider", 3],
    ["power", 5],
    ["mending", 1],
    ["fire_aspect", 2],
    ["fortune", 3],
    ["efficiency", 5],
    ["frost_walker", 2]

]



thread = None
running = True


def run():
	global running
	while running:

		time.sleep(0.1)
		player.lookTowardBlock(*villager)
		time.sleep(1)
		
		while running:
			try:
				player.openEntity()
				time.sleep(1)
				villagerInv = player.inventoryManager.getOpenVillagerInventory()
				trades = villagerInv.getTrades()

				break
			except AssertionError: time.sleep(2)
		for trade in trades:
			eprice = trade["buy"]["Count"] 
			if trade["sell"]["id"] == "minecraft:enchanted_book":
				ench = trade["sell"]["tag"]["StoredEnchantments"][0]["id"].replace("minecraft:", "")
				lvl = trade["sell"]["tag"]["StoredEnchantments"][0]["lvl"]
				print("Got", ench, "with level", lvl)
				for eName, eLevel in enchantments:
					if eName == ench:
						if eLevel <= lvl:
							player.print("§6Found potential trade")
							return
		player.closeScreen()
		
		player.mine(*workStation)
		time.sleep(0.7)
		player.place(*workStation, 3)
		time.sleep(0.3)


def startHook(player, command):
	global thread
	global running
	if thread is not None:
		if thread.is_alive():
			player.print("Already running")
			return
	thread = threading.Thread(target=run)
	thread.start()
	running=True
def stopHook(player, command):
	print("stop")
	global running
	running=False




player.registerCommandHook("start", "starts trading", startHook)
player.registerCommandHook("stop", "stops trading", stopHook)
