from itertools import takewhile, dropwhile


def extract_query(text):
    words = text.split()
    words = dropwhile(is_username, words)
    words = takewhile(is_not_username, words)
    words = list(words)

    return " ".join(words) if words else None


def is_username(word):
    return word.startswith('@')


def is_not_username(word):
    return not is_username(word)
