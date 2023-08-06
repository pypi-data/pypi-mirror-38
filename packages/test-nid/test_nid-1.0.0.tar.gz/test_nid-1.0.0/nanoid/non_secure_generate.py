from random import random


def non_secure_generate(alphabet, size):
    alphabet_len = len(alphabet)

    id = ''
    for _ in range(size):
        byte = int(random() * alphabet_len)

        id += alphabet[byte]

        if len(id) == size:
            return id
