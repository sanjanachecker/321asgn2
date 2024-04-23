import random
import hashlib
from sympy import *
from Crypto.Util import number
from cbc import *
from ssl import RAND_bytes


def generate_prime(bits):
    primeNum = number.getPrime(bits)

    return primeNum

# def mod_inv(a, m):
#     m0, x0, x1 = m, 0, 1
#     while a > 1:
#         q = a // m
#         m, a = a % m, m
#         x0, x1 = x1 - q * x0, x0
#     return x1 + m0 if x1 < 0 else x1


def generate_keypair(p,q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)
    # d = mod_inv(e, phi)
    return ((e, n), (d, n))


def encrypt(message, public_key):
    e, n = public_key
    return pow(message, e, n)


def decrypt(ciphertext, private_key):
    d, n = private_key
    return pow(ciphertext, d, n)


# -------- part 1 ------------
# sending messages to self
message = "Hello world!"
hex_message = int(message.encode('utf-8').hex(), 16)
p = generate_prime(2048)
q = generate_prime(2048)
public_key, private_key = generate_keypair(p, q)
encrypted_message = encrypt(hex_message, public_key)
decrypted_message = decrypt(encrypted_message, private_key)

print("Original Message:", message)
print("Encrypted Message:", encrypted_message)
print("Decrypted Message:", bytes.fromhex(
    hex(decrypted_message)[2:]).decode('utf-8'))


# ------ part 2 -------
p = generate_prime(2048)
q = generate_prime(2048)

alice_pk, alice_sk = generate_keypair(p, q)
n, e = alice_pk
n, d = alice_sk
s = random.randint(1, n) # natural number 

#bob computes ciphertext and sends c
c = pow(s, e, n)
print("c: ", c)

# mallory tampers with c, sending c' instead
c_prime = c * 3

# alice decrypts c
s = pow(c_prime, d, n)
print("alice's s value: ", s)

# alice computes k 
secret_key = str(s).encode('utf-8')
k = hashlib.sha256(secret_key).digest()[:16]

iv = RAND_bytes(16)

m = "Hi Bob!"
print("Alice's original message: ", m)
c0 = cbc_encrypt((m.encode('utf-8')), k, iv)
print("Alice's encrypted message ", c0)

# mallory computes value of s without knowing Alice's private key
s_mal = pow(c_prime, e, n)
# mallory's s value should be the same as alice's computed s value
print("mallory's s value: ", s_mal)
k_mal = hashlib.sha256(str(s_mal).encode('utf-8')).digest()[:16]

# mallory decrypt with cbc
mal_decrypted = cbc_decrypt(c0, k_mal, iv)
mal_decrypted_string = mal_decrypted.decode('utf-8')
print("Mallory decrypted Alice's message", mal_decrypted_string)