from Crypto.Util.number import *
from sage.modules.free_module_integer import IntegerLattice
from itertools import combinations, product
import hashlib

imag_keys = [
    ("9.83329568728950e13", "1.94539067458416e14"),
    ("4.57795946512170e13", "5.54913449090490e13"),
    ("3.35752608137010e13", "1.10651091133529e14"),
    ("8.09172050820060e13", "6.09012985967910e13"),
    ("2.75388068605530e13", "5.12867910525740e13"),
    ("2.33510497525684e14", "9.11264352204540e13"),
    ("2.36186170290599e14", "2.03323868604921e14"),
    ("1.37793863865401e14", "1.40354868241912e14")
]

Gift = '69ae60327282356b2f2731e6acf624f4'



cnt_r = ZZ(RR("3.22421607806873e14").round())
cnt_i = ZZ(RR("1.37668712938916e16").round())

coeff_r = []
coeff_i = []

keys = [
    (ZZ(RR(k).round()), ZZ(RR(k_i).round())) for k, k_i in imag_keys
]
for k, k_i in keys:
    coeff_r += [k, -k_i]
    coeff_i += [k_i, k]



# 建 matrix

SCALE = 1000 # 可調整的權重

A = [[0]*18 for _ in range(16)]

for i in range(16):
    A[i][i] = SCALE
    A[i][-1] = coeff_i[i]
    A[i][-2] = coeff_r[i]

A = Matrix(ZZ, A)


target = vector(
    ZZ,
    [SCALE*(0+15)//2]*16 + [cnt_r, cnt_i]
)



# CVP: LLL + Babai nearest plane
B = A.LLL()

# Gram-Schmidt
B_QQ = Matrix(QQ, B)
G, _ = B_QQ.gram_schmidt(orthonormal=False)

# Babai nearest plane：找接近 target 的 lattice vector
y = vector(QQ, target)
v = vector(ZZ, [0]*18)

for i in reversed(range(B.nrows())):
    c = ZZ(round((y * G[i]) / (G[i] * G[i])))
    v += c * B[i]
    y -= c * B_QQ[i]


#  recover flag part
flag_part = [v[i] // SCALE for i in range(16)]

if all(0 <= x <= 15 for x in flag_part):
    flag = "".join(hex(x)[2:] for x in flag_part)
    print(hashlib.md5(b"THJCC{" + flag.encode() + b"}").hexdigest() == Gift)
    print("THJCC{" + flag + "}")
