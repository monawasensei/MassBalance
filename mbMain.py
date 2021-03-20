import units
import sys

def main():
	mat1 = units.material("water",18.02)
	mat2 = units.material("ethanol",46.0) #or something I don't remember
	n01 = units.node("node_01")
	n02 = units.node("node_02")
	n02a = units.node("node_02a")
	n03 = units.node("mixer_01")
	n04 = units.node("node_04")
	n05 = units.node("node_05")
	n06 = units.node("node_06")
	n07 = units.node("node_07")
	s01 = units.stream("stream_01")
	s02 = units.stream("stream_02")
	s03 = units.stream("stream_03")
	s03a = units.stream("stream_03a")
	s04 = units.stream("stream_04")
	s04a = units.stream("stream_04a")
	s05 = units.stream("stream_05")
	s06 = units.stream("stream_06")
	s07 = units.stream("stream_07")
	s08 = units.stream("stream_08")
	s09 = units.stream("stream_09")
	s10 = units.stream("stream_10")
	s11 = units.stream("stream_11")

	n01.specify_connections([s01,s02],[s03,s03a])
	n02.specify_connections([s03],[s04])
	n02a.specify_connections([s03a],[s04a,s06])
	n03.specify_connections([s04,s04a],[s05])
	n04.specify_connections([s06],[s07])
	n05.specify_connections([s07],[s08,s09])
	n06.specify_connections([s05],[s10])
	n07.specify_connections([s08,s10],[s11])

	units.make_all_connections()

	#mixerSys = units.system("mixer",[s04,s04a],[s05])
	# print(mixerSys.i)
	# print(mixerSys.o)
	# print(mixerSys.contents)

def testMain():
	n1 = units.node("n1")
	n2 = units.node("n2")
	n3 = units.node("n3")
	n4 = units.node("n4")
	n5 = units.node("n5")
	n6 = units.node("n6")
	n7 = units.node("n7")
	n8 = units.node("n8")
	n9 = units.node("n9")
	n10 = units.node("n10")
	n11 = units.node("n11")
	n12 = units.node("n12")
	n13 = units.node("n13")
	n14 = units.node("n14")
	n15 = units.node("n15")
	n16 = units.node("n16")
	n17 = units.node("n17")
	n18 = units.node("n18")
	n19 = units.node("n19")
	n20 = units.node("n20")

	a = units.stream("a")
	b = units.stream("b")
	c = units.stream("c")
	d = units.stream("d")
	e = units.stream("e")
	f = units.stream("f")

	for designation in range(24):
		#str("s" + str(designation)) = units.stream(str(designation))
		pass

	n1.specify_connections([a],[s1])
	n2.specify_connections([s1],[s2])
	n3.specify_connections([b,s2],[s3,s6])
	n4.specify_connections([c,s3],[s4])
	n5.specify_connections([s6],[s7,s8,s9,s10])
	n6.specify_connections([s4],[f,s5])
	n7.specify_connections([s7],[s11])
	n8.specify_connections([s8],[s12])
	n9.specify_connections([s9],[s13])
	n10.specify_connections([s10],[s14])
	n11.specify_connections([s11,s12,s13,s14],[s15])
	n12.specify_connections([s15,s24],[s16])
	n13.specify_connections([s16,s5],[s17])
	n14.specify_connections([s17],[s18])
	n15.specify_connections([s18],[s19,s21])
	n16.specify_connections([s19],[s20])
	n17.specify_connections([s20],[e])
	n18.specify_connections([s21],[d,s22])
	n19.specify_connections([s22],[s23])
	n20.specify_connections([s23],[s24])

	units.make_all_connections()
	overall = units.system("overall")
	print(overall.contents)


def smol_main():
	mat1 = units.material("water", 18.02)
	mat2 = units.material("ethanol", 46.0)  # or something I don't remember
	n01 = units.node("n01")
	n01.specify_component_fractions(["water","ethanol"],"mass",[0.25,0.75])
	n01.specify_component_flow_rates(["water","ethanol"],"mass",[400,1200])
	n02 = units.node("n02")
	s01 = units.stream("s01")
	s02 = units.stream("s02")
	s03 = units.stream("s03")

	n01.specify_connections([s01],[s02])
	n02.specify_connections([s02],[s03])

	units.make_all_connections()

	for thing in n01.componentIdentities:
		print(thing.name + "_" + str(thing.fractionValue) + "_" + str(thing.flowRate))
	print(type(n01))

def DoF_test():
	mat1 = units.material("A",20)
	mat2 = units.material("B",45)
	n01 = units.node("n01")
	s01 = units.stream("s01")
	s02 = units.stream("s02")

	n01.specify_connections([s01],[s02])
	units.make_all_connections()
	units.print_all_connections()

	s01.specify_component_fractions(["A","B"],"mass",[None,0.40]) #will have to see how passing "None" will work :/
	s02.specify_component_fractions(["A","B"],"mass",[0.80,None])
	s01.flowRate = 500
	s02.flowRate = None

	sys01 = units.system("overall")
	tuple = sys01.get_unknown_values()
	print(tuple[0])
	dictKey = ["stream flow rates","component flow rates","component fractions"]
	print(s01.componentIdentities[1].flowRate)
	for i in range(1,4):
		print(dictKey[i-1])
		for thing in tuple[i]:
			print(thing.name)

def DoF_test_two():
	mat1 = units.material("A", 20)
	mat2 = units.material("B", 45)
	mat3 = units.material("C",50)
	mat4 = units.material("D", 15)

	n01 = units.node("n01")
	n02 = units.node("n02")
	n03 = units.node("n03")
	n04 = units.node("n04")
	n05 = units.node("n05")

	s01 = units.stream("stream_01")
	s02 = units.stream("stream_02")
	s03 = units.stream("stream_03")
	s09 = units.stream("stream_09")
	s04 = units.stream("stream_04")
	s10 = units.stream("stream_10")
	s05 = units.stream("stream_05")
	s06 = units.stream("stream_06")
	s07 = units.stream("stream_07")
	s08 = units.stream("stream_08")

	n01.specify_connections([s01,s02],[s03,s04])
	n02.specify_connections([s03,s05],[s06])
	n03.specify_connections([s06],[s08,s09])
	n04.specify_connections([s04],[s07])
	n05.specify_connections([s09],[s10])
	units.make_all_connections()
	units.print_all_connections()

	#I think None should be explicitly defined, but I will have to look into this because I'd rather not have to do that.
	s01.specify_component_fractions([],"mass",[1.0,0,0,0])
	s02.specify_component_fractions([],"mass",[0,1.0,0,0])
	s03.specify_component_fractions([],"mass",[0.25,0.75,0,0])
	s04.specify_component_fractions([],"mass",[0.75,0.25,0,0])
	s05.specify_component_fractions([],"mass",[0,0,1.0,0])
	#s06.specify_component_fractions(["A","B","C","D"],"mass",[None,None,None,None])
	s07.specify_component_fractions(["C","D"],"mass",[0,0])
	s08.specify_component_fractions([],"mass",[0.2,0.2,0.6,0])
	#s09.specify_component_fractions([],"mass",[None,None,None,None])
	#s10.specify_component_fractions([],"mass",[None,None,None,None])
	s01.flowRate = 500
	s02.flowRate = 500
	s03.flowRate = 100
	s06.flowRate = 100
	s10.flowRate = 100

	sys01 = units.system("overall")
	print("sys01 in")
	for thing in sys01.i:
		print("\t" + thing.name)
	print("sys01 out")
	for thing in sys01.o:
		print("\t" + thing.name)
	print("contents")
	for thing in sys01.contents:
		print("\t" + thing.name)
	tuple = sys01.get_unknown_values()
	dictKey = ["stream flow rates", "component flow rates", "component fractions"]
	for i in range(1,4):
		print(dictKey[i-1])
		for thing in tuple[i]:
			print(thing.name)
	print(tuple[0])

def type_test():
	n01 = units.node("n01")
	m01 = units.mixer("m01")
	print(type(n01))
	print(type(m01))
	print(g_o_t_t(m01))

def g_o_t_t(obj):
	if isinstance(obj,units.node):
		if isinstance(obj,units.mixer):
			return "mixer"
		else:
			return "node"
	else:
		return None

type_test()
