import sympy as sp

import warnings
from sympy.utilities.exceptions import SymPyDeprecationWarning

warnings.filterwarnings(
    "ignore",
    category=SymPyDeprecationWarning
)

P = 2**130 - 5
MOD128 = 2**128
R_MASK = 0x0ffffffc0ffffffc0ffffffc0fffffff

x = sp.symbols("x")


# 建立 ChaCha20-Poly1305 實際拿去做 MAC 的多項式
def p_coeff(ct):
    data = (
        ct + b"\x00" * (-len(ct) % 16)
        + (0).to_bytes(8, "little")          # AAD length
        + len(ct).to_bytes(8, "little")      # ciphertext length
    )

    coeff = [0]

    for i in range(0, len(data), 16):
        block = data[i:i+16]

        # Poly1305 每個 block 後面補一個 1
        n = int.from_bytes(block, "little") + 2**128

        # acc = (acc + n) * r
        coeff[0] = (coeff[0] + n) % P
        coeff = [0] + coeff

    return coeff


def p_eval(coeff, r):
    result = 0

    for c in reversed(coeff):
        result = (result * r + c) % P

    return result


def recover_rs(c0, tag0, c1, tag1):
    p0 = p_coeff(c0)
    p1 = p_coeff(c1)

    size = max(len(p0), len(p1))

    diff = [
        (
            (p0[i] if i < len(p0) else 0)
            - (p1[i] if i < len(p1) else 0)
        ) % P
        for i in range(size)
    ]

    t0 = int.from_bytes(tag0, "little")
    t1 = int.from_bytes(tag1, "little")

    # tag 最後只有 128 bits，所以要補可能被截掉的 carry
    for carry in range(-4, 5):
        f = diff.copy()

        f[0] = (
            f[0]
            - (t0 - t1 + carry * MOD128)
        ) % P

        poly = sp.Poly.from_list(
            list(reversed(f)),
            x,
            modulus=P
        )

        for factor, _ in sp.factor_list(poly, modulus=P)[1]:

            if factor.degree() != 1:
                continue

            a, b = map(int, factor.all_coeffs())

            a %= P
            b %= P

            poly_r = (-b * pow(a, -1, P)) % P

            # Poly1305 r 必須符合 clamp
            if (poly_r & R_MASK) != poly_r:
                continue

            poly_s = (
                t0 - p_eval(p0, poly_r)
            ) % MOD128

            # 用第二組 tag 驗證
            check = (
                p_eval(p1, poly_r) + poly_s
            ) % MOD128

            if check == t1:
                return poly_r, poly_s

    raise ValueError("r, s not found")