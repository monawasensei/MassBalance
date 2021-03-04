import units
import sys

def main():
	n01 = units.node("node_01")
	n02 = units.node("node_02")
	n02a = units.node("node_02a")
	n03 = units.node("node_03")
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

	sys01 = units.system("overall")
	for unit in sys01.contents:
		print(unit.name)
#	for stream in sys01.i:
#		print(stream.name)
#	for stream in sys01.o:
#		print(stream.name)

main()
