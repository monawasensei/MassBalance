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
global commandSwitch
commandSwitch = {
	"a":"self.add_unit",
	"m":"self.modify_unit",
	"r":"self.remove_unit",
	"p":"print_all"
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
#############################################################################################################################################################
###############################################################################################################################################################
class material():
	pass
#############################################################################################################################################################
###############################################################################################################################################################
class command():
	def __init__(self,raw):
		self.raw = raw
		self.parse_command()
		self.command_switch()

	def parse_command(self):
		#commands will be passed like add unit n01 or add unit:s04 or modify unit:n01 and so on
		#the base commands can be written as 'a' or 'add' for example
		cmdPos = 0
		unitPos = self.raw.find(" ",cmdPos + 1)
		unitNamePos = self.raw.find(" ",unitPos + 1)
		self.base = self.raw[cmdPos]
		self.object = self.raw[unitNamePos + 1:]
		self.get_unit()

	def command_switch(self): #this probably is going to break at some point in the near future.
		cmd = commandSwitch[self.base]
		eval(cmd + "()")

	def get_base(self):
                #returns 1 when a valid command is chosen, returns 0 if invalid command, returns "" if 'quit' command is chosen or if null string is entered
		self.base = input("(add,a),(modify,m),(remove,r), or (quit,q)\n")
		if self.base == "" or self.base == "q" or self.base == "quit":
                        return ""
		self.base = self.base[0]
		if self.base not in list(["a","m","r"]):
			return 0
		return 1

	def get_unit(self):
		#Returns "" if no selection is made, returns 1 for a valid selection, returns 0 if invalid typeOfUnit designation
		unitString = self.object
		if unitString == "":
			return ""
		self.typeOfUnit = unitString[0:1]
		if self.typeOfUnit != "n" and self.typeOfUnit != "s":
			return 0 #This is for an invalid unit name
		self.unit = unitString
		if self.unit_state() == 0:
			self.extant_unit = False
		else:
			self.extant_state = True
		return 1

	def unit_state(self):
		if self.typeOfUnit == "n":
			if self.unit in unitRegistry["node"]:
				return 1
			else:
				return 0
		elif self.typeOfUnit == "s":
			if self.unit in unitRegistry["stream"]:
				return 1
			else:
				return 0

	def add_unit(self):
		if self.typeOfUnit == "n":
			self.unit = node(str("node_" + self.unit))
		elif self.typeOfUnit == "s":
			self.unit = stream(str("stream_" + self.unit))

	def modify_unit(self):
		prompt = input("Which attribute to modify? (\"?\" prints a list of modifiable attributes")
		if prompt == "?":
			print(self.unit.__dict__())
		#WIP

	def remove_unit(self):
		n01.delete()
		#self.unit.delete()

	def undo_command(self):
		pass

	def print_help_text(self):
		pass

	def log_command(self):
		commandLog.append(str(self))

	def __str__(self):
		return self.base + "_" + str(self.object)

#############################################################################################################################################################
###############################################################################################################################################################
def get_command():
	commandRaw = input("Input command\n(add, a),(modify,m),(remove,r) followed by \'unit\' then the unit name ex: \'a unit n01\'\n")
	if commandRaw == "quit" or commandRaw == "q":
		return 0
	commandID = command_hash()
	commandID = command(commandRaw)
	commandID.log_command()
	return commandID

def command_hash(): #is there any reason for this to be a hash instead of sequential assignment?
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

def print_all():
	print_commandLog()
	print_unitRegistry()
#############################################################################################################################################################
def main(): #i want to make the get_command a loop or something
	commandLoop = ""
	while commandLoop != 0:
		commandLoop=get_command()
	#test = command("modify unit s078978")
	#print_commandLog()
	#print_unitRegistry()
##############################################################################################################################################################

