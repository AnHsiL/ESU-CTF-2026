from sage import *
from Crypto.Util.number import *

FLAG_BITS = 84 * 8 
BETA = 0.45

moduli = []     # p
cipher = []     # c
e = 0x10001

with open("./output.txt", "r") as f:
    for line in f:
        key, value = line.strip().split("=")

        if key == "p":
            moduli.append(Integer(value))
        elif key == "c":
            cipher.append(Integer(value))


residues = []

for p, c in zip(moduli, cipher):
    d = inverse_mod(e, p-1)
    r = power_mod(c, d, p)
    residues.append(r)
    

N = prod(moduli)
R = CRT(residues, moduli)

PR.<x> = PolynomialRing(Zmod(N))
f = x - R       # Coppersmith

roots = f.small_roots(
    X=2^FLAG_BITS,
    beta=BETA,
    epsilon=0.03
)

print(long_to_bytes(int(roots[0])))