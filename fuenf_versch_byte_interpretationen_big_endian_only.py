def addiere_zwei_bytes(byte1, byte2):
	byte1_as_bit_vector = number_to_bit_vector(byte1)
	byte2_as_bit_vector = number_to_bit_vector(byte2)

	print("(1) 8-dim. VR über GF(2)")
	print(f"\t{vector(GF(2), byte1_as_bit_vector)} + {vector(GF(2), byte2_as_bit_vector)} -> {vector(GF(2), byte1_as_bit_vector) + vector(GF(2), byte2_as_bit_vector)}")
	print("(2) (Z256, +)")
	print(f"\t{Zmod(256)(byte1)} + {Zmod(256)(byte2)} == {Zmod(256)(byte1) + Zmod(256)(byte2)} <-> {number_to_bit_vector(Zmod(256)(byte1) + Zmod(256)(byte2))}")
	print("(3) (Z257*, -)")
	print(f"\t{Zmod(257)(byte1)} * {Zmod(257)(byte2)} == {Zmod(257)(byte1) * Zmod(257)(byte2)} <-> {number_to_bit_vector(Zmod(257)(byte1) * Zmod(257)(byte2))}")
	print("(4) GF(2^8) == GF(2)[t] / <t^8 + t^4 + t^3 + t + 1> (Rijndael-Polynom)")
	var('t')
	R4 = PolynomialRing(GF(2),t).quotient_ring(t**8 + t**4 + t**3 + t + 1)
	a = R4(byte1_as_bit_vector)
	b = R4(byte2_as_bit_vector)
	print(f"\t[{a}] + [{b}] -> {a + b} <-> {(a + b).list()} <-> {bit_vector_to_number((a + b).list())}")
	print(f"\t[{a}] * [{b}] -> {a * b} <-> {(a * b).list()} <-> {bit_vector_to_number((a * b).list())}")
	print("(5) GF(2) / <t^8 - 1> (Truncated Polynomial Ring)")
	R5 = PolynomialRing(GF(2),t).quotient_ring(t**8 + 1)
	a = R5(byte1_as_bit_vector)
	b = R5(byte2_as_bit_vector)
	print(f"\t[{a}] + [{b}] -> {a + b} <-> {(a + b).list()} <-> {bit_vector_to_number((a + b).list())}")
	print(f"\t[{a}] * [{b}] -> {a * b} <-> {(a * b).list()} <-> {bit_vector_to_number((a * b).list())}")

def number_to_bit_vector(n):
	n = ZZ(n)
	return [(n//128) % 2, (n//64) % 2, (n//32) % 2, (n//16) % 2, (n//8) % 2, (n//4) % 2, (n//2) % 2, n % 2]

def bit_vector_to_number(vec):
	return ZZ(vec[0]) * 128 + ZZ(vec[1]) * 64 + ZZ(vec[2]) * 32 + ZZ(vec[3]) * 16 + ZZ(vec[4]) * 8 + ZZ(vec[5]) * 4 + ZZ(vec[6]) * 2 + ZZ(vec[7])
