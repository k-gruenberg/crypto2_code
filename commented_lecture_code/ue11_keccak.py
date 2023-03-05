"""

"""
from sage.all import *

hexn = '0123456789ABCDEF'

B = GF(2) # = {0, 1} = ein Bit


class State:
    def __init__(self):
        self.s = [B.zero() for i in range(1600)] # Ein Keccak-Status besteht aus 5*5*64=1600 Bits und ist initial mit Nullen gefüllt.

    def set(self, x, y, z, b):
        """
        Interpretiere diesen 1600-Bit-Status als 3-dimensionale 5*5*64-Matrix und setzte das Bit an der Koordinate (x,y,z).
        """
        self.s[(x + 5 * y) * 64 + z] = b

    def get(self, x, y, z):
        """
        Interpretiere diesen 1600-Bit-Status als 3-dimensionale 5*5*64-Matrix und retrieve das Bit an der Koordinate (x,y,z).
        """
        return self.s[(x + 5 * y) * 64 + z]

    def clone(self):
        ret = State()
        for x in range(5):
            for y in range(5):
                for z in range(64):
                    ret.set(x, y, z, self.s[(x + 5 * y) * 64 + z]) # Code Copy & Paste, anstatt einfach get() aufzurufen...
        return ret

    def put_bitstring(self, bit_string): # e.g. A = State() and A.put_bitstring('11000101'*72 + '0'*(1600-72*8))
        for x in range(5):
            for y in range(5):
                for z in range(64):
                    self.set(x, y, z, int(bit_string[(x + 5 * y) * 64 + z]) * B(1))

    def get_bitstring(self):
        """
        sage: A = State()
        sage: A.get_bitstring()
        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         0000000000000000000000000000000000000000000000'
        sage: len(A.get_bitstring())
        1600

        => Status = 1600 Bit = 200 Byte
        """
        return ''.join([str(self.s[(x + 5 * y) * 64 + z]) for y in range(5) for x in range(5) for z in range(64)])


def i2bs(n, sz):
    """
    Integer to bitstring:
    i2bs(15, 8) == '11110000'
    """
    ret = []
    for i in range(sz):
        ret.append(str(n % 2))
        n = n // 2
    return ''.join(ret)


def i2hx(n):
    """
    Integer to hex string:
    i2hx(15) == '0F'
    """
    return hexn[n // 16] + hexn[n % 16]


def h2b(h, n=0): # (never used)
    """
    :param h: hexadecimal string consisting of 2m digits for some positive integer m
    :param n: positive integer such that n ≤ 8m
    :return: bit string s, such that len(s) = n

    Turns a hexadecimal string into a binary string.

    Examples:
    h2b('FF') == '11111111'
    h2b('0F') == '11110000'
    """
    m = len(h) // 2
    ret = ''
    for i in range(m):
        bi = 16 * int(h[2 * i], 16) + int(h[2 * i + 1], 16)
        ret = ret + i2bs(bi, 8)
    return ret


def b2h(s):
    """
    :param s: a binary string of size 8m
    :return: a hexadecimal string of size 2*m
    
    Turns a binary string into a hexadecimal string.

    Example:
    b2h('11000101'*72 + '0'*(1600-72*8)) ==
    'A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A3A
    3A3A3A3A3A3A3A3A3A3A3A3A3A3A3000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    00000000000000000000000000000000000000000000000000000'
    """
    m = len(s) // 8
    ret = ''
    for i in range(m):
        hi = sum([int(s[8 * i + j]) * 2 ** j for j in range(8)])
        ret = ret + i2hx(hi)
    return ret


def pprint(hxs):
    """
    sage: pprint('ABCDEF')
    AB CD EF

    sage: pprint(b2h('11000101'*72 + '0'*(1600-72*8)))
    A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 
    A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 
    A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 
    A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 A3 
    A3 A3 A3 A3 A3 A3 A3 A3 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00
    """
    lh = len(hxs) // 2
    for i in range(lh):
        j = 2 * i
        print(hxs[j:j + 2] + ' ', end='')
        if i > 0 and i % 16 == 15:
            print('')
    print('')

# Achtung: theta(), rho(), pi(), chi() und iota() sind keine Member-Funktionen der State-Klasse, wie man erwarten würde !!!!!

def theta(state: State) -> State:
    c = [[sum([state.get(x, y, z) for y in range(5)]) for z in range(64)] for x in range(5)]
    d = [[c[(x + 4) % 5][z] + c[(x + 1) % 5][(z - 1) % 64] for z in range(64)] for x in range(5)]
    ret = State()
    for x in range(5):
        for y in range(5):
            for z in range(64):
                ret.set(x, y, z, state.get(x, y, z) + d[x][z])
    return ret

# Compare this with the description in the lecture! 
def rho(state: State) -> State:
    ret = State()
    for z in range(64):
        ret.set(0, 0, z, state.get(0, 0, z))
    x, y = 1, 0
    for t in range(24):
        for z in range(64):
            ret.set(x, y, z, state.get(x, y, (z - (t + 1) * (t + 2) // 2) % 64))
        x, y = y, (2 * x + 3 * y) % 5
    return ret


def pi(state):
    ret = State()
    for x in range(5):
        for y in range(5):
            for z in range(64):
                ret.set(x, y, z, state.get((x + 3 * y) % 5, x, z))
    return ret


def chi(state):
    ret = State()
    for x in range(5):
        for y in range(5):
            for z in range(64):
                nv = state.get(x, y, z) + (state.get((x + 1) % 5, y, z) + B(1)) * state.get((x + 2) % 5, y, z)
                ret.set(x, y, z, nv)
    return ret

# Compare this with the description in the lecture! 
def rc(t: int): # => benötigt für iota() !!!!! => könnte man auch in einer Lookup-Tabelle hardcoden!
    """
    This is an exact Python implementation of the pseudo-code in
    https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf (page 16 / PDF page 24):

    Algorithm 5: rc(t)
    Input: integer t
    Output: bit rc(t).

    It is a "linear feedback shift register".

    Die eigentliche Rundenkonstante RC[nr] (für nr=0 bis nr=23, da 24 Runden)
    besteht jedoch aus 8 Byte (64 Bit) und wird wie folgt berechnet, siehe auch iota() sowie mein rr_test():

    rr = [B.zero() for i in range(64)]
    for j in range(6):
        rr[(2 ** j) - 1] = rc(j + 7 * nr)
    """
    if t % 255 == 0:                     # 1. If t mod 255 = 0, return 1.
        return B(1)
    r = '10000000'                       # 2. Let R = 10000000.
    for i in range((t % 255)):           # 3. For i from 1 to t mod 255, let:
        r = '0' + r                      #      a. R = 0 || R;
        rl = list(r)
        rl[0] = str(B(rl[0]) + B(rl[8])) #      b. R[0] = R[0] ⊕ R[8];
        rl[4] = str(B(rl[4]) + B(rl[8])) #      c. R[4] = R[4] ⊕ R[8];
        rl[5] = str(B(rl[5]) + B(rl[8])) #      d. R[5] = R[5] ⊕ R[8];
        rl[6] = str(B(rl[6]) + B(rl[8])) #      e. R[6] = R[6] ⊕ R[8];
        rl = rl[:8]                      #      f. R =Trunc_8[R].
        r = ''.join(rl)
    return B(r[0])                       # 4. Return R[0].


def rr_test(state, nr): # !!!!! ADDED BY ME !!!!!
    """
       [b2h(''.join([str(bit) for bit in rr_test(State(), nr)])) for nr in range(24)] 
    == [b2h(iota(State(), nr).get_bitstring())[0:16]             for nr in range(24)]
    == ['0100000000000000', '8280000000000000', '8A80000000000000', '0080008000000000',
        '8B80000000000000', '0100008000000000', '8180008000000000', '0980000000000000',
        '8A00000000000000', '8800000000000000', '0980008000000000', '0A00008000000000',
        '8B80008000000000', '8B00000000000000', '8980000000000000', '0380000000000000',
        '0280000000000000', '8000000000000000', '0A80000000000000', '0A00008000000000',
        '8180008000000000', '8080000000000000', '0100008000000000', '0880008000000000']
    ACHTUNG: passt nicht so ganz zu den in der Vorlesung angegebenen!
             RC[0] und RC[1] stimmen fast, nur sind die Bytes in der Reihenfolge vertauscht!
             Da da erste "richtige" Fehler erst bei RC[1] auftaucht und wir hier nur Runden 0 und 1 testen,
             ist er vermutlich nicht aufgefallen...
    """
    rr = [B.zero() for i in range(64)]
    for j in range(6):
        rr[(2 ** j) - 1] = rc(j + 7 * nr)
    return rr


def iota(state, nr): # => Iota ist als einziges rundenabhängig!!!!! => daher "nr"-Parameter
    ret = state.clone()
    rr = [B.zero() for i in range(64)]
    for j in range(6):
        rr[(2 ** j) - 1] = rc(j + 7 * nr)
    for z in range(64):
        ret.set(0, 0, z, ret.get(0, 0, z) + rr[z])
    return ret


if __name__ == '__main__':
    A = State()
    #m = '0110000' + ('0' * 568) + '10000000' + '0' * 1024
    ## Input 'A3'*72 + '00'*128
    # ACHTUNG: verkehrt herum lesen! bin(0xA3) == '0b10100011'
    m = '11000101'*72 + '0'*(1600-72*8) # ACHTUNG: Testdaten kommen aus einer "keccak.txt", die er NICHT auf Stud.IP hochgeladen hat!
    # repair put_bitstring!
    A.put_bitstring(m)
    pprint(b2h(m))
    # Round 0
    #print('0 after theta') # Useless print, next line prints nothing!
    A2 = theta(A)
    print('0 after theta')
    pprint(b2h(A2.get_bitstring()))
    A3 = rho(A2)
    print('0 after rho')
    pprint(b2h(A3.get_bitstring()))
    A4 = pi(A3)
    print('0 after pi')
    pprint(b2h(A4.get_bitstring()))
    A5 = chi(A4)
    print('0 after chi')
    pprint(b2h(A5.get_bitstring()))
    A6 = iota(A5, 0)
    print('0 after iota')
    pprint(b2h(A6.get_bitstring()))
    # Round 1
    A7 = theta(A6)
    print('1 after theta')
    pprint(b2h(A7.get_bitstring()))
    A8 = rho(A7)
    print('1 after rho')
    pprint(b2h(A8.get_bitstring()))
    A9 = pi(A8)
    print('1 after pi')
    pprint(b2h(A9.get_bitstring()))
    A10 = chi(A9)
    print('1 after chi')
    pprint(b2h(A10.get_bitstring()))
    A11 = iota(A10, 1)
    print('1 after iota')
    pprint(b2h(A11.get_bitstring()))
