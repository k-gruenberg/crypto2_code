from sage.all import *

# This is the big example 11.5 from von zur Gathen, CryptoSchool.
# There you find an intelligent approach, here you will find just brute force. 

B1 = VectorSpace(GF(2),1)
B2 = VectorSpace(GF(2),2)
B3 = VectorSpace(GF(2),3)
B4 = VectorSpace(GF(2),4)
B5 = VectorSpace(GF(2),5)
B6 = VectorSpace(GF(2),6)
B=[0,B1,B2,B3,B4,B5,B6]

p_6_1 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0]])))
p_6_2 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0],[0,1,0,0,0,0]])))
p_6_3 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0]])))
p_6_4 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0]])))
p_6_5 = linear_transformation(transpose(Matrix(GF(2),[[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0]])))

p_6 = [0,p_6_1,p_6_2,p_6_3,p_6_4,p_6_5]

def X(b):
    """
    Anders als in ue08_rnd4.py ist der PRG X jetzt nicht mehr über eine Matrix dargestellt,
    sondern per Fallunterscheidung, jedoch weiterhin 3-Bit-Seed auf 6-Bit-"Randomness".

    Man beachte, dass die zurückgegebenen Zufallsvektoren stets 3 Nullen und 3 Einsen enthalten; bei ue08_rnd4.py war dies *NICHT* so!
    """
    if b == B3([0,0,0]):
        return B6([0,0,1,1,0,1])
    if b == B3([0,0,1]):
        return B6([0,0,1,0,1,1])
    if b == B3([0,1,0]):
        return B6([0,1,1,0,1,0])
    if b == B3([0,1,1]):
        return B6([0,1,0,1,1,0])
    if b == B3([1,0,0]):
        return B6([1,0,1,1,0,0])
    if b == B3([1,0,1]):
        return B6([1,0,0,1,0,1])
    if b == B3([1,1,0]):
        return B6([1,1,0,1,0,0])
    if b == B3([1,1,1]):
        return B6([1,1,0,0,1,0])


def D(x):
    """
    In ue08_rnd4.py war der Distinguisher D() eine affine Abbildung; hier schaut der Distinguisher, ob x aus exakt 3 Nullen und 3 Einsen besteht:
    
    sage: D((1, 1, 1, 1, 1, 1))
    0
    sage: D((0, 0, 0, 0, 0, 0))
    0
    sage: D((0, 0, 0, 1, 1, 1))
    1
    sage: D((1, 1, 1, 0, 0, 0))
    1
    sage: D((1, 1, 0, 0, 0, 1))
    1
    sage: D((1, 1, 0, 1, 0, 1))
    0
    sage: D((1, 0, 0, 0, 0, 1))
    0
    """
    w = ZZ(x[0])+ZZ(x[1])+ZZ(x[2])+ZZ(x[3])+ZZ(x[4])+ZZ(x[5])
    if w == 3:
        return 1
    else:
        return 0

# how much distinguishes D the r.v. X from the uniform distribution?
n0 = sum([D(b) for b in B6])/64
n6 = sum([D(X(a)) for a in B3])/8

# We construct the hybrid distributions between H_0 = U and H_6 = X
# For this we need the projections of X on B^i
# Since a vector is not hashable, we cannot use it as key for a dictionary
h_dict = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
for i in range(1,6):
    h_dict[i] = dict([[str(b),0] for b in B[i]])


for b in B3:
    z = X(b)
    for i in range(1,6):
        t = str(p_6[i](z))
        h_dict[i][t] += 1

n1 = sum([D(b) * h_dict[1][str(p_6_1(b))]/8 * 1/32 for b in B6])
n2 = sum([D(b) * h_dict[2][str(p_6_2(b))]/8 * 1/16 for b in B6])
n3 = sum([D(b) * h_dict[3][str(p_6_3(b))]/8 *  1/8 for b in B6])
n4 = sum([D(b) * h_dict[4][str(p_6_4(b))]/8 *  1/4 for b in B6])
n5 = sum([D(b) * h_dict[5][str(p_6_5(b))]/8 *  1/2 for b in B6])

print(n0)
print(n1)
print(n2)
print(n3)
print(n4)
print(n5)
print(n6)

# The experiment suggests that we might be able to predict the last bit of X
def predictor(x1,x2,x3,x4,x5):
    xx = vector(GF(2), [x1,x2,x3,x4,x5,0])
    if D(xx) == 1:
        return 0
    else:
        return 1

for b in B3:
    z = X(b)
    print(b)
    print(z[5])
    print(predictor(z[0],z[1],z[2],z[3],z[4]))
    