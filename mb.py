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
		unitString = input("unit name?(ex: n01, s01)\n")
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

	get_command_unit_name(currentCommand)
	get_command_base(currentCommand)
	get_command_details(currentCommand)

	currentCommand.log_command()

def command_hash():
	hash = "init"
	while hash in commandIndex:
		hash = random.randint(1,9999)
	commandIndex.append(hash)
	return hash

def get_command_unit_name(command):
	done = 0
	while done != 1:
		done = command.get_unit()
		if done == "":
			return ""
	return 1

def get_command_base(command):
        done = 0
        while done != 1:
                done = command.get_base()
                if done == "":
                    return "" #does this exit the function or just the loop?? I'll find out later I guess
        return 1

def get_command_details(command):
        done = 0
        command.get_detail()

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

