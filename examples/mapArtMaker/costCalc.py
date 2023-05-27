import sys, os
from mcbotit import MapSchematic



if sys.argv[-1] == "single":
	schematic = MapSchematic("mapart.nbt")
	costs = {}
	for block in schematic.blocks.items():
		costs[block[-1]] = costs.get(block[-1], 0)+1
	for k, v in costs.items():
		print(k,"items:", v,"stacks:", v/64,"rows", v/64/9,"chests:", v/64/9/3)
elif sys.argv[-1] == "multi":
	cmax = {}
	for f in os.listdir("todo"):
		schematic = MapSchematic(os.path.join("todo", f))
		costs = {}
		for block in schematic.blocks.items():
			costs[block[-1]] = costs.get(block[-1], 0)+1
		for k, v in costs.items():
			cmax[k] = max(cmax.get(k, 0 ), v)
	for k, v in cmax.items():
		print(k,"items:", v,"stacks:", v/64,"rows", v/64/9,"chests:", v/64/9/3)
