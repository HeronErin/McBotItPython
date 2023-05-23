from functools import partial

import nbtlib # Faster then the normal nbt library


class MapSchematic:
	def __init__(self, path):
		file =  nbtlib.load(path, gzipped=True)
		self.blocks ={}
		self.palette = [str(p["Name"]) for p in file["palette"]]
		self.size = [int(i) for i in file["size"]]
		self.size[1]-=1

		for v in list(file["blocks"]):
			pos = [int(i) for i in v["pos"]]
			pos[1]-=1
			self.blocks[tuple(pos)] = self.palette[int(v["state"])]
			
	def __getitem__(self, v):
		if len(v) == 3:
			try: return self.blocks[v]
			except KeyError:
				return "minecraft:air"
		else:
			raise ValueError("Must contain 3 inputs")
	def getRow(self, row):
		def tmp(rw, t):

			return t[0][0] == rw and t[0][1] == 1 and t[-1] != "minecraft:cobblestone"
		return filter(partial(tmp, row),self.blocks.items())
	def getRowRange(self, rows):
		rows = list(rows)
		def tmp(rws, t):
			return t[0][0] in rws and t[0][1] == 1
		return filter(partial(tmp, rows),self.blocks.items())
	def getRowCosts(self, row):
		
		blocks = self.getRow(row)
		stuff = {}
		for b in blocks:
			if b[-1] != "minecraft:cobblestone":
				a = stuff.get(b[-1], 0)
				a+=1
				stuff[b[-1]]=a

		return stuff