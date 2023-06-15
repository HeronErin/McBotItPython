from mcbotit import Player, InputKeys
import time
PORT = 22436
player = Player(PORT)
time.sleep(0.1)

player.rotate(player.lastPitch, -90)
player.keyDown(InputKeys.FORWARD)
try:
    while True:
        time.sleep(7)
        player.keyUp(InputKeys.FORWARD)
        time.sleep(1)
        player.keyDown(InputKeys.FORWARD)
finally:

    player.keyUp(InputKeys.FORWARD)

    player.kill()
