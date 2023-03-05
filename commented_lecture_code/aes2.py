from sage.all import *
from sage.rings.finite_rings.finite_field_givaro import FiniteField_givaro # Givaro = C++ algebra / finite field library

# polynomial ring over the integers
Z = ZZ['x']
x = Z.gen() # x


class HexField(FiniteField_givaro):

    def __init__(self, q, name='t', modulus='None', repr='poly', cache=False) -> None:
        """
        Simply calls the constructor of FiniteField_givaro but with default values, and it caches p and e where q = p^e
        """
        fc = list(factor(q))
        self.p = fc[0][0]
        self.e = fc[0][1]
        if modulus == 'None':
            modulus = GF(q, name).polynomial()
        super().__init__(q, name, modulus, repr, cache)
    
    def c(self, hx):
        """
        cast hex string into self; e.g.: F256.c('0f') == t^3 + t^2 + t + 1   and   F256.c('f0') == t^7 + t^6 + t^5 + t^4
        """
        return self(Integer(hx,16).bits()) # IMPORTANT: note that: Integer('f0',16).bits() == [0, 0, 0, 0, 1, 1, 1, 1]
        # type(Integer('f0',16)) == <class 'sage.rings.integer.Integer'>

    def r(self, p):
        """
        represent as hex string; e.g.: F256.r(15) == '0f'
        """
        return format(Z(p)(2), f'0{self.e//4}x')
        # for x in range(256): assert(Z(x)(2) == Z(x))
        # f'0{F256.e//4}x' == '02x'
        # format(128, '03x') == '080'


F256 = HexField(256, modulus=x**8+x**4+x**3+x+1) # = Rijndael-Polynom
t = F256.gen() # t

# The truncated polynomial ring of length 8
Tpr = Z.quotient(x**8+1) # Im TPR gilt: x^8 + 1 = 0 d.h. x^8 = 1 Zum Beispiel ist dann einfach x^9 = x, das Rechnen (insb. *) ist so kinderleicht.

# tpr_to_f256() und f256_to_tpr() werden lediglich für die sbox() benötigt (da wir für diese keine Lookup-Tabelle verwenden):

def tpr_to_f256(k):
    """
                            F256.c('0f')   == t^3 + t^2 + t + 1
                f256_to_tpr(F256.c('0f'))  == xbar^3 + xbar^2 + xbar + 1
    tpr_to_f256(f256_to_tpr(F256.c('0f'))) == t^3 + t^2 + t + 1
    """
    return F256(k.lift())

def f256_to_tpr(a): # f256_to_tpr(F256.c('0f')) == xbar^3 + xbar^2 + xbar + 1
    return Tpr(Z(a)) # f256_to_tpr(F256.c('f0')) == xbar^7 + xbar^6 + xbar^5 + xbar^4 # d.h. simples Uminterpretieren des Polynoms

Status = MatrixSpace(F256,4,4) # AES-Status = 4*4*8 bit = 128 bit; sehe als 4x4-Matrix mit Elementen aus GF(2^8)=GF(256)=F256

# sage sees matrices row-wise, we need them column-wise, therefore: transpose
def hex_to_status(h):
    """
    sage: hex_to_status('00' * 16)
    [0 0 0 0]
    [0 0 0 0]
    [0 0 0 0]
    [0 0 0 0]
    sage: hex_to_status('01' * 16)
    [1 1 1 1]
    [1 1 1 1]
    [1 1 1 1]
    [1 1 1 1]
    sage: hex_to_status('02' * 16)
    [t t t t]
    [t t t t]
    [t t t t]
    [t t t t]
    sage: hex_to_status('00' * 4 + '01' * 4 + '02' * 4 + '03' * 4)
    [    0     1     t t + 1]
    [    0     1     t t + 1]
    [    0     1     t t + 1]
    [    0     1     t t + 1]
    """
    return Status([F256.c(h[2*i:2*i+2]) for i in range(len(h)//2)]).transpose() # erstellt eine 4x4-F256-Matrix und transponiert sie
    # h = '0123456789'
    # [h[2*i:2*i+2] for i in range(len(h)//2)] == ['01', '23', '45', '67', '89']
    # [F256.c(h[2*i:2*i+2]) for i in range(len(h)//2)] == [1, t^5 + t + 1, t^6 + t^2 + 1, t^6 + t^5 + t^2 + t + 1, t^7 + t^3 + 1]

double_index = cartesian_product([range(4), range(4)]) # list(cartesian_product([[1,2], ['a', 'b']])) == [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
# double_index == The Cartesian product of ({0, 1, 2, 3}, {0, 1, 2, 3})
# list(double_index) == [(0, 0), (0, 1), (0, 2), ..., (3, 2), (3, 3)]

def status_to_hex(m):
    """
    status_to_hex(hex_to_status('02' * 16)) == '02020202020202020202020202020202'
    """
    return ''.join([F256.r(m[j,i]) for i , j in double_index])

# The SBOX
def sbox(p):
    """
    operates on bytes as elements of F256
    """
    return tpr_to_f256(f256_to_tpr(F256.c('1F')) * f256_to_tpr(p**254) + f256_to_tpr(F256.c('63')))

# SubBytes
def sub_bytes(m):
    ret = Status(0)
    for i , j in double_index:
        ret[i,j] = sbox(m[i,j])
    return ret

# ShiftRows
def shift_rows(m):
    """
    sage: [(i, (j+i)%4) for i, j in double_index]
    [(0, 0), (0, 1), (0, 2), (0, 3),
     (1, 1), (1, 2), (1, 3), (1, 0),
     (2, 2), (2, 3), (2, 0), (2, 1),
     (3, 3), (3, 0), (3, 1), (3, 2)]
    """
    u = matrix(F256,4,4)
    for i, j in double_index:
        u[i,j] = m[i, (j+i)%4]
    return u

# This is the matrix C, aka c(s) => used for MixColumns!
U = matrix(F256,4,4)
for i in range(4):
    U[i,i] = F256.c('02') # Tatsächlich: auf der Diagonale sind überall Zweien!
    U[i, (i+1)%4] = F256.c('03')
    U[i, (i+2)%4] = F256.c('01')
    U[i, (i+3)%4] = F256.c('01')
    # In jeder Zeile und in jeder Spalte steht genau einmal 02, einmal 03 und zweimal 01 und die Eisen dabei nebeneinander!
    # Die 03 steht dabei immer rechts von der 02 !!!!!
# sage: U
# [    t t + 1     1     1]
# [    1     t t + 1     1]
# [    1     1     t t + 1]
# [t + 1     1     1     t]
# => genau wie auf dem Cheat Sheet!

# MixColumns
def mix_columns(m):
    return U*m
    # Man beachte dass bei der Multiplikation einer Matrix mit einer anderern Matrix im Grunde die linke Matrix
    # einzeln auf jede Spalte der rechten Matrix angewandt wird! (denke an 3Blue1Brown und die Basisvektoren)

# key derivation
# attention: we number the round from 0 to 9
def next_key(m, r): # m = k[r] = r-ter Rundenschlüssel; r in range(10) = 0 bis 9
    uv = matrix(F256,4,4)

    # Spalte1 = Spalte1 + R[i](Spalte4) = Spalte1 + Rcon(SubWord(RotWord(Spalte4))):
    uv[0,0] = m[0,0] + sbox(m[1,3]) + t**(r) # ...wobei rcon[i] = [rc[i], 00, 00, 00]
    uv[1,0] = m[1,0] + sbox(m[2,3])
    uv[2,0] = m[2,0] + sbox(m[3,3])
    uv[3,0] = m[3,0] + sbox(m[0,3])

    for j in range(1,4):
        for i in range(4):
            uv[i,j] = m[i,j] + uv[i,j-1]
    return uv # = k[r+1] = (r+1)-ter Rundenschlüssel


def aes_key_scheduler(m):
    """
    sage: [status_to_hex(round_key) for round_key in aes_key_scheduler(hex_to_status('00' * 16))]
    ['00000000000000000000000000000000',
     '62636363626363636263636362636363',
     '9b9898c9f9fbfbaa9b9898c9f9fbfbaa',
     '90973450696ccffaf2f457330b0fac99',
     'ee06da7b876a1581759e42b27e91ee2b',
     '7f2e2b88f8443e098dda7cbbf34b9290',
     'ec614b851425758c99ff09376ab49ba7',
     '217517873550620bacaf6b3cc61bf09b',
     '0ef903333ba9613897060a04511dfa9f',
     'b1d4d8e28a7db9da1d7bb3de4c664941',
     'b4ef5bcb3e92e21123e951cf6f8f188e']

    = [k[0], ..., k[10]]

    = cool!
    """
    keys = []
    keys.append(m)
    kn = m
    for i in range(10):
        kn = next_key(kn,i)
        keys.append(kn)
    return keys

def full_round(m,k): # m = Status, k = Rundenschlüssel
    return mix_columns(shift_rows(sub_bytes(m)))+k

def last_round(m,k): # "Schlussrunde"; m = Status, k = Rundenschlüssel
    return shift_rows(sub_bytes(m))+k

def aes(m,k):
    """
    sage: [status_to_hex(status) for status in aes(hex_to_status('00' * 16), hex_to_status('00' * 16))[0]]
    ['00000000000000000000000000000000',  # message m
     '00000000000000000000000000000000',  # message m + key k[0] = message m + key k da k[0] = k
     '01000000010000000100000001000000',  # nach 1. Runde (nutzt k[1])
     'c6e4e48ba48787e8c6e4e48ba48787e8',  # nach 2. Runde
     '282df3c46af386254a4e90a70890e546',  # nach 3. Runde
     'abd2cdfe375ab54950a0afc0759a6a5f',  # nach 4. Runde
     'd46f4f6c55b896337e05bb3d7979de23',  # nach 5. Runde
     '04f2ca9707782845e22f019649c5d710',  # nach 6. Runde
     'b7aae4c51d252d4f6c920f8194e58150',  # nach 7. Runde
     '23e78c3c132163dbaac0c6572e03cb95',  # nach 8. Runde
     '7ffe0e9551a566350e347c472929eccb',  # nach 9. Runde
     '66e94bd4ef8a2c3b884cfa59ca342b2e']  # nach Schlussrunde / 10. Runde (nutzt k[10])
    """
    s = [m, m+k]
    keys = aes_key_scheduler(k)
    for i in range(1,10):
        s.append(full_round(s[len(s)-1], keys[i]))
    s.append(last_round(s[len(s)-1], keys[10])) # Schlussrunde / 10. Runde (nutzt k[10])
    return s, keys # Gebe alle Zwischenergebnisse sowie Rundenschlüssel zurück.

pt = '6bc1bee22e409f96e93d7e117393172a' # pt = "Plaintext"
ky = '2b7e151628aed2a6abf7158809cf4f3c' # ky = "Key"

pt = '00112233445566778899aabbccddeeff' # pt = "Plaintext" # cf. https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf (page 39)
ky = '000102030405060708090a0b0c0d0e0f' # ky = "Key"       # cf. https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf (page 39)

ptm = hex_to_status(pt) # ptm = "Plaintext Matrix", i.e., status
kym = hex_to_status(ky) # kym = "Key Matrix", i.e., status
test, keys = aes(ptm, kym) # Führe AES aus, aes() gibt alle Zwischenergebnisse sowie Rundenschlüssel zurück.

# test ud keys werden nun schön ausgegeben/geprintet:

def pp(m): # pp = "Pretty Print"
    return status_to_hex(m)


print('Zwischen-Ergebnisse nach jeder Runde:')
for g in test:
    print(pp(g))
print('\n')
print('Runden-Schluessel:')
for k in keys:
    print(pp(k))

