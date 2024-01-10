import os
import socket

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag
from .utils import Session


class CryptoRequest:
    def __init__(self, session: Session):
        self.session = session
        self.password = session.key

    def to_bytes(self, data: bytes) -> bytes:
        password = self.password.encode()
        key, salt = generate_key(password)
        encrypted_data = encrypt_data(key, data)
        return salt + encrypted_data


class CryptoReply:
    def __init__(self, session: Session):
        self.password = session.key
        self.session = session
        self.data = None

    def from_bytes(self, data: bytes):
        if len(data) < 16:
            return False
        try:
            salt = data[0: 16]
            encrypted_data = data[16: len(data)]
            key, salt = generate_key(self.password.encode(), salt)
            self.data = decrypt_data(key, encrypted_data)
        except InvalidTag as e:
            print(e)
            return False
        return True


def generate_key(password, salt=None, iterations=100000, key_length=None):
    if salt is None:
        salt = os.urandom(16)
    valid_key_lengths = {128, 192, 256}
    if key_length is None or key_length not in valid_key_lengths:
        key_length = 256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=iterations,
        length=key_length // 8,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return key, salt


def encrypt_data(key, plaintext):
    aead = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aead.encrypt(nonce, plaintext, None)
    return nonce + ciphertext


def decrypt_data(key, ciphertext):
    aead = AESGCM(key)
    nonce = ciphertext[:12]
    ciphertext = ciphertext[12:]
    decrypted_data = aead.decrypt(nonce, ciphertext, None)
    return decrypted_data


def send_encrypted(session: Session, message: bytes):
    request = CryptoRequest(session)
    data = request.to_bytes(message)
    l_data = len(data)
    try:
        session.sock.sendall(l_data.to_bytes(2, "big"))
        session.sock.sendall(data)
    except socket.error as e:
        print(e)


def recv_decrypted(session: Session):
    try:
        lb_message = session.sock.recv(2)
        l_message = int.from_bytes(lb_message, "big")
        message = session.sock.recv(l_message)
        if not message:
            session.sock.close()
            return None

        crypto_reply = CryptoReply(session)
        if crypto_reply.from_bytes(message) is False:
            return None

        return crypto_reply.data
    except socket.error as e:
        print(e)
