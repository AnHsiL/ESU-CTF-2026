
from dataclasses import dataclass, field
from pathlib import Path
import argparse
import secrets
import time

# 公開的大質數模數
P = int(''.join('''
    FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
    29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
    EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
    E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
    EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
    C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
    83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
    670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
    E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
    DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
    15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
    '''.split()), 16
)
Q = (P - 1) // 2
G = 2
ELEMENT_BYTES = (P.bit_length() + 7) // 8 # 群元素的固定編碼長度


def dim(capacity:int):
    if capacity < 1:
        raise ValueError('capacity must be a positive integer')
    width = capacity.bit_length()  # ceil(log2(capacity + 1))
    return width, 1 + width + 8*capacity


def normal_keygen():
    """Return public (h,u,v) and private exponent b."""
    r1, r2 = secrets.randbelow(Q), secrets.randbelow(Q)
    return (pow(G, r1, P), pow(G, r2, P), pow(G, r1*r2 % Q, P)), r2


def lossy_keygen():
    """Choose c != r1r2."""
    r1, r2 = secrets.randbelow(Q), secrets.randbelow(Q)
    c = secrets.randbelow(Q)
    while c == r1*r2 % Q:
        c = secrets.randbelow(Q)
    return pow(G, r1, P), pow(G, r2, P), pow(G, c, P)


def pack(choice:bool, msg:bytes, capacity:int):
    width, _ = dim(capacity)
    if not isinstance(msg, bytes):
        raise TypeError('message must be bytes; encode text with UTF-8')
    
    if choice:
        if len(msg) > capacity:
            raise ValueError('message exceeds capacity')
        length = len(msg)
        body = msg + secrets.token_bytes(capacity - length)
    else:
        length = 0
        body = secrets.token_bytes(capacity)

    return str(int(choice)) + format(length, f'0{width}b') + ''.join(format(byte, '08b') for byte in body)


def encrypt_bit(pk, bit:int):
    if bit not in (0, 1):
        raise ValueError('bit must be 0 or 1')
    h, u, v = pk
    r, s = secrets.randbelow(Q), secrets.randbelow(Q)
    x = pow(G, r, P) * pow(h, s, P) % P
    y = pow(G, bit, P) * pow(u, r, P) * pow(v, s, P) % P
    return x, y


def encrypt_bits(pk, bits):
    return tuple(encrypt_bit(pk, int(bit)) for bit in bits)


def decrypt_bit(sk, pair):
    x, y = pair
    z = y * pow(pow(x, sk, P), -1, P) % P

    if z == 1:
        return '0'
    if z == G:
        return '1'
    
    raise ValueError('invalid ciphertext for this normal key')


def decrypt_bits(sk, c):
    return ''.join(decrypt_bit(sk, pair) for pair in c)


@dataclass(frozen=True)
class Result:
    status: str  # ACCEPT / REJECT / NO_INFO
    message: bytes | None = None


def unpack(bits, capacity:int):
    width, count = dim(capacity)

    if len(bits) != count or set(bits) - {'0', '1'}:
        raise ValueError('invalid payload')
    if bits[0] == '0':
        return Result('REJECT')
    
    l = int(bits[1:1+width], 2)
    if l > capacity:
        raise ValueError('invalid message length')
    
    body = bits[1+width:]
    data = bytes(int(body[i:i+8], 2) for i in range(0, len(body), 8))
    return Result('ACCEPT', data[:l])


def encode_elements(elements):
    return b''.join(x.to_bytes(ELEMENT_BYTES, 'big') for x in elements)


def decode_elements(data, count:int):
    if len(data) != count * ELEMENT_BYTES:
        raise ValueError('wrong wire length')
    
    values = tuple(int.from_bytes(data[i:i+ELEMENT_BYTES], 'big')
                   for i in range(0, len(data), ELEMENT_BYTES))
    
    if any(not 1 <= x < P for x in values):
        raise ValueError('invalid element encoding')
    return values


@dataclass
class ReceiverState:
    """Local state only. Never send or log this object."""
    capacity: int
    sk: int | None = field(repr=False)


def start(choice:bool, capacity:int):
    """Receiver creates private state and public key bytes for the sender."""
    dim(capacity)

    if choice:
        pk, sk = normal_keygen()
    else:
        pk, sk = lossy_keygen(), None

    return ReceiverState(capacity, sk), encode_elements(pk)


def send(choice:bool, msg, capacity:int, pk_bytes):
    """Sender encrypts using the receiver's public key."""

    pk = decode_elements(pk_bytes, 3)
    bits = pack(choice, msg, capacity)
    c = encrypt_bits(pk, bits)

    return encode_elements(x for pair in c for x in pair)


def receive(state, c_bytes):
    _, count = dim(state.capacity)
    elements = decode_elements(c_bytes, 2 * count)
    if state.sk is None:
        return Result('NO_INFO')
    pairs = tuple(zip(elements[::2], elements[1::2]))
    return unpack(decrypt_bits(state.sk, pairs), state.capacity)


def load_config(path):
    """Load LOCAL demo inputs, never a public wire-format configuration."""
    import yaml
    with Path(path).open(encoding='utf-8') as stream:
        config = yaml.safe_load(stream)

    if not isinstance(config, dict) or set(config) != {'capacity', 'sender', 'receiver'}:
        raise ValueError('YAML must contain exactly capacity, sender, receiver')
    dim(config['capacity'])

    for role, size in [('sender', 3), ('receiver', 2)]:
        entry = config[role]
        if not isinstance(entry, list) or len(entry) != size:
            raise ValueError(f'{role} must be a list of {size} items')
        if not isinstance(entry[0], str) or not entry[0].strip():
            raise ValueError(f'{role} name must be nonempty text')
        if type(entry[1]) is not bool:
                raise TypeError('Choice must be bool')
    
    msg = config['sender'][2]
    if not isinstance(msg, str):
        raise TypeError('sender message must be text')
    if len(msg.encode('utf-8')) > config['capacity']:
        raise ValueError('UTF-8 message exceeds capacity')
    
    return config


def demo(config_path):
    config = load_config(config_path)
    sender, sender_choice, msg = config['sender']
    receiver, receiver_choice = config['receiver']
    capacity = config['capacity']

    t0 = time.perf_counter()
    state, pk = start(receiver_choice, capacity)
    t_start = time.perf_counter() - t0

    t0 = time.perf_counter()
    c = send(sender_choice, msg.encode('utf-8'), capacity, pk)
    t_send = time.perf_counter() - t0

    t0 = time.perf_counter()
    res = receive(state, c)
    t_recv = time.perf_counter() - t0
    
    print(f'{sender} -> {receiver}: {res.status}')
    if res.message is not None:
        print('message: ', res.message.decode('utf-8'))

    print(f'public key: {len(pk)} bytes, ciphertext: {len(c)} bytes')

    print("-"*30)
    print(f'capacity: {capacity}')
    print(f'start time:   {t_start:.6f} 秒')
    print(f'send time:    {t_send:.6f} 秒')
    print(f'receive time: {t_recv:.6f} 秒')
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Local HBC protocol')
    parser.add_argument('config', nargs='?', type=Path, default=Path(__file__).with_name('config.yaml'))
    args = parser.parse_args()
    
    try:
        demo(args.config)
    except (ValueError, TypeError, OSError) as error:
        parser.exit(2, f'Configuration/protocol error: {error}\n')
