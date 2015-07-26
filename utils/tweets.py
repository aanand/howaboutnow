from itertools import takewhile, dropwhile


def extract_query(text):
    words = text.split()
    words = dropwhile(is_not_word, words)
    words = takewhile(is_word, words)
    words = list(words)

    return " ".join(words) if words else None


def is_word(word):
    return not word.startswith('@') and not word.startswith('http')


def is_not_word(word):
    return not is_word(word)
