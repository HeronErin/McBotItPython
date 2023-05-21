from mcbotit import Player, InputKeys
import time
PORT = int(input("Port: "))

while True:
	player = Player(PORT)


	player.holdFor(InputKeys.BACKWORD, 0.6)
	player.goto(4872, 161.5, 4584)


	player.holdFor(InputKeys.RIGHT, 1, wait=False)
	time.sleep(5)
	player.holdFor(InputKeys.LEFT,1)
	time.sleep(5)
	player.holdFor(InputKeys.BACKWORD,2)

	player.goto(4872, 161.5, 4587)

	player.holdFor(InputKeys.FORWARD,0.3)

	time.sleep(17)
	print("hitting")
	lenn = 34
	start = time.time()
	while time.time()-start < lenn:
		player.hitEntity()
		time.sleep(1.2)
	print("end hitting")

	player.kill()
