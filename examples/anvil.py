from mcbotit import Player

PORT = 7949
player = Player(PORT)

anvil = player.inventoryManager.getOpenAnvil()
print(anvil.getInfo())
anvil.setName("test")

player.kill()