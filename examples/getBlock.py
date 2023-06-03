from mcbotit import Player
import time


PORT = 25721
player = Player(PORT)

time.sleep(0.1)

bx, by, bz = int(player.lastX), int(player.lastY)-1, int(player.lastZ)

with player.client:
	with player.client:
		for dx in range(-5, 5):
			for dz in range(-5, 5):
				print(player.getBlock(bx+dx, by, bz+dz))



player.kill()