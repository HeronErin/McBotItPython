from mcbotit import Player

PORT = int(input("Port: "))
player = Player(PORT)

def testCommand(player, command):
	# This is used as an example NEVER use eval in your code EVER
	player.print(str(eval(command[len("eval")+1:])))
player.registerCommandHook("eval", "preforms a python calculation", testCommand)