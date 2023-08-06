# coding: utf-8

from lookalikes import lookalikes
from lowercase import lowercase
from numbers import numbers
from prevent_misreadings import prevent_misreadings
from uppercase import uppercase

__all__ = ['alphabet_std', 'human_alphabet']

alphabet_std = '_-' + numbers + lowercase + uppercase
human_alphabet = prevent_misreadings(alphabet_std, lookalikes)
