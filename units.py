import math

global nodeRegistry
nodeRegistry = list()
global streamRegistry
streamRegistry = list()
global unitRegistry
unitRegistry = {
	"node" : nodeRegistry,
	"stream" : streamRegistry
	}
global materialRegistry
materialRegistry = list()

global unitConversionDict
global massUnitConversionDict
massUnitConversionDict = {
	"kg" : 1,
	"lb" : 0.45359,
	"oz" : 0.028349375,
	"ton" : 907.28 #regular ton, not short ton
}
global volumeUnitConversionDict
volumeUnitConversionDict = dict()
global moleUnitConversionDict
moleUnitConversionDict = dict()
global energyUnitConversionDict
energyUnitConversionDict = dict()
global pressureUnitConversionDict
pressureUnitConversionDict = dict()
global timeUnitConversionDict
timeUnitConversionDict = {
	"second" : 1,
	"minute" : 60,
	"hour" : 3600,
	"day" : 86400,
	"week" : 604800,
	"op. year" : 2851200,
	"year" : 31536000
}
unitConversionDict = {
	"mass" : massUnitConversionDict,
	"volume" : volumeUnitConversionDict,
	"mole" : moleUnitConversionDict,
	"energy" : energyUnitConversionDict,
	"pressure" : pressureUnitConversionDict,
	"time" : timeUnitConversionDict
}

# global exceptions
# exceptions = list() #will be a list containing strings explaining errors
###############################################################################################################################################################
###############################################################################################################################################################
class unit:
	def __init__(self,name,flowRate = None, flowType = "mass", flowUnits = "kg/hr", temperature = 25, tempUnits = "C", pressure = 1, pressUnits = "atm"):
		self.componentIdentities = list()
		self.typeOfUnit = "base" #should be overwritten by any other child class
		self.subTypeOfUnit = None
		self.name = name
		self.flowType = flowType
		self.flowRate = flowRate
		self.flowUnits = flowUnits
		self.temp = temperature
		self.tempUnits = tempUnits
		self.pressure = pressure
		self.pressUnits = pressUnits
		#self.specify_component_identities()

	def unconditional_update(self):
		pass

	def delete(self):
		if self in unitRegistry["node"]:
			unitRegistry["node"].remove(self)
		elif self in unitRegistry["stream"]:
			unitRegistry["stream"].remove(self)
		else:
			print("I couldn't find this shit anywhere dawg")
		del self

	def get_all_downstream_units(self, downstreamUnitList=None):
		if downstreamUnitList is None:
			downstreamUnitList = []
		return self.get_downstream_units(downstreamUnitList)

	def get_all_upstream_units(self, upstreamUnitList=None):
		if upstreamUnitList is None:
			upstreamUnitList = []
		return self.get_upstream_units(upstreamUnitList)

	def get_downstream_units(self,downstreamUnitList):
		if len(downstreamUnitList) == 0 or downstreamUnitList[0] == "init":
			#downstreamUnitList[0] = self
			downstreamUnitList = []
		else:
			pass

		index = len(downstreamUnitList)

		if self.typeOfUnit == "node":
			if len(self.o) != 0:
				for streamUnit in self.o:
					if streamUnit not in downstreamUnitList:
						downstreamUnitList.append(streamUnit)
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
			if self.t is not None:
				if self.t not in downstreamUnitList:
					downstreamUnitList.append(self.t)
				self.t.get_downstream_units(downstreamUnitList)
			else:
				pass
		else:
			print("this shouldn't be happening")

		return downstreamUnitList

	def get_upstream_units(self,upstreamUnitList): #hopefully it will be as easy as copying the above...
		if len(upstreamUnitList) == 0 or upstreamUnitList[0] == "init":
			#downstreamUnitList[0] = self
			upstreamUnitList = []
		else:
			pass

		index = len(upstreamUnitList)

		if self.typeOfUnit == "node":
			if len(self.i) != 0:
				for streamUnit in self.i:
					if streamUnit not in upstreamUnitList:
						upstreamUnitList.append(streamUnit)
					else:
						continue
				for subunit in upstreamUnitList[index:]:
					if subunit.typeOfUnit == "stream":
						subunit.get_upstream_units(upstreamUnitList)
					else:
						continue
			else:
				return []
		elif self.typeOfUnit == "stream":
			if self.f is not None:
				if self.f not in upstreamUnitList:
					upstreamUnitList.append(self.f)
				self.f.get_upstream_units(upstreamUnitList)
			else:
				pass
		else:
			print("this shouldn't be happening")

		return upstreamUnitList

	def calculate_DoF(self): #this parent method should never be called, and is overwritten by each child class
		pass

	# def check_exceptions(self): #maybe look into making exceptions a new class idk
	# 	pass

	def __str__(self):
		return self.name
################################################################################################################################################################
###############################################################################################################################################################
class node(unit):
	def __init__(self,name):
		unit.__init__(self,name)
		self.unknownDict = dict()
		self.flowIn = int()
		self.flowOut = int()
		self.flowInOutContainsNone = 0  # this feels retarded to me
		self.numberOfUnknownFlowRates = int()
		self.i = list()
		self.o = list()
		self.typeOfUnit = "node"
		unitRegistry["node"].append(self)

	def unconditional_update(self): #unconditional update is called at the beginning of each method or function when a unit is being checked or having calculations run on it.
		self.make_connections()
		self.get_flow_in_out()
		#self.calculate_DoF()

	def specify_connections(self,i,o):
		for streamUnit in i:
			self.i.append(streamUnit)
		for streamUnit in o:
			self.o.append(streamUnit)

	def make_connections(self):
		for streamUnit in unitRegistry["stream"]:
			if streamUnit.t == self and streamUnit not in self.i:
				self.i.append(streamUnit)
			elif streamUnit.f == self and streamUnit not in self.o:
				self.o.append(streamUnit)
			else:
				continue

	def print_connections(self):
		if len(self.i) != 0:
			print(self.name + " Incoming streams:")
			for streamUnit in self.i:
				print(streamUnit.name)
		else:
			print("No incoming streams")

		if len(self.o) != 0:
			print("\n\n" + self.name + " Outgoing streams:")
			for streamUnit in self.o:
				print(streamUnit.name)
		else:
			print("no outgoing streams")
		print("\n")

	# def get_flow_in_out(self): #this *may* exhibit recursion issues since it calls the child method of the same name. I don' think it will but you can never be too sure
	# 	#really don't like this method, I'm going to rewrite it so that the parent node has the functinoality rather than calling its child. this is retarded.
	# 	tempSystem = system("temp",self.i,self.o)
	# 	self.flowIn = tempSystem.flowIn
	# 	self.flowOut = tempSystem.flowOut
	# 	self.numberOfUnknownFlowRates = tempSystem.numberOfUnknownFlowRates
	# 	del tempSystem

	def get_flow_in_out(self):
		containsNone = 0
		i = 0
		o = 0
		for streamObject in self.i:
			if streamObject.flowRate is None:
				containsNone = 1
				continue
			i += streamObject.flowRate
		for streamObject in self.o:
			if streamObject.flowRate is None:
				containsNone = 1
				continue
			o += streamObject.flowRate
		self.flowInOutContainsNone = containsNone
		self.flowIn = i
		self.flowOut = o

	def calculate_DoF(self):
		unknownTuple = self.get_unknown_values()
		components = {
			"flowRates" : unknownTuple[2],
			"fractions" : unknownTuple[3]
		}
		self.unknownDict = {
			"streams" : unknownTuple[1],
			"components" : components
		}
		return unknownTuple[0] - self.get_possible_equations()

	def get_unknown_values(self):
		unknowns = 0
		errorDict = {
			"streamFlowRates" : list(),
			"componentFlowRates" : list(),
			"componentFractions" : list()
		}
		for streamObject in self.i:
			unknownTuple = streamObject.get_unknown_values()
			unknowns += unknownTuple[0]
			if unknownTuple[1] is not None:
				errorDict["streamFlowRates"].append(unknownTuple[1])
			errorDict["componentFlowRates"].extend(unknownTuple[2])
			errorDict["componentFractions"].extend(unknownTuple[3])
		for streamObject in self.o:
			unknownTuple = streamObject.get_unknown_values()
			unknowns += unknownTuple[0]
			if unknownTuple[1] is not None:
				errorDict["streamFlowRates"].append(unknownTuple[1])
			errorDict["componentFlowRates"].extend(unknownTuple[2])
			errorDict["componentFractions"].extend(unknownTuple[3])
		nodeTuple = (unknowns , errorDict["streamFlowRates"] , errorDict["componentFlowRates"] , errorDict["componentFractions"])
		return nodeTuple

	def get_possible_equations(self):
		pass

	# def check_exceptions(self):
	# 	unit.check_exceptions(self)
	# 	if (self.flowIn != self.flowOut) and (self.flowInOutContainsNone != 1) and (self.flowType == "mass" or self.flowType == "mole"):
	# 		#to raise this exception, flowIn != flowOut AND BOTH flowIn and flowOut have some value (ie not None)
	# 		specify_exception("for flowType " + self.flowType + ", the value of flow in and out must be equal. Please re-specify the streams surrounding this node: " + self.name,"units.node.check_exceptions()")
##############################################################################################################################################################
################################################################################################################################################################
class mixer(node):
	def __init__(self,name):
		node.__init__(self,name)
		self.subTypeOfUnit = "mixer"

##############################################################################################################################################################
################################################################################################################################################################

class system(node):
	def __init__(self,name,i = None,o = None):
		node.__init__(self,name)
		self.numberOfUnknownFlowRates = int()
		self.contents = list()
		self.get_bounds(i,o)
		self.get_contents()
		self.get_flow_in_out()
		self.typeOfUnit = "system"
		unitRegistry["node"].remove(self)

	def get_bounds(self,i,o): #need to add handling for if either i OR o are == None
		if i is None and o is None:
			#check which streams only stream.f and which ones only have stream.t
			for streamObject in unitRegistry["stream"]:
				if streamObject.f is None and streamObject.t is not None:
					self.i.append(streamObject)
				elif streamObject.f is not None and streamObject.t is None:
					self.o.append(streamObject)
				else:
					continue
		else:
			self.i = i
			self.o = o

	def get_contents(self):
		forwardContents = self.construct_forward_content_list()
		backwardContents = self.construct_backward_content_list()
		check = self.compare_content_lists(forwardContents,backwardContents)
		if check == 0:
			self.contents = forwardContents
		else:
			print("Invalid bounds, the degree of separation is " + str(check))

	def construct_forward_content_list(self):
		forwardContents = list()
		for streamObject in self.i:
			forwardHolding = streamObject.get_all_downstream_units()
			for entry in forwardHolding:
				if entry not in forwardContents:
					forwardContents.append(entry)
		for streamObject in self.o:
			forwardHolding = streamObject.get_all_downstream_units()
			for entry in forwardHolding:
				if entry in forwardContents:
					forwardContents.remove(entry)
			if streamObject in forwardContents:
				forwardContents.remove(streamObject)
		return forwardContents

	def construct_backward_content_list(self):
		backwardContents = list()
		for streamObject in self.o:
			backwardHolding = streamObject.get_all_upstream_units()
			for entry in backwardHolding:
				if entry not in backwardContents:
					backwardContents.append(entry)
		for streamObject in self.i:
			backwardHolding = streamObject.get_all_upstream_units()
			for entry in backwardHolding:
				if entry in backwardContents:
					backwardContents.remove(entry)
			if streamObject in backwardContents:
				backwardContents.remove(streamObject)
		return backwardContents

	@staticmethod
	def compare_content_lists(forward, backward):
		checkedList = list()
		degreeOfSeparation = 0
		for entry in forward:
			if entry not in backward and entry not in checkedList:
				degreeOfSeparation += 1
			checkedList.append(entry)
		for entry in backward:
			if entry not in forward and entry not in checkedList:
				degreeOfSeparation += 1
			checkedList.append(entry)
		return degreeOfSeparation

	def get_unknown_values(self):
		unknowns = 0
		errorDict = {
			"streamFlowRates": set(),
			"componentFlowRates": set(),
			"componentFractions": set()
		}
		for unitObject in self.contents:
			if unitObject.typeOfUnit == "node":
				unknownTuple = unitObject.get_unknown_values()
				unknowns += unknownTuple[0]
				errorDict["streamFlowRates"].update(unknownTuple[1])
				errorDict["componentFlowRates"].update(unknownTuple[2])
				errorDict["componentFractions"].update(unknownTuple[3])

		#just gonna try this
		unknowns = len(errorDict["streamFlowRates"]) + len(errorDict["componentFlowRates"]) + len(errorDict["componentFractions"])

		systemTuple = (unknowns , errorDict["streamFlowRates"] , errorDict["componentFlowRates"] , errorDict["componentFractions"])
		return systemTuple

	def force_overall_balance(self,iterand,interval,lowerBound,upperBound,tolerance):
		if self.numberOfUnknownFlowRates >= 2:
			print("It is not recommended to use this iterative strategy with more than one unknown")
			return 0
		iterand = lowerBound
		sqrdDiff = self.calculate_sqrdDiff()
		overFlow = 0
		overFlowLimit = 100000
		while sqrdDiff > tolerance and iterand < upperBound and overFlow < overFlowLimit:
			iterand += interval
			sqrdDiff = self.calculate_sqrdDiff()
			overFlow += 1
		if sqrdDiff <= tolerance:
			print("success")
		elif iterand >= upperBound:
			print("iterand exceeded the upperbound")
		elif overFlow >= overFlowLimit:
			print("over flow limit exceeded")
		else:
			return 0

	def calculate_sqrdDiff(self):
		self.get_flow_in_out()
		return abs(pow(self.flowIn,2)-pow(self.flowOut,2))

##############################################################################################################################################################
################################################################################################################################################################
class stream(unit):
	def __init__(self,name):
		unit.__init__(self,name)
		self.specify_component_identities()
		self.t = None
		self.f = None
		self.typeOfUnit = "stream"
		unitRegistry["stream"].append(self)

	def make_connections(self):
		for nodeObject in unitRegistry["node"]:
			if self in nodeObject.i:
				self.t = nodeObject
			elif self in nodeObject.o:
				self.f = nodeObject
			else:
				continue

	def print_connections(self):
		print(self.name + " going to " + str(self.t))
		print(self.name + " coming from " + str(self.f))
		print("\n")

	def specify_component_identities(self):
		if len(materialRegistry) == 0:
			print("no materials specified for system")
			return 0
		for materialObject in materialRegistry:
			newComponent = component(self, materialObject, self.name + "_" + materialObject.name)
			self.componentIdentities.append(newComponent)

	def specify_component_fractions(self, componentNameList, fractionType, componentFraction):
		componentList = list() #initializing componentList
		if len(componentNameList) == 0: #if no argument is returned for componentNameList, it is assumed that fractions are being specified for each component material in the system
			componentList = self.componentIdentities
		else:
			for name in componentNameList:
				componentObject = self.get_component_by_material_name(name) #get's components by their names that have been passed in componentNameList
				componentList.append(componentObject)
		if self.check_componentList_and_values(componentList,componentFraction) != 1: #checks to ensure that both arg lists are the same length
			return 0
		for componentObject in componentList: #now assigning fractions to specific components
			componentObject.fractionType = fractionType #can be molar or mass fraction type
			componentObject.fractionValue = componentFraction[componentList.index(componentObject)]

	def specify_component_flow_rates(self,componentNameList,flowType,componentFlowRate):
		if flowType is None:
			flowType = self.flowType #self.flowType is "mass" by default
		componentList = list()
		if len(componentNameList) == 0:
			componentList = self.componentIdentities
		else:
			for name in componentNameList:
				componentObject = self.get_component_by_material_name(name)
				componentList.append(componentObject)
		if self.check_componentList_and_values(componentList,componentFlowRate) != 1:
			return 0
		for componentObject in componentList:
			componentObject.flowType = flowType
			componentObject.flowRate = componentFlowRate[componentList.index(componentObject)]

	@staticmethod
	def check_componentList_and_values(componentList, values):
		if len(componentList) != len(values):
			return 0
		else:
			return 1

	def get_component_by_material_name(self,materialName): #this check is utterly retarded but I don't want to think of a better way for now
		for componentObject in self.componentIdentities:
			if componentObject.name.find(materialName) != -1:
				return componentObject
		return 0

	def get_unknown_values(self): #WIPWIPWIPWIPWIPWIP
		unknowns = 0
		errorDict = {
			"streamFlowRate" : None,
			"componentFlowRates" : list(),
			"componentFractions" : list()
		}
		if self.flowRate is None:
			errorDict["streamFlowRate"] = self
			unknowns += 1
		for componentObject in self.componentIdentities:
			unknownTuple = componentObject.get_unknown_values()
			print("components: " + componentObject.name + str(unknownTuple))
			unknowns += unknownTuple[0]
			if unknownTuple[1] is not None:
				errorDict["componentFlowRates"].append(unknownTuple[1])
			if unknownTuple[2] is not None:
				errorDict["componentFractions"].append(unknownTuple[2])
		streamTuple = (unknowns, errorDict["streamFlowRate"], errorDict["componentFlowRates"] , errorDict["componentFractions"])
		print("streamTuple: " + str(streamTuple))
		return streamTuple

	# def check_exceptions(self): #this method really sucks and I hate it!
	# 	unit.check_exceptions(self)
	# 	if (self.flowRate != self.f.flowRate or self.flowRate != self.t.flowRate) and (self.flowType == "mass" or self.flowType == "mole"):
	# 		specify_exception("Overspecified information for: " + self.name + " between nodes: " + self.f.name + " and " + self.t.name + ". the mass flowRate must be the same between these units","units.stream")


#############################################################################################################################################################
###############################################################################################################################################################
class material: #will define a material and its typical physical/chemical properties
	def __init__(self,name,mw):
		self.name = name
		self.mw = mw
		materialRegistry.append(self)
#############################################################################################################################################################
###############################################################################################################################################################
class component: #will be a specific representation of a material per unit
	def __init__(self, parentUnit, materialObject, name):
		self.name = name

		self.flowType = str()
		self.flowUnits = str()
		self.temp = float()
		self.tempUnits = str()
		self.pressure = float()
		self.pressUnits = str()

		self.material = materialObject
		self.fractionType = None
		self.fractionValue = None
		self.flowRate = None
		self.get_unit_attr(parentUnit)

	def get_unit_attr(self, parentUnit):
		"""
			How does a docstring work??
		:type parentUnit: object
		"""
		self.flowType = parentUnit.flowType
		self.flowUnits = parentUnit.flowUnits
		self.temp = parentUnit.temp
		self.tempUnits = parentUnit.tempUnits
		self.pressure = parentUnit.pressure
		self.pressUnits = parentUnit.pressUnits

	def get_unknown_values(self):
		unknowns = 0
		errorDict = {
			"flowRate" : None,
			"fraction" : None
		}
		if self.flowRate is None:
			unknowns += 1
			errorDict["flowRate"] = self
		if self.fractionValue is None:
			unknowns += 1
			errorDict["fraction"] = self
		componentTuple = (unknowns,errorDict["flowRate"],errorDict["fraction"])
		return componentTuple

#############################################################################################################################################################
###############################################################################################################################################################
def print_unitRegistry():
	for nodeObject in unitRegistry["node"]:
		print(nodeObject)
	for streamObject in unitRegistry["stream"]:
		print(streamObject)

def print_all():
	print_unitRegistry()

def make_all_connections():
	for nodeObject in unitRegistry["node"]:
		nodeObject.make_connections()
	for streamObject in unitRegistry["stream"]:
		streamObject.make_connections()

def print_all_connections():
	for nodeObject in unitRegistry["node"]:
		nodeObject.print_connections()
	for streamObject in unitRegistry["stream"]:
		streamObject.print_connections()

def detect_unconnected_units():
	unitList = list()
	for nodeObject in unitRegistry["node"]:
		if len(nodeObject.i) == 0 or len(nodeObject.o) == 0:
			unitList.append(nodeObject)
	for streamObject in unitRegistry["stream"]:
		if streamObject.t is None and streamObject.f is None:
			unitList.append(streamObject)
	if len(unitList) == 0:
		return 0,unitList
	else:
		return 1,unitList

# def specify_exception(message, methodName = None):
# 	if methodName is None:
# 		errorString = "Exception raised: " + message
# 	else:
# 		errorString = "Exception raised in method" + methodName + ": " + message
# 	print(errorString)
# 	exceptions.append(errorString)
#
# def print_exceptions():
# 	if len(exceptions) != 0:
# 		for message in exceptions:
# 			print(message)

def convert_unit(fromUnitStr,toUnitStr):
	fromUnit = parse_unit_string(fromUnitStr)
	toUnit = parse_unit_string(toUnitStr)


def parse_unit_string(string):
	unitTuple = tuple()
	if string.find("/") == -1:
		unitTuple = (string,)
	elif string.find("/") != -1:
		numerator = string[0:string.find("/")]
		denominator = string[string.find("/") + 1 :]
		unitTuple = (numerator,denominator)
	return unitTuple

def get_unit_conversion_type(baseUnit):
	pass

def get_type(obj):
	if isinstance(obj, node): #parent class then children in a nested if-elif
		if isinstance(obj, mixer):
			return "mixer"
		elif isinstance(obj, system):
			return "system"
		return "node"

	elif isinstance(obj, stream):
		return "stream"

	elif isinstance(obj, component):
		return "component"

	elif isinstance(obj,material):
		return "material"

	else:
		return None
