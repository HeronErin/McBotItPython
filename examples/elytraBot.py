from mcbotit import Player, InputKeys
import time, threading
PORT = int(input("Port: "))
player = Player(PORT)
# player.setHotbarSlot(1)
# player.holdFor(InputKeys.RIGHT_CLICK, 0.05, wait=False)
thread = None
running = True


MINY = 200
TARGETY = 300



MASTER_ROT = None


def achiveAltitude():
	player.rotate(-50, MASTER_ROT["yaw"], speed=0.3)
	while True:
		if player.lastVelocity[1] > 0.05:
			time.sleep(0.1)
		else:
			if player.lastY > TARGETY:
				break
			player.useItem()
			time.sleep(0.2)
	player.rotate(30, MASTER_ROT["yaw"], speed=0.3, wait=False)
		

def run(x, z):
	global MASTER_ROT
	with player.client:
		player.client.send({"cmd":"get rotation to get to block", "x":x, "y":int(player.lastY), "z":z})
		MASTER_ROT = player.client.recv(1024)[0]

		chestplate = player.inventoryManager.getOpenPlayerInventory().chestplate
		if chestplate["type"] != "minecraft:elytra":
			player.print("Please equip an elytra")
			return
		if chestplate["durability"] <= 10:
			player.print("Elytra durability too low")
			return
		while not player.getPlayerInfo()["isElytraFlying"]:
			player.rotate(-50, MASTER_ROT["yaw"], speed=0.3)
			player.jump()
			time.sleep(0.1)
			player.client.enableElytra()
			time.sleep(0.05)
			player.useItem()
		
	achiveAltitude()
	goingDown = True
	goingUp = False

	while ((player.lastX-x)**2 + (player.lastZ-z)**2) > 100: # Within 10 blocks
		if goingDown and player.lastY < MINY: 
			goingDown = False
			goingUp=True

			player.rotate(-40, MASTER_ROT["yaw"], speed=0.3, wait=False)
			time.sleep(2)
			with player.client:
				player.client.send({"cmd":"get rotation to get to block", "x":x, "y":int(player.lastY), "z":z})
				MASTER_ROT = player.client.recv(1024)[0]

		elif goingUp and player.isFalling:
			if player.lastY > MINY+40:
				player.rotate(30, MASTER_ROT["yaw"], speed=0.3, wait=False)
				time.sleep(2)
				with player.client:
					player.client.send({"cmd":"get rotation to get to block", "x":x, "y":int(player.lastY), "z":z})
					MASTER_ROT = player.client.recv(1024)[0]
			else:
				achiveAltitude()
				time.sleep(2)
			goingDown = True
			goingUp = False
		else:
			time.sleep(0.5)
	player.print("finished")
def gotoCommand(player, command):
	global thread
	global running
	if thread is not None:
		if thread.is_alive():
			player.print("Already running")
			return
	cSegs = command.strip().split(" ")
	if len(cSegs) == 3:
		running=True
		thread = threading.Thread(target=run, args=[int(coord) for coord in cSegs[1:]])
		thread.start()
	else:
		player.print("Syntax error")
def stopHook(player, command):
	global running
	running=False

player.registerCommandHook("goto", "x, y    fly to a location", gotoCommand, spinIntoThread=False)
player.registerCommandHook("stop", "stop flying", stopHook, spinIntoThread=False)
# gotoCommand(player, "")
# player.kill()