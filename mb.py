import random

global commandIndex
commandIndex = ["init"]
global commandLog
commandLog = list()
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
		self.name=name

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
##############################################################################################################################################################
################################################################################################################################################################
class stream(unit):
	def __init(self,name,flow = "mass", flowUnits = "kg/hr", temperature = 25, tempUnits = "C", pressure = 1, pressUnits = "atm"):
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
#############################################################################################################################################################
###############################################################################################################################################################
class material():
	pass
#############################################################################################################################################################
###############################################################################################################################################################
class command():
	def __init__(self):
		pass
	def get_base(self):
		self.base = input("(add,a),(modify,m),(remove,r), or (quit,q)\n")
		if self.base == "":
			return 0
		self.base = self.base[0] #Think this gets the first letter of the base command
		return 1
	def get_unit(self):
		unitString = input("unit name?(ex: n01, s01)\n")
		if unitString == "":
			return ""
		self.typeOfUnit = unitString[0:1]
		self.unit = unitString
		return 1
	def get_detail(self): #change this so it only runs once per successful command
		if self.base == "a":
			self.add_unit()
			return 1
		elif self.base == "m":
			#need to check that it exists first before calling anything below this.
			self.modify_unit()
			return 1
		elif self.base == "r":
			return 1
		elif self.base == "q":
			return ""
		elif self.base == "":
			return ""
		else:
			return 0
	def add_unit(self):
		if self.typeOfUnit == "n":
			self.unit = node(self.unit)
		elif self.typeOfUnit == "s":
			self.unit = stream(self.unit)

	def modify_unit(self):
		prompt = input("Which attribute to modify? (\"?\" prints a list of modifiable attributes")
		if prompt == "?":
			print(self.unit.__dict__())
		#WIP

	def remove_unit(self):
		pass

	def undo_command(self):
		pass

	def print_help_text(self):
		pass

	def log_command(self):
		commandLog.append(str(self))

	def __str__(self):
		return self.base + "_" + str(self.unit)
#############################################################################################################################################################
###############################################################################################################################################################
def get_command():
	currentCommand = command_hash()
	currentCommand = command()
	unitDone = 0
	while unitDone != 1:
		unitDone = currentCommand.get_unit()
		if unitDone == 0:
			return 0
		baseDone = 0
		while unitDone == 1 and baseDone != 1:
			baseDone = currentCommand.get_base()
			if baseDone == "":
				continue
			detailDone = 0
			while unitDone == 1 and baseDone == 1 and detailDone != 1:
				detailDone = currentCommand.get_detail()
				if detailDone == "":
					continue
	currentCommand.log_command()

def command_hash():
	hash = "init"
	while hash in commandIndex:
		hash = random.randint(1,9999)
	commandIndex.append(hash)
	return hash

def print_commandLog():
	for command in commandLog:
		print(command)
def print_unitRegistry():
	for node in unitRegistry["node"]:
		print(node)
	for stream in unitRegistry["stream"]:
		print(stream)
#############################################################################################################################################################
def main():
	get_command()
	print_commandLog()
	print_unitRegistry()
##############################################################################################################################################################
main()

