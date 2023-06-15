from mcbotit import Player
import time
PORT = 22436
player = Player(PORT)
time.sleep(0.1)

player.rotate(player.lastPitch, int(input("Yaw: ")))

player.kill()
