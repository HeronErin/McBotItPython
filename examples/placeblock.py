from mcbotit import Player
import time
PORT = int(input("Port: "))
player = Player(PORT)
time.sleep(0.2)
player.client.hackerPlace(int(player.lastX)-2, int(player.lastY), int(player.lastZ), 1)

player.kill()