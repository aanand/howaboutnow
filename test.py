import sys

from utils.images import search, debug


def main():
    query = sys.argv[1]
    then = search(query, 2000, 2010)
    now = reversed(search(query, 2010, 2020))

    print('Then:\n')
    debug(then)

    print('\n===============\n\n')

    print('Now:\n')
    debug(now)


if __name__ == '__main__':
    main()
