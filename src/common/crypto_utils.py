from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


def hash(data: bytes) -> bytes:
    digest = hashes.Hash(algorithm=hashes.SHA256(), backend=default_backend())
    digest.update(data)
    return digest.finalize()


def hash_with_salt(password: bytes, salt: bytes, iterations: int = 200_000):
    return PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    ).derive(password)


def generate_keypair():
    return rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
