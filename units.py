

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

	def __str__(self):
		return self.name
################################################################################################################################################################
###############################################################################################################################################################
class node(unit): #right now these just have mixer functionality it looks like
	def __init__(self,name):
		unit.__init__(self,name)
		self.i = list()
		self.o = list()
		unitRegistry["node"].append(self)

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
