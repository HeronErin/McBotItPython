from mcbotit import Player, InputKeys
import time, math
PORT = 25778
player = Player(PORT)

# time.sleep(1)


player.keyDown(InputKeys.LEFT_CLICK)
try:
	while True:
		time.sleep(1000000000)
finally:
	player.keyUp(InputKeys.LEFT_CLICK)

	player.kill()
