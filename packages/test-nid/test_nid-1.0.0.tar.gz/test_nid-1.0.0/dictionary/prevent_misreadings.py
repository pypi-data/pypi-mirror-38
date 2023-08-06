import re


def match_all_occurences(symbols):
    return '[%s]' % symbols


def prevent_misreadings(string, chars):
    return re.sub(match_all_occurences(chars), '', string, flags=re.IGNORECASE)
