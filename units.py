

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
###############################################################################################################################################################
###############################################################################################################################################################
class unit():
	def __init__(self,name,flowRate = None, flowType = "mass", flowUnits = "kg/hr", temperature = 25, tempUnits = "C", pressure = 1, pressUnits = "atm"):
		self.name = name
		self.specify_component_identities()
		self.flowType = flowType
		self.flowRate = flowRate
		self.flowUnits = flowUnits
		self.temp = temperature
		self.tempUnits = tempUnits
		self.pressure = pressure
		self.pressUnits = pressUnits

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

	def get_upstream_units(self,upstreamUnitList): #hopefully it will be as easy as copying the above...
		if len(upstreamUnitList) == 0 or upstreamUnitList[0] == "init":
			#downstreamUnitList[0] = self
			upstreamUnitList = []
		else:
			pass

		index = len(upstreamUnitList)

		if self.typeOfUnit == "node":
			if len(self.i) != 0:
				for stream in self.i:
					if stream not in upstreamUnitList:
						upstreamUnitList.append(stream)
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
			if self.f != None:
				if self.f not in upstreamUnitList:
					upstreamUnitList.append(self.f)
				self.f.get_upstream_units(upstreamUnitList)
			else:
				pass
		else:
			print("this shouldn't be happening")

		return upstreamUnitList

	def specify_component_identities(self):
		if len(materialRegistry) == 0:
			print("no materials specified for system")
			return 0
		self.componentIdentities = list()
		for material in materialRegistry:
			newComponent = component(self,material,self.name + "_" + material.name)
			self.componentIdentities.append(newComponent)

	def specify_component_fractions(self,componentNameList = [], componentFraction, fractionType = "mass"):
		componentList = list() #initializing componentList
		if len(componentNameList) == 0: #if no argument is returned for componentNameList, it is assumed that fractions are being specified for each component material in the system
			componentList = self.componentIdentities
		else:
			for name in componentNameList:
				component = self.get_component_by_material_name(name) #get's components by their names that have been passed in componentNameList
				componentList.append(component)
		if self.check_componentList_and_values(componentList,componentFraction) != 1: #checks to ensure that both arg lists are the same length
			return 0
		for component in componentList: #now assigning fractions to specific components
			component.fractionType = fractionType #can be molar or mass fraction type
			component.fractionValue = componentFraction[componentList.index(component)]

	def specify_component_flow_rates(self,componentNameList = [],componentFlowRate,flowType = None):
		if flowType == None:
			flowType = self.flowType #self.flowType is "mass" by default
		componentList = list()
		if len(componentNameList) == 0:
			componentList = self.componentIdentities
		else:
			for name in componentNameList:
				component = self.get_component_by_material_name(name)
				componentList.append(component)
		if self.check_components_and_values(componentList,componentFlowRate) != 1:
			return 0
		for component in componentList:
			component.flowType = flowType
			component.flowRate = componentFlowRate[componentList.index(component)]

	def check_componentList_and_values(self,componentList,values):
		if len(componentList) != len(values):
			return 0
		else:
			return 1

	def get_component_by_material_name(self,materialName):
		for component in self.componentIdentities:
			if component.name == materialName:
				return component
		return 0

	def __str__(self):
		return self.name
################################################################################################################################################################
###############################################################################################################################################################
class node(unit):
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

	def get_flow_in_out(self): #this *may* exhibit recursion issues since it calls the child method of the same name. I don' think it will but you can never be too sure
		tempSystem = system("temp",self.i,self.o)
		self.flowIn = tempSystem.flowIn
		self.flowOut = tempSystem.flowOut
		self.numberOfUnkownFlowRates = tempSystem.numberOfUnkownFlowRates
		del tempSystem
##############################################################################################################################################################
################################################################################################################################################################
class mixer(node):
	def __init__(self,name):
		node.__init__(self,name)

##############################################################################################################################################################
################################################################################################################################################################

class system(node):
	def __init__(self,name,i = None,o = None):
		node.__init__(self,name)
		self.get_bounds(i,o)
		self.get_contents()
		self.get_flow_in_out()
		self.typeOfUnit = "system"
		unitRegistry["node"].remove(self)

	def get_bounds(self,i,o): #need to add handling for if either i OR o are == None
		if i == None and o == None:
			#check which streams only stream.f and which ones only have stream.t
			for stream in unitRegistry["stream"]:
				if stream.f == None and stream.t != None:
					self.i.append(stream)
				elif stream.f != None and stream.t == None:
					self.o.append(stream)
				else:
					continue
		else:
			self.i = i
			self.o = o

	def get_contents(self):
		forwardContents = list()
		backwardContents = list()
		check = int()
		forwardContents = self.construct_forward_content_list()
		backwardContents = self.construct_backward_content_list()
		check = self.compare_content_lists(forwardContents,backwardContents)
		if check == 0:
			self.contents = forwardContents
		else:
			print("Invalid bounds, the degree of separation is " + str(check))

	def construct_forward_content_list(self):
		forwardHolding = list()
		forwardContents = list()
		for stream in self.i:
			forwardHolding = stream.get_all_downstream_units()
			for entry in forwardHolding:
				if entry not in forwardContents:
					forwardContents.append(entry)
		for stream in self.o:
			forwardHolding = stream.get_all_downstream_units()
			for entry in forwardHolding:
				if entry in forwardContents:
					forwardContents.remove(entry)
			if stream in forwardContents:
				forwardContents.remove(stream)
		return forwardContents

	def construct_backward_content_list(self):
		backwardContents = list()
		backwardHolding = list()
		for stream in self.o:
			backwardHolding = stream.get_all_upstream_units()
			for entry in backwardHolding:
				if entry not in backwardContents:
					backwardContents.append(entry)
		for stream in self.i:
			backwardHolding = stream.get_all_upstream_units()
			for entry in backwardHolding:
				if entry in backwardContents:
					backwardContents.remove(entry)
			if stream in backwardContents:
				backwardContents.remove(stream)
		return backwardContents

	def compare_content_lists(self,forward,backward):
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

	def get_flow_in_out(self,guess = 0):
		errorCount = 0
		i = 0
		o = 0
		for stream in self.i:
			if stream.flowRate == "unknown":
				stream.flowRate = guess
				errorCount += 1
			i += stream.flowRate
		for stream in self.o:
			if stream.flowRate == "unknown":
				stream.flowRate = guess
				errorCount += 1
			o += stream.flowRate
		self.flowIn = i
		self.flowOut = o
		self.numberOfUnknownFlowRates = errorCount
##############################################################################################################################################################
################################################################################################################################################################
class stream(unit):
	def __init__(self,name):
		unit.__init__(self,name)
		self.t = None
		self.f = None
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
class material(): #will define a material and it's typical physical/chemical properties
	def __init__(self,name,mw):
		self.name = name
		self.mw = mw
		materialRegistry.append(self)
#############################################################################################################################################################
###############################################################################################################################################################
class component(): #will be a specific representation of a material per unit
	def __init__(self,parentUnit,material,name):
		self.name = name
		self.material = material
		materialRegistry.remove(self)
		self.fractionType = None
		self.fractionValue = None
		self.flowRate = None
		self.get_unit_attr(parentUnit)

	def get_stream_attr(self,unit):
		self.flowType = unit.flowType
		self.flowUnits = unit.flowUnits
		self.temp = unit.temp
		self.tempUnits = unit.tempUnits
		self.pressure = unit.pressure
		self.pressUnits = unit.pressUnits
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

def make_bulk_units(unit,number):
	pass
