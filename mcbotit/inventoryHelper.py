class InventoryManager:
	def __init__(self, client):
		self.client = client
	def getOpenPlayerInventory(self):	
		return PlayerInventory(self.client, self.client.getOpenInventory())
	def getOpenChest(self):
		nbt = self.client.getOpenInventory()
		assert nbt.get("container type").startswith("chest-")
		return {
			"chest-1": Chest1Inventory, "chest-2":Chest2Inventory, "chest-3": Chest3Inventory, "chest-4": Chest4Inventory, "chest-5": Chest5Inventory, "chest-6": Chest6Inventory
		}[nbt.get("container type")](self.client, nbt)
	def getOpenShulker(self):
		return ShulkerInventory(self.client, self.client.getOpenInventory())
	def getOpenCraftingTable(self):
		return CraftingInventory(self.client, self.client.getOpenInventory())
	def getOpenFurnace(self):
		return FurnaceInventory(self.client, self.client.getOpenInventory())
	def getOpenBlastFurnace(self):
		return BlastFurnace(self.client, self.client.getOpenInventory())
	def getOpenSmoker(self):
		return Smoker(self.client, self.client.getOpenInventory())
	def getOpen3by3(self):
		return X3Inventory(self.client, self.client.getOpenInventory())
	def getOpenEnchantmentTable(self): 
		return EnchantmentTable(self.client, self.client.getOpenInventory())
	def getOpenBrewingStand(self):
		return BrewingStand(self.client, self.client.getOpenInventory())
	def getOpenAnvil(self):
		return Anvil(self.client, self.client.getOpenInventory())
	def getOpenVillagerInventory(self):
		return VillagerInventory(self.client, self.client.getOpenInventory())
	def getOpenBeacon(self):
		return Beacon(self.client, self.client.getOpenInventory())
	def getOpenHopper(self):
		return Hopper(self.client, self.client.getOpenInventory())
	def getOpenCartographyTable(self):
		return CartographyTable(self.client, self.client.getOpenInventory())
	def getOpenGrindstone(self):
		return Grindstone(self.client, self.client.getOpenInventory())
	def getOpenSmithingTable(self):
		return SmithingTable(self.client, self.client.getOpenInventory())
class BaseInventory:
	requiredType : str
	playerInvEnd : int
	maxRows : int
	maxCols : int
	def __init__(self, client, nbt):
		assert nbt.get("container type") == self.requiredType
		self.client = client
		self.items = nbt["items"]
		self.init()
	def getId(self, id):
		x = [s for s in self.items if s["id"] == id]
		return x[0]
	def init(self):
		pass# Overide me
	def getSlotIdByRowCol(self, row, col):
		assert row < self.maxRows
		assert col < self.maxCols
		return self.playerInvEnd-(row+1)*self.maxCols+1+col
	def getSlot(self, row, col):
		return self.getId(self.getSlotIdByRowCol(row, col))
class PlayerInventory(BaseInventory):
	requiredType="other"
	playerInvEnd = 44
	maxRows = 4
	maxCols = 9
	def init(self):
		self.helmet = self.getId(5)
		self.chestplate = self.getId(6)
		self.leggings = self.getId(7)
		self.boots = self.getId(8)

		self.offhand = self.getId(45)

		self.craftingSlot1 = self.getId(1)
		self.craftingSlot2 = self.getId(2)
		self.craftingSlot3 = self.getId(3)
		self.craftingSlot4 = self.getId(4)
		self.craftingOutput = self.getId(0)
class Chest1Inventory(BaseInventory):
	requiredType="chest-1"
	maxRows = 5
	maxCols = 9
	playerInvEnd=44
class Chest2Inventory(BaseInventory):
	requiredType="chest-2"
	maxRows = 6
	maxCols = 9
	playerInvEnd=53
class Chest3Inventory(BaseInventory):
	requiredType="chest-3"
	maxRows = 7
	maxCols = 9
	playerInvEnd=62
class ShulkerInventory(Chest3Inventory):
	requiredType="shulker"
class Chest4Inventory(BaseInventory):
	requiredType="chest-4"
	maxRows = 8
	maxCols = 9
	playerInvEnd=71
class Chest5Inventory(BaseInventory):
	requiredType="chest-5"
	maxRows = 9
	maxCols = 9
	playerInvEnd=80
class Chest6Inventory(BaseInventory):
	requiredType="chest-6"
	maxRows = 10
	maxCols = 9
	playerInvEnd=80

class CraftingInventory(BaseInventory):
	requiredType="crafting table"
	maxRows=4
	maxCols = 9
	playerInvEnd = 45
	def init(self):
		self.output = self.getId(0)
		self.craftingSlot1 = self.getId(1)
		self.craftingSlot2 = self.getId(2)
		self.craftingSlot3 = self.getId(3)
		self.craftingSlot4 = self.getId(4)
		self.craftingSlot5 = self.getId(5)
		self.craftingSlot6 = self.getId(6)
		self.craftingSlot7 = self.getId(7)
		self.craftingSlot8 = self.getId(8)
		self.craftingSlot9 = self.getId(9)
class FurnaceInventory(BaseInventory):
	requiredType="furnace"
	maxRows=4
	maxCols = 9
	playerInvEnd=38
	def init(self):
		self.output = self.getId(2)
		self.fuelSlot = self.get(1)
		self.inputSlot = self.getId(0)
class BlastFurnace(FurnaceInventory):
	requiredType="blast furnace"
class Smoker(FurnaceInventory):
	requiredType="smoker table"

class X3Inventory(BaseInventory):
	maxRows=4
	maxCols=9
	playerInvEnd=44
	requiredType="3x3"
	def init(self):
		self.slot1 = self.getId(0)
		self.slot2 = self.getId(1)
		self.slot3 = self.getId(2)
		self.slot4 = self.getId(3)
		self.slot5 = self.getId(4)
		self.slot6 = self.getId(5)
		self.slot7 = self.getId(6)
		self.slot8 = self.getId(7)
		self.slot9 = self.getId(8)
class EnchantmentTable(BaseInventory):
	maxRows=4
	maxCols=9
	playerInvEnd=37
	requiredType="enchantment table"
	def init(self):
		self.inputSlot = self.getId(0)
		self.lapisSlot = self.getId(1)
	def pickEnchantment(self, i):
		self.client.clickInventoryButton(i)
class BrewingStand(BaseInventory):
	playerInvEnd=40
	maxRows=4
	maxCols=9
	requiredType="brewing stand"
	def init(self):
		self.blazeSlot = self.getId(4)
		self.ingredientSlot = self.getId(3)
		self.potion1 =self.getId(0)
		self.potion2 =self.getId(1)
		self.potion3 =self.getId(2)
class Anvil(BaseInventory):
	requiredType="anvil"
	playerInvEnd=38
	maxRows=4
	maxCols=9
	def init(self):
		self.input1 = self.getId(0)
		self.input2 = self.getId(1)
		self.output = self.getId(2)
class VillagerInventory(Anvil):
	requiredType = "villager"
	def setTradeIndex(self, i):
		self.client.setVillagerTrade(i)
	def getTrades(self):
		return self.client.getVillagerTrades()
class Beacon(BaseInventory):
	requiredType = "beacon"
	playerInvEnd=36
	maxRows=4
	maxCols=9
	def init(self):
		self.input = self.getId(0)
class Hopper(BaseInventory):
	requiredType = "hopper"
	playerInvEnd=40
	maxRows=4
	maxCols=9
	def init(self):
		self.slot1 =self.getId(0)
		self.slot2 =self.getId(1)
		self.slot3 =self.getId(2)
		self.slot4 =self.getId(3)
		self.slot5 =self.getId(4) 
class CartographyTable(Anvil):
	requiredType="cartography Table"
class Grindstone(Anvil):
	requiredType="grindstone"

# CHANGES IN 1.20
class SmithingTable(Anvil):
	requiredType="smithing table"