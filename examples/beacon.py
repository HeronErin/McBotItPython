from mcbotit import Player, STATUS_EFFECT

PORT = int(input("Port: "))
player = Player(PORT)

beacon = player.inventoryManager.getOpenBeacon()
beacon.setPrimaryEffect(STATUS_EFFECT.HASTE)
beacon.doneButton()

player.kill()