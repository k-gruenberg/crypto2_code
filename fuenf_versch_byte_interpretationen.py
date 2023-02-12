def addiere_zwei_bytes(byte1, byte2):
	print("(1) 8-dim. VR über GF(2)")
	vector1 = vector(GF(2), byte1)
	vector2 = vector(GF(2), byte2)
	vector_sum = vector1 + vector2
	print(f"\t{vector1} + {vector2} -> {vector_sum}")

	n1_big_endian = bit_vector_to_number_big_endian(byte1)
	n1_little_endian = bit_vector_to_number_little_endian(byte1)
	n2_big_endian = bit_vector_to_number_big_endian(byte2)
	n2_little_endian = bit_vector_to_number_little_endian(byte2)
	print("(2) (Z256, +) Big Endian")
	print(f"\t{Zmod(256)(n1_big_endian)} + {Zmod(256)(n2_big_endian)} == {Zmod(256)(n1_big_endian) + Zmod(256)(n2_big_endian)} <-> {number_to_bit_vector(True, Zmod(256)(n1_big_endian) + Zmod(256)(n2_big_endian))}")
	print("(2) (Z256, +) Little Endian")
	print(f"\t{Zmod(256)(n1_little_endian)} + {Zmod(256)(n2_little_endian)} == {Zmod(256)(n1_little_endian) + Zmod(256)(n2_little_endian)} <-> {number_to_bit_vector(False, Zmod(256)(n1_little_endian) + Zmod(256)(n2_little_endian))}")
	print("(3) (Z257*, *) Big Endian")
	print(f"\t{Zmod(257)(n1_big_endian)} * {Zmod(257)(n2_big_endian)} == {Zmod(257)(n1_big_endian) * Zmod(257)(n2_big_endian)} <-> {number_to_bit_vector(True, Zmod(257)(n1_big_endian) * Zmod(257)(n2_big_endian))}")
	print("(3) (Z257*, *) Little Endian")
	print(f"\t{Zmod(257)(n1_little_endian)} * {Zmod(257)(n2_little_endian)} == {Zmod(257)(n1_little_endian) * Zmod(257)(n2_little_endian)} <-> {number_to_bit_vector(False, Zmod(257)(n1_little_endian) * Zmod(257)(n2_little_endian))}")
	
	print("(4) GF(2^8) == GF(2)[t] / <t^8 + t^4 + t^3 + t + 1> (Rijndael-Polynom)")
	var('t')
	R4 = PolynomialRing(GF(2),t).quotient_ring(t**8 + t**4 + t**3 + t + 1)
	a = R4(byte1)
	b = R4(byte2)
	print(f"\t[{a}] + [{b}] -> {a + b} <-> {(a + b).list()}")
	print(f"\t[{a}] * [{b}] -> {a * b} <-> {(a * b).list()}")
	print("(5) GF(2)[t] / <t^8 - 1> (Truncated Polynomial Ring)")
	R5 = PolynomialRing(GF(2),t).quotient_ring(t**8 + 1)
	a = R5(byte1)
	b = R5(byte2)
	print(f"\t[{a}] + [{b}] -> {a + b} <-> {(a + b).list()}")
	print(f"\t[{a}] * [{b}] -> {a * b} <-> {(a * b).list()}")

def addiere_zwei_bytes_gegeben_als_zahlen(byte1, byte2):
	for big_endian in [False, True]:
		print("===== Big Endian: =====" if big_endian else "===== Little Endian: =====")

		byte1_as_bit_vector = number_to_bit_vector(big_endian, byte1)
		byte2_as_bit_vector = number_to_bit_vector(big_endian, byte2)

		print("(1) 8-dim. VR über GF(2)")
		vector1 = vector(GF(2), byte1_as_bit_vector)
		vector2 = vector(GF(2), byte2_as_bit_vector)
		vector_sum = vector1 + vector2
		print(f"\t{vector1} + {vector2} -> {vector_sum} <-> {bit_vector_to_number(big_endian, vector_sum)}")
		print("(2) (Z256, +)")
		print(f"\t{Zmod(256)(byte1)} + {Zmod(256)(byte2)} == {Zmod(256)(byte1) + Zmod(256)(byte2)} <-> {number_to_bit_vector(big_endian, Zmod(256)(byte1) + Zmod(256)(byte2))}")
		print("(3) (Z257*, *)")
		print(f"\t{Zmod(257)(byte1)} * {Zmod(257)(byte2)} == {Zmod(257)(byte1) * Zmod(257)(byte2)} <-> {number_to_bit_vector(big_endian, Zmod(257)(byte1) * Zmod(257)(byte2))}")
		print("(4) GF(2^8) == GF(2)[t] / <t^8 + t^4 + t^3 + t + 1> (Rijndael-Polynom)")
		var('t')
		R4 = PolynomialRing(GF(2),t).quotient_ring(t**8 + t**4 + t**3 + t + 1)
		a = R4(byte1_as_bit_vector)
		b = R4(byte2_as_bit_vector)
		print(f"\t[{a}] + [{b}] -> {a + b} <-> {(a + b).list()} <-> {bit_vector_to_number(big_endian, (a + b).list())}")
		print(f"\t[{a}] * [{b}] -> {a * b} <-> {(a * b).list()} <-> {bit_vector_to_number(big_endian, (a * b).list())}")
		print("(5) GF(2)[t] / <t^8 - 1> (Truncated Polynomial Ring)")
		R5 = PolynomialRing(GF(2),t).quotient_ring(t**8 + 1)
		a = R5(byte1_as_bit_vector)
		b = R5(byte2_as_bit_vector)
		print(f"\t[{a}] + [{b}] -> {a + b} <-> {(a + b).list()} <-> {bit_vector_to_number(big_endian, (a + b).list())}")
		print(f"\t[{a}] * [{b}] -> {a * b} <-> {(a * b).list()} <-> {bit_vector_to_number(big_endian, (a * b).list())}")

		print("")
		print("")

def number_to_bit_vector(big_endian, n):
	if big_endian:
		return number_to_bit_vector_big_endian(n)
	else:
		return number_to_bit_vector_little_endian(n)

def bit_vector_to_number(big_endian, n):
	if big_endian:
		return bit_vector_to_number_big_endian(n)
	else:
		return bit_vector_to_number_little_endian(n)

def number_to_bit_vector_big_endian(n):
	n = ZZ(n)
	return [(n//128) % 2, (n//64) % 2, (n//32) % 2, (n//16) % 2, (n//8) % 2, (n//4) % 2, (n//2) % 2, n % 2]

def bit_vector_to_number_big_endian(vec):
	return ZZ(vec[0]) * 128 + ZZ(vec[1]) * 64 + ZZ(vec[2]) * 32 + ZZ(vec[3]) * 16 + ZZ(vec[4]) * 8 + ZZ(vec[5]) * 4 + ZZ(vec[6]) * 2 + ZZ(vec[7])

def number_to_bit_vector_little_endian(n):
	n = ZZ(n)
	return [n % 2, (n//2) % 2, (n//4) % 2, (n//8) % 2, (n//16) % 2, (n//32) % 2, (n//64) % 2, (n//128) % 2]

def bit_vector_to_number_little_endian(vec):
	return ZZ(vec[0]) + ZZ(vec[1]) * 2 + ZZ(vec[2]) * 4 + ZZ(vec[3]) * 8 + ZZ(vec[4]) * 16 + ZZ(vec[5]) * 32 + ZZ(vec[6]) * 64 + ZZ(vec[7]) * 128
