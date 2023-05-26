from mcbotit import Player, InputKeys
import time, math
PORT = 14795
player = Player(PORT)
time.sleep(0.2)
player.keyDown(InputKeys.FORWARD)
time.sleep(0.4)
player.keyUp(InputKeys.FORWARD)

	


player.kill()