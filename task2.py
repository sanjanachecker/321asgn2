import hashlib
from ssl import RAND_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from cbc import *

q_hex = 'B10B8F96 A080E01D DE92DE5E AE5D54EC 52C99FBC FB06A3C6 9A6A9DCA 52D23B61 6073E286 75A23D18 9838EF1E 2EE652C013ECB4AE A9061123 24975C3C D49B83BF ACCBDD7D 90C4BD7098488E9C 219A7372 4EFFD6FA E5644738 FAA31A4F F55BCCC0A151AF5F 0DC8B4BD 45BF37DF 365C1A65 E68CFDA7 6D4DA708DF1FB2BC 2E4A4371'
a_hex = 'A4D1CBD5 C3FD3412 6765A442 EFB99905 F8104DD2 58AC507F D6406CFF 14266D31 266FEA1E 5C41564B 777E690F 5504F213 160217B4 B01B886A 5E91547F 9E2749F4 D7FBD7D3 B9A92EE1 909D0D22 63F80A76 A6A24C08 7A091F53 1DBF0A01 69B6A28A D662A4D1 8E73AFA3 2D779D59 18D08BC8 858F4DCE F97C2A24 855E6EEB 22B3B2E5'

q = int(q_hex.replace(' ', ''), 16)
a = int(a_hex.replace(' ', ''), 16)


def generate_public_key(priv_x, q, a):
    # priv_x < q
    return pow(a, priv_x) % q


def generate_secret_key(public_key, priv_x, q):
    return pow(public_key, priv_x) % q


# alice and bob generate public key
y_a = generate_public_key(6, q, a)
y_b = generate_public_key(15, q, a)

print("public key a:", y_a)
print("public key b:", y_b)

# ------ part 1 ---------
# mallory tampers with public key
y_a_tampered = q
y_b_tampered = q

# alice and bob generate secret key from public key
s_a = generate_secret_key(y_b_tampered, 6, q)
s_b = generate_secret_key(y_a_tampered, 15, q)

# mallory knows secret key is 0
s_mal = 0

# note: mallory knows both alice and bob's secret keys should be 0, since q^ anything % q is 0.
print("secret key a:", s_a)
print("secret key b:", s_b)

# ------ part 2 ---------

# encode secret key and truncate SHA-256 hash
secret_key = str(s_a).encode('utf-8')
k = hashlib.sha256(secret_key).digest()[:16]
# print(type(k))
# print(k)
iv = RAND_bytes(16)
# print(type(iv))

# encrypt with cbc
m1 = "Hi Bob!"
print("Alice's original message: ", m1)
m2 = "Hi Alice!"
print("Bob's original message: ", m2)
m1 = m1.encode()
m2 = m2.encode()
encrypted_m1 = cbc_encrypt(m1, k, iv)
encrypted_m2 = cbc_encrypt(m2, k, iv)
print("Alice's encrypted message: ", encrypted_m1)
print("Bob's encrypted message: ", encrypted_m2)


# Alice and Bob decrypt with cbc
m1_decrypted = cbc_decrypt(encrypted_m1, k, iv)
m1_decrypted_string = m1_decrypted.decode('utf-8')
print("Bob decrypted Alice's message: ", m1_decrypted_string)
m2_decrypted = cbc_decrypt(encrypted_m2, k, iv)
m2_decrypted_string = m2_decrypted.decode('utf-8')
print("Alice decrypted Bob's message: ", m2_decrypted_string)

# mallory decrypt with cbc
secret_key = str(s_mal).encode('utf-8')
k = hashlib.sha256(secret_key).digest()[:16]
mal_decrypted1 = cbc_decrypt(encrypted_m1, k, iv)
mal_decrypted_string1 = mal_decrypted1.decode('utf-8')
mal_decrypted2 = cbc_decrypt(encrypted_m2, k, iv)
mal_decrypted_string2 = mal_decrypted2.decode('utf-8')
print("Mallory decrypted Alice's message: ", mal_decrypted_string1)
print("Mallory decrypted Bob's's message: ", mal_decrypted_string2)


# mallory tampering with alpha:
# if a is 1, it will be 1
# if a is q, it will be 0
# if a is q - 1 then if x is even you get 1, if x is odd you get q - 1
