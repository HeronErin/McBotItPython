# McBotIt python library
-----------------

This library allows you to control your minecraft character from python. Allowing you to automate pretty much everything.


### I am not responsible if you get banned from your favorite server! Many servers may feel this is cheating!
Although this tool may make use of baritone, using baritone with the mod is optional, it is an optional dependency. Meaning that most functions of the mod will still work, with the exception of several functions which make use of baritone. 




## Install: 
1. You need to install the [minecraft mod](https://github.com/HeronErin/McBotit/releases) in fabric 1.19.4. 
2. It is recommended that you download the [baritone api fabric mod](https://github.com/cabaletta/baritone/releases/download/v1.9.3/baritone-api-fabric-1.9.3.jar) in order for some functions to work, but this is optional.
3. Since this library is not yet in PyPi, you must install it from github with ```pip install git+https://github.com/HeronErin/McBotItPython.git``` 

## Usage:
Now that everything (should) be installed, you need to join a world/server while the mods are installed, if everything is correct you should see a message in chat about what port to use. This is the number that the python library connects to, it changes often, so it is unwise to hardcode it, however this is a trap I often fall into. 

Run the following hello world from python to test if everything is correct, if you see a chat message in Minecraft, you are ready to go. 
```python
from mcbotit import Player

PORT = int(input("Port: ")) # Gets input from user for the port to connect to
player = Player(PORT) # Creates player instance

player.print("Hello world") # Prints to clients chat

player.kill() # Kills connection thread, otherwise the script would run forever. 
```




## Classes and Methods:

There are a few Classes you need to be aware of:

1. The Player class.
2. The Client class.
3. The InputKeys Enum
4. And the assorted Inventory classes.


You can view the full documentation [here](https://heronerin.github.io/McBotItPython/mcbotit/)



### The Player class
The Player class is the main class you will be dealing with, it is an abstraction over the Client class. This class keeps track of the players position, rotation, velocity, hunger level, and if they are currently falling. It also allows you to register client side commands. And gives you easy access to the inventoryManager.

The following are some fields in the Player class you sould know of:

* lastX - last known X position
* lastY - last known Y position
* lastZ - last known Z position
* lastPitch - last known pitch rotation value
* lastYaw - last known yaw rotation value
* isFalling
* lastVelocity - A tuple of the players velocity
* lastHunger
* lastHealth
* inventoryManager - used for getting inventory data

You can view the player classes documentation [here](https://heronerin.github.io/McBotItPython/mcbotit/player.html#Player)

### The InputKeys Enum
The following are possible values:

* InputKeys.FORWARD
* InputKeys.BACKWORD
* InputKeys.LEFT
* InputKeys.RIGHT
* InputKeys.SNEAK
* InputKeys.LEFT_CLICK
* InputKeys.RIGHT_CLICK

Docs [here](https://heronerin.github.io/McBotItPython/mcbotit/client.html#InputKeys)

### inventoryManager class
All the following return an inventory object:

* getOpenPlayerInventory()
* getOpenChest()
* getOpenShulker()
* getOpenCraftingTable()
* getOpenFurnace()
* getOpenBlastFurnace()
* getOpenSmoker()
* getOpen3by3()
* getOpenEnchantmentTable()
* getOpenBrewingStand()
* getOpenAnvil()
* getOpenVillagerInventory()
* getOpenBeacon()
* getOpenHopper()
* getOpenCartographyTable()
* getOpenGrindstone()
* getOpenSmithingTable()


Docs [here](https://heronerin.github.io/McBotItPython/mcbotit/inventoryHelper.html#InventoryManager)


### Assorted inventory classes
All inventory classes are quite simmular in structor

* getSlot(row, col)
* search(itemId) find item in the chest
* searchPlayerInv(itemId)
* serialize() return json that can be saved to files

Most of the inventory classes also have fields set to important slots. I'm not going to list all of them here, you can see the documentation [here](https://heronerin.github.io/McBotItPython/mcbotit/inventoryHelper.html), but here are a few notable ones. 

* PlayerInventory has helmet, chestplace, leggings, boots, offhand, craftingSlot1, craftingSlot2, craftingSlot3, craftingSlot4, and craftingOutput.
* X3Inventory (getOpen3by3) has self.slot(1-9) for every slot in a dispensor.
* EnchantmentTable has inputSlot and lapisSlot
* Anvil has input1, input2, and output.
* VillagerInventory has input1, input2, and output. Along with a setTradeIndex(i) function for selecting a trade

### The Client class
This can be obtained by ```player.client```   and use of this should be minimized. This class manages the socket connection itself and has some importent features.

1. using ```with player.client: ```   You can take controll of the connection itself, this is used with many of the Player functions. But taking controll can take 0.1 secounds, so you can speed up your code by taking controll of the connection before running a bunch of functions, however this means the the players attributes, like position, will not be updated. 

2. All raw packets can be directly send with this class. Most have functions to call them, but others can be send like this: ``` player.client.send({"cmd": "right click block"})```

Docs [here](https://heronerin.github.io/McBotItPython/mcbotit/client.html#Client)
