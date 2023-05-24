from mcbotit import Player

PORT = int(input("Port: "))
player = Player(PORT)

player.print("Hello world")

player.kill()