from Crypto.Util.number import *
from Secret import flag2

def leak_info(primes):
    mod = getPrime(4096)
    parameters = [getPrime(4096) for _ in range(3)]
    cnt = sum(primes[i] * parameters[i] for i in range(3)) % mod
    print(f"---leak info---\n{cnt=}\n{parameters=}\n{mod=}")

primes = [getPrime(512) for _ in range(3)]
p, q, r = primes
n = p * q * r
e = 0x10001
c = pow(bytes_to_long(flag2), e, n)
print(f"{n=}\n{e=}\n{c=}")
leak_info(primes)

