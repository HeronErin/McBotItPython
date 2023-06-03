from mcbotit import Player, InputKeys
import time, math
PORT = 17214
player = Player(PORT)

# time.sleep(1)


def eatFood():
	while player.lastHunger != 20:
		player.setHotbarSlot(9)
		player.useItem()
		time.sleep(2)
	player.setHotbarSlot(1)


player.keyDown(InputKeys.LEFT_CLICK)
try:
	while True:
		time.sleep(0.1)
		if int(player.lastX) == 15599:
			player.keyUp(InputKeys.LEFT_CLICK)
			time.sleep(0.2)
			eatFood()
			player.keyDown(InputKeys.LEFT_CLICK)
			time.sleep(1)

		playerinv = player.inventoryManager.getOpenPlayerInventory()
		if playerinv.getSlot(0, 0)["durability"] < 100:
			player.keyUp(InputKeys.LEFT_CLICK)

			slot1 = playerinv.getSlot(0, 0)["id"]
			for i in playerinv.items:
				if i["type"] == "minecraft:diamond_pickaxe":
					if i["durability"] > 100:
						player.swapSlots(i["id"], slot1, delay=0.1)
						time.sleep(1)
						break

		player.keyDown(InputKeys.LEFT_CLICK)


finally:
	player.keyUp(InputKeys.LEFT_CLICK)

	player.kill()
