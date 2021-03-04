import units
import sys

def main():
	n01 = units.node("node_01")
	n02 = units.node("node_02")
	n02a = units.node("node_02a")
	n03 = units.node("node_03")
	s01 = units.stream("stream_01")
	s02 = units.stream("stream_02")
	s03 = units.stream("stream_03")
	s03a = units.stream("stream_03a")
	s04 = units.stream("stream_04")
	s04a = units.stream("stream_04a")
	s05 = units.stream("stream_05")


	n01.specify_connections([s01,s02],[s03,s03a])
	n02.specify_connections([s03],[s04])
	n03.specify_connections([s04,s04a],[s05])
	n02a.specify_connections([s03a],[s04a])

	units.make_all_connections()
	units.print_all_connections()

	listTest = s01.get_all_downstream_units()
	for unit in listTest:
		print(unit)

main()
