

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
	def __init__(self,name,flowRate = "unknown", flowType = "mass", flowUnits = "kg/hr", temperature = 25, tempUnits = "C", pressure = 1, pressUnits = "atm"):
		self.name = name
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

	def get_all_downstream_units(self,downstreamUnitList = ["init"]):
		allDownstreamUnits = list()
		allDownstreamUnits = self.get_downstream_units(downstreamUnitList)
		return allDownstreamUnits

	def get_all_upstream_units(self,upstreamUnitList = ["init"]):
		allUpstreamUnits = list()
		allUpstreamUnits = self.get_upstream_units(upstreamUnitList)
		return allUpstreamUnits

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

	def specify_component_identities(self,componentList):
		self.componentIdentities = componentList
	def specify_component_fractions(self,componentList = [], componentFraction):
		if len(componentList) == 0:
			if len(self.componentIdentities) == 0:
				return 0
			else:
				componentList = self.componentIdentities
		if self.check_componentList_and_values(componentList,componentFraction) != 1:
			return 0
	def specify_component_flow_rates(self,componentList = [],componentFlowRate):
		pass

	def check_componentList_and_values(self,componentList,values):
		if len(componentList) != len(values):
			return 0
		else:
			return 1


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
	def __init__(self,name):
		self.name = name
#############################################################################################################################################################
###############################################################################################################################################################
class component(material): #will be a specific representation of a material per unit
	def __init__(self,parentUnit,name,fractionType = "unknown",fractionValue = "unknown"):
		material.__init__(self,name)
		self.fractionType = fractionType #
		self.fractionValue = fractionValue #
		self.get_unit_attr(parentUnit)

	def get_stream_attr(self,unit):
		self.flowType = unit.flowType
		self.flowRate = unit.flowRate
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
