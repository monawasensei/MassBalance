import units

def main():
	n01 = units.node("node_01")
	s01 = units.stream("stream_01")
	s02 = units.stream("stream_02")
	s03 = units.stream("stream_03")

	n01.i = [s01,s02]
	n01.o = [s03]

	units.make_all_connections()

	units.print_all_connections()
main()
