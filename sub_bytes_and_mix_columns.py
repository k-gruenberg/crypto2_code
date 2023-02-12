"""
Integer to bit array.

E.g.: 0x1F => [0, 0, 0, 1, 1, 1, 1, 1]

Source: https://stackoverflow.com/questions/10321978/integer-to-bitfield-as-a-list
"""
def bits(n):
	bits_ = [int(digit) for digit in bin(n)[2:]] # [2:] to chop off the "0b" part
	result = ([0] * (8 - len(bits_))) + bits_
	result = list(reversed(result))
	return result

"""
Bit array to integer.

E.g.: [0, 0, 0, 1, 1, 1, 1, 1] => 0x1F
"""
def to_byte(bits_):
	bits_ = list(reversed(bits_))
	return ZZ(bits_[0]) * 128 + ZZ(bits_[1]) * 64 + ZZ(bits_[2]) * 32 + ZZ(bits_[3]) * 16 + ZZ(bits_[4]) * 8 + ZZ(bits_[5]) * 4 + ZZ(bits_[6]) * 2 + ZZ(bits_[7])

F256 = PolynomialRing(GF(2),t).quotient_ring(t**8 + t**4 + t**3 + t + 1) # https://en.wikipedia.org/wiki/Finite_field_arithmetic#Rijndael's_(AES)_finite_field
Z = ZZ['x']
TPR = Z.quotient(x**8+1)

"""
Compare results to those on:

https://en.wikipedia.org/wiki/Rijndael_S-box
"""
def sub_byte(byte):        # sub_byte(0x00)              # sub_byte(0x03)
	#result = TPR(Z(F256(bits(0x1F)))) * TPR(Z(F256(bits(byte))**254)) + TPR(Z(F256(bits(0x63)))) # Def. SubBytes: b -> 1F * b^254 + 63 (Achtung: Invertieren im F256, Multiplizieren im TPR!!!)
	result = TPR(bits(0x1F)) * TPR((F256(bits(byte))**254).list()) + TPR(bits(0x63))
	result = F256(result.lift())
	print(result)          # tbar^6 + tbar^5 + tbar + 1  # tbar^6 + tbar^5 + tbar^4 + tbar^3 + tbar + 1
	l = result.list()
	print(l)               # [1, 1, 0, 0, 0, 1, 1, 0]    # [1, 1, 0, 1, 1, 1, 1, 0]
	print(to_byte(l))      # 99                          # 123
	return hex(to_byte(l)) # '0x63'                      # '0x7b'

def mix_column(column):                     # mix_column([0x01, 0x01, 0x01, 0x01]) # mix_column([0xDB, 0x13, 0x53, 0x45])
	[b0, b1, b2, b3] = column
	result = [
		F256(bits(0x02)) * F256(bits(b0)) + F256(bits(0x03)) * F256(bits(b1)) + F256(bits(0x01)) * F256(bits(b2)) + F256(bits(0x01)) * F256(bits(b3)),
		F256(bits(0x01)) * F256(bits(b0)) + F256(bits(0x02)) * F256(bits(b1)) + F256(bits(0x03)) * F256(bits(b2)) + F256(bits(0x01)) * F256(bits(b3)),
		F256(bits(0x01)) * F256(bits(b0)) + F256(bits(0x01)) * F256(bits(b1)) + F256(bits(0x02)) * F256(bits(b2)) + F256(bits(0x03)) * F256(bits(b3)),
		F256(bits(0x03)) * F256(bits(b0)) + F256(bits(0x01)) * F256(bits(b1)) + F256(bits(0x01)) * F256(bits(b2)) + F256(bits(0x02)) * F256(bits(b3))
	]
	print(result)                           # [1, 1, 1, 1]                         # [tbar^7 + tbar^3 + tbar^2 + tbar, tbar^6 + tbar^3 + tbar^2 + 1, tbar^7 + tbar^5 + 1, tbar^7 + tbar^5 + tbar^4 + tbar^3 + tbar^2]
	result = [to_byte(value.list()) for value in result]
	print(result)                           # [1, 1, 1, 1]                         # [142, 77, 161, 188]
	return [hex(value) for value in result] # ['0x1', '0x1', '0x1', '0x1']         # ['0x8e', '0x4d', '0xa1', '0xbc']
