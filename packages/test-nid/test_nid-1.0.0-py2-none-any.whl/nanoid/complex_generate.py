from random import SystemRandom


def complex_generate(alphabet, size):
    alphabet_len = len(alphabet)
    random_bytes = SystemRandom(alphabet_len)

    id = ''
    for _ in range(size):
        byte = random_bytes.randrange(alphabet_len)

        id += alphabet[byte]

        if len(id) == size:
            return id
