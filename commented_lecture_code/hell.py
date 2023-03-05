from sage.all import *

# Hellman Time Memory Trade-off
## The last version in class contained some errors which are fixed here

B = GF(2**12, name = 'g', repr = 'int') # 2**12 == 4096
g = B.gen()
a = g**11 + g**9  + g**8  + g**6  + g**3  + g

# build toy cryptosystem
def inv(x):
    if x == B(0):
        return B(0)
    else:
        return 1/x

def rnd(k, x): # rnd = "round" = die Rundenfunktion
    return inv(x+k)

def kdv(k): # kdv = "key derivation"
    return inv(k+a)

def enc(k,x):
    """
    Verschlüsselt den Klartext x mit dem Schlüssel k und dem 'toy cryptosystem'.
    """
    c = x # Ciphertext c = initial dem Plaintext x
    kr = k # kr = "key round" = Rundenschlüssel
    for i in range(3): # 'toy cryptosystem' hat 3 Runden (exkl. "Schlussrunde", siehe unten):
        c = rnd(kr,c) # Runde; wende den Rundenschlüssel kr auf den aktuellen Status/Ciphertext c an
        kr = kdv(kr) # leite den nächsten Rundenschlüssel ab
    return c + kr # Schlussrunde: addiere den letzten Rundenschlüssel nur noch auf, ein anschließendes Invertieren wie es rnd() noch tuen würde wäre überflüssig, da eh umkehrbar







# Preperation TMTO

## fixed plain text
x0 = g**33 # = ein Element aus B = GF(2**12) = GF(4096)

def f(y): # Bei Hellman's TMTO gilt: f(k) = Enc(k,x) - d.h. man fixiert den Klartext
    return enc(y,x0) # = enc(k=y, x=x0=g**33=const.)

## s*t**2 = 2**12 (number of keys)    ## ...denn nach Vorlesung wählen wir s*t = 2^n / t
## This would lead to s = t = 16: try yourself.    ## ...denn 16*16 = 2^12 / 16 = 256, stimmt! (Bilde Logarithmus: 4+4 = 12-4)
s = 32 # Haha, ja siehste, geht nicht mit der Formel...
t = 16

tbl = Matrix(B,t,s) # die berüchtigte Hellman-TMTO-Tabelle/Matrix; eigentlich würde man nur die 1. und letzte Spalte speichern!

## in reality, we do not store the whole tbl
for i in range(t): # "Wähle t zufällige Schlüssel k[1], ..., k[t]"
    tbl[i,0] = B.random_element() # "Wähle t zufällige Schlüssel k[1], ..., k[t]"
    for j in range(1,s): # Fülle die Tabellenzeile durch ewig wiederholtes Anwenden der Funktion f(.)
        tbl[i,j] = f(tbl[i, j-1])







# do CPA
## choose a key:
k_secret = g**400
print(f'k_secret={k_secret}')
c = enc(k_secret, x0) # "Schicke x(0) an den Challenger und erhalte c."

# Analysis
def search(c): # ...gehe die gesamte Tabelle durch und suche; in Wirklichkeit wäre dies nicht Zeit O(s*t), sondern nur Zeit O(s), da die t Elemente in einer Hashtabelle wären => der besagte "TMTO"
    ret = [] # "Kandidatenliste" in Anführungszeichen
    c0 = c
    for j in range(s):
        # compare with i-th row entry in column s-1
        for i in range(t):
            if c0 == tbl[i,s-1]:
                ret.append([i,j])
                break
        c0 = f(c0)
    return ret # "Kandidatenliste" in Anführungszeichen

cand_list = search(c) # "Kandidatenliste" in Anführungszeichen







# Wir haben nun "Kandidatenliste" in Anführungszeichen; der eigentliche Schlüsselkandidat y ist jedoch ein weiter links in der
# Tabelle, berechne diese(n) und gebe aus:

def analysis(i,j,c): # (Parameter c scheint mir unnötig)
    # we know: f**(j)(c) == tbl[i, s-1]
    # by construction: f**(j)(tbl[i, s-j-1]) == tbl[i,s-1]
    # further: tbl[i, s-j-1] ) == f(tbl[i, s-j-2])
    # Therefore we assume that f(tbl[i, s-j-2]) = c, whence
    # k_secret = tbl[i, s-j-2] = f**(s-j-2)(tbl[i,0])

    z = tbl[i,0] # ...fange ganz links in der Tabelle an; das ist die Information die wir eigentlich nur gespeichert haben
    # Gehe in der (imaginären) Tabelle so lange nach rechts (d.h. wende wiederholt f(.) an),
    #   bis der Schlüsselkandidat y erreicht ist und zurückgeg. werden kann:
    for l in range(s-j-2): # (s = Breite der Tabelle; -2 damit wir den eigentlichen Schlüsselkandidaten kriegen)
        z = f(z)
    return z


for res in cand_list:
    print(f'possible key: {analysis(res[0],res[1],c)}') # (Parameter c scheint mir unnötig)







"""
Some example executions:

sage: load("/Users/kendrick/Github_k-gruenberg/crypto2_code/commented_lecture_code/hell.py")
k_secret=2711
possible key: 2711
possible key: 2711
possible key: 2711
possible key: 2703
possible key: 1518
sage: 
sage:
sage: load("/Users/kendrick/Github_k-gruenberg/crypto2_code/commented_lecture_code/hell.py")
k_secret=2711
possible key: 2711
possible key: 1518
possible key: 2711
possible key: 2703
possible key: 3960
possible key: 654
sage: 
sage: 
sage: load("/Users/kendrick/Github_k-gruenberg/crypto2_code/commented_lecture_code/hell.py")
k_secret=2711
possible key: 2711
possible key: 2711
possible key: 2711
possible key: 2711
possible key: 1930
possible key: 2433
sage: 
sage: 
sage: load("/Users/kendrick/Github_k-gruenberg/crypto2_code/commented_lecture_code/hell.py")
k_secret=2711
possible key: 2711
possible key: 1696
"""
