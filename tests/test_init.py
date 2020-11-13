import struct

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY = b'000102030405060708090A0B0C0D0E0F'


def __parse_key_string(key_string):
    num = int(key_string, 16)
    return struct.pack(">QQ", num >> 64, num & 0xFFFFFFFFFFFFFFFF)


key = __parse_key_string(KEY)

cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

encryptor = cipher.encryptor()
decryptor = cipher.decryptor()


ct = decryptor.update(b"a secret message") + decryptor.finalize()
print(ct)


f = encryptor.update(ct) + encryptor.finalize()
print(f)
