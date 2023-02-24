def bbs(p, q, s0, L):
	"""
	Examples:

	sage: load("/Users/kendrick/Github_k-gruenberg/crypto2_code/bbs.py")

	sage: bbs(p=3, q=7, s0=5, L=4)
	p=3 and q=7 private, n = p*q = 21 public.
	s0=5 -> [4, 16, 4, 16]
	BBS_4(5) = [0, 0, 0, 0]

	sage: bbs(p=3, q=7, s0=1, L=4)
	p=3 and q=7 private, n = p*q = 21 public.
	s0=1 -> [1, 1, 1, 1]
	BBS_4(1) = [1, 1, 1, 1]

	sage: bbs(p=5, q=7, s0=5, L=4)
	Error: p=5 != 3 (mod 4)

	sage: bbs(p=7, q=11, s0=64, L=20) # https://de.wikipedia.org/wiki/Blum-Blum-Shub-Generator#Symmetrisches_Kryptosystem "Zunächst wird der BBS-Generator zur Umsetzung einer Stromchiffre verwendet."
	p=7 and q=11 private, n = p*q = 77 public.
	s0=64 -> [15, 71, 36, 64, 15, 71, 36, 64, 15, 71, 36, 64, 15, 71, 36, 64, 15, 71, 36, 64]
	BBS_20(64) = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]

	sage: bbs(p=1000, q=2000, s0=64, L=20)
	Error: p=1000 is not prime!

	sage: next_prime(1000)
	1009
	sage: next_prime(2000)
	2003
	sage: bbs(p=1009, q=2003, s0=64, L=20)
	Error: p=1009 != 3 (mod 4)
	sage: next_prime(1009)
	1013
	sage: bbs(p=1013, q=2003, s0=64, L=20)
	Error: p=1013 != 3 (mod 4) 
	sage: next_prime(1013)
	1019
	sage: bbs(p=1019, q=2003, s0=64, L=20)
	p=1019 and q=2003 private, n = p*q = 2041057 public.
	s0=64 -> [4096, 448760, 566581, 666715, 1374594, 147086, 1128253, 648591, 273353, 806896, 300272, 1622066, 104454, 1188451, 253287, 1841802, 1955318, 1329864, 1148079, 1395496]
	BBS_20(64) = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0]
	"""

	n = p * q

	if not is_prime(p):
		print(f"Error: p={p} is not prime!")
		return
	if not is_prime(q):
		print(f"Error: q={q} is not prime!")
		return
	if p % 4 != 3:
		print(f"Error: p={p} != 3 (mod 4)")
		return
	if q % 4 != 3:
		print(f"Error: q={q} != 3 (mod 4)")
		return
	if gcd(s0, n) != 1: # Zn* = Restklassen der zu n teilerfremden Zahlen
		print(f"Error: s0={s0} is not in Zn* (n={n}) as gcd(s0, n) == {gcd(s0, n)} != 1")
		return

	print(f"p={p} and q={q} private, n = p*q = {n} public.")

	random_numbers = [s0]
	for i in range(1, L+1): # Append s1 to sL to the list:
		random_numbers.append((random_numbers[-1]**2) % n)
	print(f"s0={s0} -> {random_numbers[1:]}")

	random_bits = [random_number % 2 for random_number in random_numbers[1:]]
	print(f"BBS_{L}({s0}) = {random_bits}") # BBS_L(s0) = (b1, b2, ..., bL)

	#return (random_numbers, random_bits)
