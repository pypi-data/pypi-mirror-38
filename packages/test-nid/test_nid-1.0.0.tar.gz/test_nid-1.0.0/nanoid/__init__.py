from complex_generate import complex_generate
from dictionary import alphabet_std
from non_secure_generate import non_secure_generate

__all__ = ['generate', 'fast_generate']


def generate(alphabet=alphabet_std, size=21):
    return complex_generate(alphabet, size)


def fast_generate(alphabet=alphabet_std, size=21):
    return non_secure_generate(alphabet, size)
