from sage.all import *  # "from lib import *" geht bei mir nicht... # Problem: keine "lib.py" im Stud.IP...

# <Teile von lib.py aus Video von UE06 abgetippt:>
b_len = 4

B = VectorSpace(GF(2), b_len)

Sb = [6, 4, 0xc, 5, 0, 7, 2, 0xe, 1, 0xf, 3, 0xd, 8, 0xa, 9, 0xb] # Sb = "S-Box"
Rb = [4, 8, 6, 0xa, 1, 3, 0, 5, 0xc, 0xe, 0xd, 0xf, 2, 0xb, 7, 9] # Rb = "Reverse S-Box" # inv of S

def n2b(x):
    '''
    Transform an integer x0 + 2*x1 + 4*x2 + 8*x3 into the element
    (x3, x2, x1, x0) of B.
    '''
    s = format(x, '04b')
    return B([int(x) for x in s])

def b2n(b):
    '''
    Transform an element of B into an integer.
    (x3, x2, x1, x0) is mapped to x0 + 2*x1 + 4*x2 + 8*x3.
    '''
    bl = b.list()
    bl.reverse()
    return Integer(bl, 2)

def b2nh(b):
    return (b2n(b)).hex() # redundante Klammern...

def a_vec(n):
    if 'Vector' in str(type(n)):
        return n
    else:
        return n2b(n)

def a_num(n):
    if 'Vector' in str(type(n)):
        return b2n(n)
    else:
        return n

def S(b):
    arg = a_num(b)
    return n2b(Sb[arg])

def Sinv(b):
    arg = a_num(b)
    return n2b(Rb[arg])
# </>

def chiffre3(m,k1,k2,k3,k4):
    """
    Wendet Chiffre3 aus VL06 auf die Nachricht m an; unter Verwendung der vier Rundenschlüssel k1, ..., k4.
    Chiffre3 hat *3* S-Boxen, also *4* Rundenschlüssel.

    Gibt ein Tupel (u, v, w, x, y, z, c) zurück, d.h. die eigentliche Rückgabe, der Ciphertext, ist das *letzte* Tupelelement (d.h. lese Rückgabe chronologisch).
    """
    mv = a_vec(m) # mv = "message vector"
    k1v = a_vec(k1) # k1v = "(round) key 1 vector"
    k2v = a_vec(k2) # k2v = "(round) key 2 vector"
    k3v = a_vec(k3) # k3v = "(round) key 3 vector"
    k4v = a_vec(k4) # k4v = "(round) key 4 vector"
    u = mv + k1v # u =  vor der 1. S-Box
    v = S(u)     # v = nach der 1. S-Box
    w = v + k2v  # w =  vor der 2. S-Box
    x = S(w)     # x = nach der 2. S-Box
    y = x + k3v  # y =  vor der 3. S-Box
    z = S(y)     # z = nach der 3. S-Box
    c = z + k4v
    return u, v, w, x, y, z, c




##### Das war Chiffre 3. Nun zum Angriff auf Chiffre 3: #####




# 2-round differential 
din = 0xf  # selbes Beispiel
dout = 0xc # wie in der VL, siehe Cheat Sheet
possible_diffs = [a_vec(1), a_vec(3), a_vec(5), a_vec(8), a_vec(0xe)] # == S(0xc) == set(b2n(S(a) + S(b)) for a in range(16) for b in range(16) if a^^b == 0xc) == {0x1, 0x3, 0x5, 0x8, 0xe} (vgl. vorletzte Folie von VL06)

def algo3(m, k1, k2, k3, k4):
    """ Angriff:
    Nehme ein Paar (m1, m2) - wobei m2 = m1 + 0xf - und lasse den Challenger die Schlüsseltexte (c1, c2) generieren.
    Wenn c1 + c2 in S(0xc) liegt, d.h. wenn a und b mit a^^b == 0xc existieren sodass S(a)+S(b) == S(0xc), dann ist es ein gutes Paar.
    Wir fordern dies, da wir 0xc als Eingabe in die 3./letzte S-Box geraten haben,
      da das 2-Runden-Differential 0xf -S-> ? -S-> 0xc für die S-Box S recht wahrscheinlich ist. 
    Dies wird natürlich nur zum Erfolg führen, wenn tatsächlich "true input difference to the last Sbox: c".

    Der wirkliche Schlüssel liegt nun in der Schnittmenge aller Kandidatenlisten, bei denen die echte Input-Difference in the letzte S-Box tatsächlich c war.
    """

    # Lasse den Challenger die erste Nachricht m1 = m verschlüsseln (eigentlich kennen wir hier ausschließlich m und c1 !!!):
    u1, v1, w1, x1, y1, z1, c1 = chiffre3(m, k1, k2, k3, k4)

    # Lasse den Challenger die zweite Nachricht m2 = m + Δin = m + 0xf verschlüsseln:
    u2, v2, w2, x2, y2, z2, c2 = chiffre3(m + a_vec(din), k1, k2, k3, k4)

    if c1+c2 not in possible_diffs:
        print(f'dc= {b2nh(c1+c2)}: {b2nh(m)}, {b2nh(m+a_vec(din))}  is a bad pair')
    else:
        print(f'dc= {b2nh(c1+c2)}: {b2nh(m)}, {b2nh(m+a_vec(din))}  is a good pair')

    print(f'true input difference to the last Sbox: {b2nh(y1+y2)}') # Wir gehen davon aus, dass es
    
    for k in B:
        if a_vec(dout) == Sinv(c1 + k) + Sinv(c2 + k):
            print(f'{b2nh(k)} is candidate')
    print('\n')

def break3():
    """
    Führt algo3() für mehrere Paare (m1, m2) - wobei m2 = m1 + 0xf - aus, genauer gesagt für *alle*, d.h. für alle m in B = VectorSpace(GF(2), b_len), b_len=4
    Der verwendete Schlüssel (d.h. genauer die 4 Rundenschlüssel) bleiben dabei natürlich gleich.

    Ausgabe:

    dc= e: 0, f  is a good pair
    true input difference to the last Sbox: c
    4 is candidate
    a is candidate
    9 is candidate
    5 is candidate
    b is candidate
    7 is candidate

    ...

    dc= 5: 2, d  is a good pair
    true input difference to the last Sbox: c
    a is candidate
    f is candidate

    ...

    dc= 5: d, 2  is a good pair
    true input difference to the last Sbox: c
    a is candidate
    f is candidate

    ...

    dc= e: f, 0  is a good pair
    true input difference to the last Sbox: c
    4 is candidate
    a is candidate
    9 is candidate
    5 is candidate
    b is candidate
    7 is candidate
    """

    k1 = a_vec(4) # "Der verwendete Schlüssel (d.h. genauer die 4 Rundenschlüssel) bleiben dabei natürlich gleich."
    k2 = a_vec(0xc)
    k3 = a_vec(7)
    k4 = a_vec(0xa)

    for m in B:
        algo3(m, k1, k2, k3, k4) # printet!

break3()
     