from mcbotit import Player, InputKeys
import time, math
PORT = 11149
player = Player(PORT)
time.sleep(0.2)
base = (14922, 63, 3073)
for i in range(32):
	player.client.printerPlace(base[0], base[1], base[2]+i, 1)
	time.sleep(0.7)
	player.client.printerPlace(base[0]+1, base[1], base[2]+i, 1)
	time.sleep(0.7)
	player.client.printerPlace(base[0]+2, base[1], base[2]+i, 1)
	time.sleep(0.7)
	player.rotate(50, 0)

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

	


player.kill()