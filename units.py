

global nodeRegistry
nodeRegistry = list()
global streamRegistry
streamRegistry = list()
global unitRegistry
unitRegistry = {
	"node" : nodeRegistry,
	"stream" : streamRegistry
	}
###############################################################################################################################################################
###############################################################################################################################################################
class unit():
	def __init__(self,name):
		self.name = name

	def delete(self):
		if self in unitRegistry["node"]:
			unitRegistry["node"].remove(self)
		elif self in unitRegistry["stream"]:
			unitRegistry["stream"].remove(self)
		else:
			print("I couldn't find this shit anywhere dawg")
		del self #kill yourslef :^)

	def get_all_downstream_units(self,downstreamUnitList = ["init"]):
		allDownstreamUnits = list()
		allDownstreamUnits = self.get_downstream_units(downstreamUnitList)
		return allDownstreamUnits

	def get_downstream_units(self,downstreamUnitList):
		if len(downstreamUnitList) == 0 or downstreamUnitList[0] == "init":
			#downstreamUnitList[0] = self
			downstreamUnitList = []
		else:
			pass

		index = len(downstreamUnitList)

		if self.typeOfUnit == "node":
			if len(self.o) != 0:
				for stream in self.o:
					if stream not in downstreamUnitList:
						downstreamUnitList.append(stream)
					else:
						continue
				for subunit in downstreamUnitList[index:]:
					if subunit.typeOfUnit == "stream":
						subunit.get_downstream_units(downstreamUnitList)
					else:
						continue
			else:
				return []
		elif self.typeOfUnit == "stream":
			if self.t != None:
				if self.t not in downstreamUnitList:
					downstreamUnitList.append(self.t)
				self.t.get_downstream_units(downstreamUnitList)
			else:
				pass
		else:
			print("this shouldn't be happening")

		return downstreamUnitList


	def __str__(self):
		return self.name
################################################################################################################################################################
###############################################################################################################################################################
class node(unit): #right now these just have mixer functionality it looks like
	def __init__(self,name):
		unit.__init__(self,name)
		self.i = list()
		self.o = list()
		self.typeOfUnit = "node"
		unitRegistry["node"].append(self)

	def specify_connections(self,i=list(),o=list()):
		for stream in i:
			self.i.append(stream)
		for stream in o:
			self.o.append(stream)

	def make_connections(self):
		for stream in unitRegistry["stream"]:
			if stream.t == self and stream not in self.i:
				self.i.append(stream)
			elif stream.f == self and stream not in self.o:
				self.o.append(stream)
			else:
				continue

	def print_connections(self):
		if len(self.i) != 0:
			print(self.name + " Incoming streams:")
			for stream in self.i:
				print(stream.name)
		else:
			print("No incoming streams")

		if len(self.o) != 0:
			print("\n\n" + self.name + " Outgoing streams:")
			for stream in self.o:
				print(stream.name)
		else:
			print("no outgoing streams")
		print("\n")
##############################################################################################################################################################
################################################################################################################################################################
class stream(unit):
	def __init__(self,name,flow = "mass", flowUnits = "kg/hr", temperature = 25, tempUnits = "C", pressure = 1, pressUnits = "atm"):
		unit.__init__(self,name)
		self.t = None
		self.f = None
		self.flow = flow
		self.flowUnits = flowUnits
		self.temp = temperature
		self.tempUnits = tempUnits
		self.pressure = pressure
		self.pressUnits = pressUnits
		self.typeOfUnit = "stream"
		unitRegistry["stream"].append(self)

	def make_connections(self):
		for node in unitRegistry["node"]:
			if self in node.i:
				self.t = node
			elif self in node.o:
				self.f = node
			else:
				continue

	def print_connections(self):
		print(self.name + " going to " + str(self.t))
		print(self.name + " coming from " + str(self.f))
		print("\n")
#############################################################################################################################################################
###############################################################################################################################################################
class material():
	pass
#############################################################################################################################################################
###############################################################################################################################################################
def print_unitRegistry():
	for node in unitRegistry["node"]:
		print(node)
	for stream in unitRegistry["stream"]:
		print(stream)

def print_all():
	print_unitRegistry()

def make_all_connections():
	for node in unitRegistry["node"]:
		node.make_connections()
	for stream in unitRegistry["stream"]:
		stream.make_connections()

def print_all_connections():
	for node in unitRegistry["node"]:
		node.print_connections()
	for stream in unitRegistry["stream"]:
		stream.print_connections()

def detect_unconnected_units():
	unitList = list()
	for node in unitRegistry["node"]:
		if len(node.i) == 0 or len(node.o) == 0:
			unitList.append(node)
	for stream in unitRegistry["stream"]:
		if stream.t == None and stream.f == None:
			unitList.append(stream)
	if len(unitList) == 0:
		return 0,unitList
	else:
		return 1,unitList
