from hashlib import sha256
from secrets import randbelow
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
E = EllipticCurve(GF(p), [0, 7])
G = E(55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)
flag = b"FLAG{TEST_ME}"

def point(Q):
    x, y = Q.xy()
    return (int(x), int(y))

def encrypt(secret, flag):
    key = sha256(str(secret).encode()).digest()
    return AES.new(key, AES.MODE_ECB).encrypt(pad(flag, 16))

a = randbelow(int(n - 1)) + 1
b = randbelow(int(n - 1)) + 1
P = a * G
bP = b * G
secret = int((a * bP).xy()[0])

print(f"p = {p}")
print("E = y^2 = x^3 + 7")
print(f"G = {point(G)}")
print(f"a = {a}")
print(f"aP = {point(P)}")
print(f"b = {b}")
print(f"bP = {point(bP)}")
print(f"enc = {encrypt(secret, flag).hex()}")
