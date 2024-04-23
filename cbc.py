from ssl import RAND_bytes
from Crypto.Cipher import AES


def pad(data, block_size=16):
    padding_len = block_size - len(data) % block_size
    padding = bytes([padding_len] * padding_len)
    return data + padding


def unpad(data, block_size=16):
    # print("data to unpad:", data)
    # print("last byte:",data[-1])
    padding_len = data[-1]
    return data[:-padding_len]


def cbc_decrypt(encrypted_string, key, iv):

    cipher = AES.new(key, AES.MODE_ECB)

    decrypted_data = b''
    prev_block = iv

    for i in range(0, len(encrypted_string), 16):
        encrypted_block = encrypted_string[i:i+16]
        decrypted_block = cipher.decrypt(encrypted_block)
        # xor with previous block after decrypting
        decrypted_block = bytes(
            x ^ y for x, y in zip(decrypted_block, prev_block))
        decrypted_data += decrypted_block
        prev_block = encrypted_block

    decrypted_data = unpad(decrypted_data)
    # print("decrypted data:", decrypted_data)

    return decrypted_data


def cbc_encrypt(im, key, iv):

    cipher = AES.new(key, AES.MODE_ECB)
    padded_file = pad(im)

    encrypted_data = bytes()
    prev_block = iv
    # print("iv is type: ", type(iv))

    for i in range(0, len(padded_file), 16):
        block = padded_file[i:i+16]
        # xor with previous block before encrypting
        block = bytes(x ^ y for x, y in zip(block, prev_block))
        encrypted_block = cipher.encrypt(block)
        encrypted_data += encrypted_block
        prev_block = encrypted_block

    return encrypted_data
