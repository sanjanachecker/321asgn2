from random import randint
from sympy import *
# from gmpy2 import mpz


# a = 1
# b = 100
# p = randint(a, b)
# q = randint(a, b)
# while not isprime(p) or not isprime(q) or p == q:
#     p = randint(a, b)
#     q = randint(a, b)

# print(p)
# print(q)


# def generateKey(p, q):
#     n = p * q
#     phi_n = (p - 1) * (q - 1)
#     e = 65537

#     d = pow(e, -1, phi_n)
#     return ((n, e), (n, d))


# public_key, private_key = generateKey(p, q)
# print("Public key:", public_key)
# print("Private key:", private_key)

import random


def generate_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        if isprime(prime_candidate):
            return prime_candidate


def mod_inv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def generate_keypair(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = mod_inv(e, phi)
    return ((e, n), (d, n))


def encrypt(message, public_key):
    e, n = public_key
    return pow(message, e, n)


def decrypt(ciphertext, private_key):
    d, n = private_key
    return pow(ciphertext, d, n)


# Testing
message = "Hello, RSA!"
hex_message = int(message.encode('utf-8').hex(), 16)

public_key, private_key = generate_keypair(2048)
encrypted_message = encrypt(hex_message, public_key)
decrypted_message = decrypt(encrypted_message, private_key)

print("Original Message:", message)
print("Encrypted Message:", encrypted_message)
print("Decrypted Message:", bytes.fromhex(
    hex(decrypted_message)[2:]).decode('utf-8'))
