data = (
    (0x5A5B474874727F75).to_bytes(8, "little")
    + b"@lUF]PGZ\\]lZ@lF]AVRP[RQ_VN"
)

decoded = bytes(x ^ 0x33 for x in data)

print(decoded)