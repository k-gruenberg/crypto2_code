from sage.all import *

B1 = VectorSpace(GF(2),1) # [x for x in B1] -> [(0), (1)]
B2 = VectorSpace(GF(2),2) # [x for x in B2] -> [(0, 0), (1, 0), (0, 1), (1, 1)]
B3 = VectorSpace(GF(2),3) # [x for x in B3] -> [(0, 0, 0), (1, 0, 0), ..., (0, 1, 1), (1, 1, 1)]
B4 = VectorSpace(GF(2),4)
B5 = VectorSpace(GF(2),5)
B6 = VectorSpace(GF(2),6)
B=[0,B1,B2,B3,B4,B5,B6]   # [0, Vector space of dimension 1 over Finite Field of size 2, ..., Vector space of dimension 6 over Finite Field of size 2]
# => B[0] wird nie aufgerufen; schöner wäre daher hier "None" statt "0"

"""
sage: p_6_1
Vector space morphism represented by the matrix:
[1]
[0]
[0]
[0]
[0]
[0]
Domain: Vector space of dimension 6 over Finite Field of size 2         # f: X -> Y. X is the domain of f. Y is the codomain of f. (https://en.wikipedia.org/wiki/Codomain)
Codomain: Vector space of dimension 1 over Finite Field of size 2

sage: p_6_1((1, 0, 0, 0, 0, 0))
(1)
sage: p_6_1((0, 1, 1, 1, 1, 1))
(0)

=> p_6_1: B^6 -> B; gibt das 1. Bit zurück
"""
p_6_1 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0]])))

"""
sage: p_6_2
Vector space morphism represented by the matrix:
[1 0]
[0 1]
[0 0]
[0 0]
[0 0]
[0 0]
Domain: Vector space of dimension 6 over Finite Field of size 2
Codomain: Vector space of dimension 2 over Finite Field of size 2

sage: p_6_2((1, 1, 0, 0, 0, 0))
(1, 1)
sage: p_6_2((0, 0, 1, 1, 1, 1))
(0, 0)

=> p_6_2: B^6 -> B^2; gibt die ersten beiden Bits zurück
"""
p_6_2 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0],[0,1,0,0,0,0]])))

p_6_3 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0]])))

p_6_4 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0]])))

"""
sage: p_6_5
Vector space morphism represented by the matrix:
[1 0 0 0 0]
[0 1 0 0 0]
[0 0 1 0 0]
[0 0 0 1 0]
[0 0 0 0 1]
[0 0 0 0 0]
Domain: Vector space of dimension 6 over Finite Field of size 2
Codomain: Vector space of dimension 5 over Finite Field of size 2

sage: p_6_5((1, 1, 1, 1, 1, 0))
(1, 1, 1, 1, 1)
sage: p_6_5((0, 0, 0, 0, 0, 1))
(0, 0, 0, 0, 0)

=> p_6_5: B^6 -> B^5; gibt die ersten fünf Bits zurück
"""
p_6_5 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0]])))

p_6 = [0,p_6_1,p_6_2,p_6_3,p_6_4,p_6_5]

"""
sage: A
[1 0 0 1 0 1]
[0 1 0 1 1 0]
[0 0 1 0 1 1]
"""
A = Matrix(GF(2), [[1,0,0,1,0,1],[0,1,0,1,1,0],[0,0,1,0,1,1]])

"""
sage: X
Vector space morphism represented by the matrix:
[1 0 0 1 0 1]
[0 1 0 1 1 0]
[0 0 1 0 1 1]
Domain: Vector space of dimension 3 over Finite Field of size 2
Codomain: Vector space of dimension 6 over Finite Field of size 2
"""
X = linear_transformation(A) # X soll eine Zufallsvariable darstellen, genauer [X(a) for a in B3]; der Distinguisher D soll diese dann von der gleichförmigen Verteilung U unterscheiden können
# !!!!! X ist ein simpler Zufallsgenerator, X nimmt einen 3-Bit großen Seed und generiert eine 6-Bit große Zahl, z.B.: X((0,1,0)) -> (0, 1, 0, 1, 1, 0) !!!!!

"""
sage: Dm
[0]
[0]
[0]
[1]
[1]
[1]
"""
Dm = Matrix(GF(2), [[0,0,0,1,1,1]]) # Dm = "Distinguisher matrix"
Dm = transpose(Dm)

"""
sage: Dl
Vector space morphism represented by the matrix:
[0]
[0]
[0]
[1]
[1]
[1]
Domain: Vector space of dimension 6 over Finite Field of size 2
Codomain: Vector space of dimension 1 over Finite Field of size 2
"""
Dl = linear_transformation(Dm)

def D(x):
    """
    Distinguisher D: B^6 -> B, definiert durch Anwenden der 6x1-Matrix "Dm" und anschließendes Addieren von 1.
    Unser Distinguisher ist also eine affine Abbildung (ugs. lineare Abbildung).

    sage: D((0, 0, 0, 0, 0, 0))
    1
    sage: D((0, 0, 0, 0, 0, 1))
    0
    sage: D((0, 0, 0, 0, 1, 0))
    0
    sage: D((0, 0, 0, 0, 1, 1))
    1
    sage: D((0, 0, 0, 1, 0, 0))
    0
    sage: D((0, 0, 0, 1, 0, 1))
    1
    sage: D((0, 0, 0, 1, 1, 0))
    1
    sage: D((0, 0, 0, 1, 1, 1))
    0
    sage: D((0, 0, 1, 0, 0, 0))
    1
    sage: D((0, 0, 1, 0, 0, 1))
    0
    sage: D((1, 1, 1, 1, 1, 1))
    0
    """
    return ZZ(Dl(x)[0]+1) # e.g. Dl((0, 0, 0, 0, 0, 0)) -> (0), then add 1

# how much distinguishes D the random variable X from the uniform distribution?   # "r.v." = abbreviation for "random variable" (https://mathworld.wolfram.com/RandomVariable.html)
n0 = sum([D(b) for b in B6])/64    # n0 == 1/2 # [b for b in B6]    -> [(0, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0), ..., (1, 1, 1, 1, 1, 1)]
n6 = sum([D(X(a)) for a in B3])/8  # n6 == 1   # [X(a) for a in B3] -> [(0, 0, 0, 0, 0, 0), (1, 0, 0, 1, 0, 1), (0, 1, 0, 1, 1, 0), (1, 1, 0, 0, 1, 1),
                                               #                        (0, 0, 1, 0, 1, 1), (1, 0, 1, 1, 1, 0), (0, 1, 1, 1, 0, 1), (1, 1, 1, 0, 0, 0)]
# ...denn: [D(X(a)) for a in B3] == [1, 1, 1, 1, 1, 1, 1, 1]
#
# !!!!! Das bedeutet: Wenn der Distinguisher D() auf einen vom PRG X generierten "Zufallswert" aufgerufen wird, arbeitet er perfekt und gibt stets 1 zurück! !!!!!
#                     Wenn der Distinguisher D() auf einem von der Gleichvertilung U generierten, also einem echten Zufallswert, aufgerufen wird, gibt er dagegen genau in der Hälfte der Fälle 1 zurück.
#                     D ist ein 1/2-Distinguisher! !!!!!
#                     Das ist sehr gut; will ich wissen, ob jemand seine Werte echt zufällig oder mithilfe des PRG X generiert,
#                       so muss ich mir nur N generierte Werte anschauen:
#                         – Hat D() wenigstens einmal 0 zurückgegeben => Es wurde *definitiv* nicht X zur Erzeugung der Zufallsbits genutzt!
#                         – Hat D() alle N-mal 1 zurückgegeben        => Es wurde mit Wk. 1-(1/2)^N X zur Erzeugung der Zufallsbits genutzt!

# We construct the hybrid distributions between H_0 = U and H_6 = X
# For this we need the projections of X on B^i
# Since a vector is not hashable, we cannot use it as key for a dictionary => so we transform the vectors to a String using the str() function
"""
sage: big_dic
{1: {'(0)': 4, '(1)': 4},
 2: {'(0, 0)': 2, '(1, 0)': 2, '(0, 1)': 2, '(1, 1)': 2},
 3: {'(0, 0, 0)': 1,
  '(1, 0, 0)': 1,
  '(0, 1, 0)': 1,
  '(1, 1, 0)': 1,
  '(0, 0, 1)': 1,
  '(1, 0, 1)': 1,
  '(0, 1, 1)': 1,
  '(1, 1, 1)': 1},
 4: {'(0, 0, 0, 0)': 1,
  '(1, 0, 0, 0)': 0,
  ...
  '(1, 1, 1, 1)': 0},
 5: {'(0, 0, 0, 0, 0)': 1,
  '(1, 0, 0, 0, 0)': 0,
  ...
  '(1, 1, 1, 1, 1)': 0}}

=> sagt uns, wie gut der PRG X im Vergleich zur gleichförmigen Verteilung abschneidet,
   wenn man nur die ersten 1, 2, 3, 4 oder 5 Bit seiner 6-Bit-Zufallsausgabe betrachtet
=> anhand der ersten 1, 2 und 3 Bits ist einer von einer gleichförmigen Verteilung nicht zu unterscheiden! (dies lässt auch leicht durch Hingucken erkennen; siehe oben)
   => tatsächlich folgt diese Aussage für 1 und 2 Bits natürlich auch bereits schon aus der Aussage für 3 Bits!
=> für die ersten 4 und 5 Bits dagegen schon, das kann aber auch gar nicht anders sein, da X ja lediglich einen 3-Bit-Seed entgegennimmt !!!!!
"""
# Initialisieren von big_dic mit Nullen:
big_dic = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
for i in range(1,6):
    big_dic[i] = dict([[str(b),0] for b in B[i]]) # remember: B=[0,B1,B2,B3,B4,B5,B6] = [0, VectorSpace(GF(2),1), ..., VectorSpace(GF(2),6)]
# Befüllen von big_dic durch inkrementelles Hochzählen:
for b in B3: # Für alle 3-Bit-Seeds b:
    z = X(b) # Nutze den PRG X zum Generieren eines 6-Bit-"Zufalls"-Vektors z.
    for i in range(1,6):
        t = str(p_6[i](z))                        # remember: p_6=[0,p_6_1,p_6_2,p_6_3,p_6_4,p_6_5] = [0, transpose(Matrix(GF(2),[[1,0,0,0,0,0]])), transpose(Matrix(GF(2),[[1,0,0,0,0,0],[0,1,0,0,0,0]])), ...]
        big_dic[i][t] += 1
"""
Da die Matrizen in p_6 ganz einfach "abgeschnittene Einheits-Matrizen" sind, gilt schlichtweg:

sage: p_6[1]((1,0,1,0,1,0))
(1)
sage: p_6[2]((1,0,1,0,1,0))
(1, 0)
sage: p_6[3]((1,0,1,0,1,0))
(1, 0, 1)
sage: p_6[4]((1,0,1,0,1,0))
(1, 0, 1, 0)
sage: p_6[5]((1,0,1,0,1,0))
(1, 0, 1, 0, 1)
"""

n1 = sum([D(b) * big_dic[1][str(p_6_1(b))]/8 * 1/32 for b in B6]) # n1 == 1/2 # remember: p_6_x() sind einfach die "abgeschnittenen Einheitsmatrizen", die
n2 = sum([D(b) * big_dic[2][str(p_6_2(b))]/8 * 1/16 for b in B6]) # n2 == 1/2 #           die ersten x Bit zurückgeben
n3 = sum([D(b) * big_dic[3][str(p_6_3(b))]/8 *  1/8 for b in B6]) # n3 == 1/2
n4 = sum([D(b) * big_dic[4][str(p_6_4(b))]/8 *  1/4 for b in B6]) # n4 == 1/2 # remember: big_dic[x][y] für eine x-Bit-Eingabe y = wie
n5 = sum([D(b) * big_dic[5][str(p_6_5(b))]/8 *  1/2 for b in B6]) # n5 == 1/2 #           oft (absolut) der Präfix y vom PRG X erzeugt wird
# ...also vom Prinzip her genauso wie n0 und n6, nur komplizierter und umständlich aufgeschrieben.

"""
Vielleicht etwas verständlicher definiert wäre es so:

n0 = sum([D(b) for b in B6])/(1*64)

n1 = sum([D(vector(list(X(a)[:1]) + list(b))) for a in B3 for b in B5])/(8*32) # == 1/2
n2 = sum([D(vector(list(X(a)[:2]) + list(b))) for a in B3 for b in B4])/(8*16) # == 1/2
n3 = sum([D(vector(list(X(a)[:3]) + list(b))) for a in B3 for b in B3])/(8*8)  # == 1/2
n4 = sum([D(vector(list(X(a)[:4]) + list(b))) for a in B3 for b in B2])/(8*4)  # == 1/2
n5 = sum([D(vector(list(X(a)[:5]) + list(b))) for a in B3 for b in B1])/(8*2)  # == 1/2

n6 = sum([D(X(a)) for a in B3])/(8*1)
"""

print("Distinguisher:")
print(f'U.U.U.U.U.U n0 = {n0}')
print(f'X.U.U.U.U.U n1 = {n1}')
print(f'X.X.U.U.U.U n2 = {n2}')
print(f'X.X.X.U.U.U n3 = {n3}')
print(f'X.X.X.X.U.U n4 = {n4}')
print(f'X.X.X.X.X.U n5 = {n5}')
print(f'X.X.X.X.X.X n6 = {n6}')
print('=> D ist ein 1/2-Distinguisher zwischen X.X.X.X.X.X und jeder beliebigen der anderen Verteilungen.')

print("")
print("Predictor:")

# The experiment suggests that we might guess the last bit of X
def predictor(x1,x2,x3,x4,x5):
    """
    Nimmt die ersten 5 Bits eines von X generierten 6-Bit-Zufallsvektors entgegen und versucht, das 6. Bit vorherzusagen/zu predicten.
    Konstruiert wird der Predictor genau wie in der Vorlesung, auf Basis des bereits gegebenen Distinguishers, was logisch völlig einleuchtet.
    """
    xx = vector(GF(2), [x1,x2,x3,x4,x5,0])
    if D(xx) == 1: # Sagt der Distinguisher für den mit 0 endenden Vektor: "Ja, das sieht mir nach einem von X generierten Zufallswert aus."
        return 0   # ...dann sagt der Predictor eben jene 0 vorher.
    else:          # Und ansonsten
        return 1   # ...sagt der Predictor eben die 1 vorher.

for b in B3:
    z = X(b)
    print(f'Für den 3-Bit-Seed b = {b}')
    print(f'...generiert der PRG X den "Zufallswert" z = {z} mit letzem Bit z[5] = {z[5]}')
    prediction = predictor(z[0],z[1],z[2],z[3],z[4])
    print(f'Der Predictor sagt {prediction} und liegt damit {"richtig" if prediction == z[5] else "falsch"}!')
    