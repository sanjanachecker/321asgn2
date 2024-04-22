from random import randint
from sympy import *
from gmpy2 import mpz


a = 1
b = 100
p = randint(a, b)
q = randint(a, b)
while not isprime(p) or not isprime(q) or p == q:
    p = randint(a, b)
    q = randint(a, b)

print(p)
print(q)


def generateKey(p, q):
    n = p * q
    on = (p-1) * (q-1)
    e = 65537

    d = 1/(e)
