from mcbotit import Player

PORT = int(input("Port: "))
player = Player(PORT)

table  = player.inventoryManager.getOpenEnchantmentTable()
print(table.getEnchants())
table.pickEnchantment(0)

player.kill()