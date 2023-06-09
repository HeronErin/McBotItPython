import json
from typing import Generator
from .client import Client, STATUS_EFFECT




class BaseInventory:
	requiredType : str
	playerInvEnd : int
	maxRows : int
	maxCols : int

	items : list[dict]
	client : Client

	def __init__(self, client: Client, nbt: dict):
		assert nbt.get("container type") == self.requiredType
		self.client = client
		self.items = nbt["items"]
		self.init()
	def getId(self, id : int):
		""" From a slot id, get an itemstack"""
		x = [s for s in self.items if s["id"] == id]
		return x[0]
	def init(self):
		""" Do not call me """
		pass
	def getSlotIdByRowCol(self, row : int, col : int) -> int:
		""" Use math to get the slot id by the row and col"""

		assert row < self.maxRows
		assert col < self.maxCols
		return self.playerInvEnd-(row+1)*self.maxCols+1+col
	def getSlot(self, row : int, col : int) -> dict:
		""" Got an itemstack from by a row and col"""

		return self.getId(self.getSlotIdByRowCol(row, col))
	def serialize(self) -> dict:
		out = self.__dict__.copy()
		del out["client"]
		out["container type"] = self.requiredType
		return out
	def search(self, id:str) -> Generator[dict, None, None]:
		""" Search for an item stack in a chest or non player inventory, YEILD the results"""
		for row in range(3, self.maxRows):
			for col in range(0, self.maxCols):
				if (item:=self.getSlot(row, col))["type"] == id:
					yield item
	def searchPlayerInv(self, id:str) -> dict:
		""" Search specificly the players inventory and RETURN the result"""
		for row in range(0, 4):
			for col in range(0, 9):
				slot = self.getSlot( row, col)
				if slot["type"] == id:
					return slot

class PlayerInventory(BaseInventory):
	requiredType="other"
	playerInvEnd = 44
	maxRows = 4
	maxCols = 9

	helmet : dict
	chestplate : dict
	leggings : dict
	boots : dict
	offhand : dict
	craftingSlot1 : dict
	craftingSlot2 : dict
	craftingSlot3 : dict
	craftingSlot4 : dict
	craftingOutput : dict

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
	playerInvEnd=89

class CraftingInventory(BaseInventory):
	requiredType="crafting table"
	maxRows=4
	maxCols = 9
	playerInvEnd = 45

	output : dict
	craftingSlot1 : dict
	craftingSlot2 : dict
	craftingSlot3 : dict
	craftingSlot4 : dict
	craftingSlot5 : dict
	craftingSlot6 : dict
	craftingSlot7 : dict
	craftingSlot8 : dict
	craftingSlot9 : dict
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

	output : dict
	fuelSlot : dict
	inputSlot : dict

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

	slot1 : dict
	slot2 : dict
	slot3 : dict
	slot4 : dict
	slot5 : dict
	slot6 : dict
	slot7 : dict
	slot8 : dict
	slot9 : dict
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

	inputSlot : dict
	lapisSlot : dict
	def init(self):
		self.inputSlot = self.getId(0)
		self.lapisSlot = self.getId(1)
	def pickEnchantment(self, i: int):
		""" Select an enchantment based on the index of the enchantment """

		self.client.clickInventoryButton(i)
	def getEnchants(self)->list[dict]:
		return self.client.getEnchants()
class BrewingStand(BaseInventory):
	playerInvEnd=40
	maxRows=4
	maxCols=9
	requiredType="brewing stand"

	blazeSlot : dict
	ingredientSlot : dict
	potion1 : dict
	potion2 : dict
	potion3 : dict
	def init(self):
		self.blazeSlot = self.getId(4)
		self.ingredientSlot = self.getId(3)
		self.potion1 =self.getId(0)
		self.potion2 =self.getId(1)
		self.potion3 =self.getId(2)

class Base3WayIO(BaseInventory):
	requiredType=""
	playerInvEnd=38
	maxRows=4
	maxCols=9
	input1 : dict
	input2 : dict
	output : dict
	def init(self):
		self.input1 = self.getId(0)
		self.input2 = self.getId(1)
		self.output = self.getId(2)
class Anvil(Base3WayIO):
	requiredType="anvil"

	def getInfo(self)->dict:
		return self.client.getAnvilInfo()
	def setName(self, text:str):
		self.client.setAnvilName(text)

class VillagerInventory(Base3WayIO):
	requiredType = "villager"
	def setTradeIndex(self, i):
		""" Select the villagers strade bassed on index """
		self.client.setVillagerTrade(i)
	def getTrades(self) -> dict:
		"""Gets the trades of the opened villager"""

		return self.client.getVillagerTrades()
class Beacon(BaseInventory):
	requiredType = "beacon"
	playerInvEnd=36
	maxRows=4
	maxCols=9
	input : dict
	def init(self):
		self.input = self.getId(0)

	def setPrimaryEffect(self, effect:STATUS_EFFECT):
		self.client.setBeaconEffect(True, effect)
	def setSecoundaryEffect(self, effect:STATUS_EFFECT):
		self.client.setBeaconEffect(False, effect)
	def doneButton(self):
		self.client.pressDoneButtonInBeacon()
class Hopper(BaseInventory):
	requiredType = "hopper"
	playerInvEnd=40
	maxRows=4
	maxCols=9

	slot1 : dict
	slot2 : dict
	slot3 : dict
	slot4 : dict
	slot5 : dict
	def init(self):
		self.slot1 =self.getId(0)
		self.slot2 =self.getId(1)
		self.slot3 =self.getId(2)
		self.slot4 =self.getId(3)
		self.slot5 =self.getId(4) 
class CartographyTable(Base3WayIO):
	requiredType="cartography Table"
class Grindstone(Base3WayIO):
	requiredType="grindstone"

# CHANGES IN 1.20
class SmithingTable(Base3WayIO):
	requiredType="smithing table"


class InventoryManager:
	""" Used for getting the current open inventory """
	def __init__(self, client):
		self.client = client
	def getOpenPlayerInventory(self) -> PlayerInventory:	
		return PlayerInventory(self.client, self.client.getOpenInventory())
	def getOpenChest(self) -> Chest1Inventory | Chest2Inventory | Chest3Inventory | Chest4Inventory | Chest5Inventory | Chest6Inventory:
		nbt = self.client.getOpenInventory()
		assert nbt.get("container type").startswith("chest-")
		return {
			"chest-1": Chest1Inventory, "chest-2":Chest2Inventory, "chest-3": Chest3Inventory, "chest-4": Chest4Inventory, "chest-5": Chest5Inventory, "chest-6": Chest6Inventory
		}[nbt.get("container type")](self.client, nbt)
	def getOpenShulker(self) -> ShulkerInventory:
		return ShulkerInventory(self.client, self.client.getOpenInventory())
	def getOpenCraftingTable(self) -> CraftingInventory:
		return CraftingInventory(self.client, self.client.getOpenInventory())
	def getOpenFurnace(self) -> FurnaceInventory:
		return FurnaceInventory(self.client, self.client.getOpenInventory())
	def getOpenBlastFurnace(self) -> BlastFurnace:
		return BlastFurnace(self.client, self.client.getOpenInventory())
	def getOpenSmoker(self) -> Smoker:
		return Smoker(self.client, self.client.getOpenInventory())
	def getOpen3by3(self) -> X3Inventory:
		return X3Inventory(self.client, self.client.getOpenInventory())
	def getOpenEnchantmentTable(self) -> EnchantmentTable: 
		return EnchantmentTable(self.client, self.client.getOpenInventory())
	def getOpenBrewingStand(self) -> BrewingStand:
		return BrewingStand(self.client, self.client.getOpenInventory())
	def getOpenAnvil(self) -> Anvil:
		return Anvil(self.client, self.client.getOpenInventory())
	def getOpenVillagerInventory(self) -> VillagerInventory:
		return VillagerInventory(self.client, self.client.getOpenInventory())
	def getOpenBeacon(self) -> Beacon:
		return Beacon(self.client, self.client.getOpenInventory())
	def getOpenHopper(self) -> Hopper:
		return Hopper(self.client, self.client.getOpenInventory())
	def getOpenCartographyTable(self) -> CartographyTable:
		return CartographyTable(self.client, self.client.getOpenInventory())
	def getOpenGrindstone(self) -> Grindstone:
		return Grindstone(self.client, self.client.getOpenInventory())
	def getOpenSmithingTable(self) -> SmithingTable:
		return SmithingTable(self.client, self.client.getOpenInventory())