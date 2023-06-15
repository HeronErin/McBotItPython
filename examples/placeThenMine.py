from mcbotit import Player, InputKeys
import time, math
PORT = 10597
player = Player(PORT)

# time.sleep(1)



try:
	while True:
		player.holdFor(InputKeys.RIGHT_CLICK, 0.1)
		player.holdFor(InputKeys.LEFT_CLICK, 0.5)
finally:


	player.kill()
