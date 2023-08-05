import sys
import random
import string
import argparse
from itertools import product, islice
from pprint import pprint as pp


exclude_words = ['pid']


def is_consonant(letter):
    return letter not in 'aeiou'


def name_filter(name):
    # Filter any double letters
    if any(x[0] == x[1] for x in zip(name, name[1:])):
        return False
    # Filter any double consonants
    if any(is_consonant(x[0]) and is_consonant(x[1]) for x in zip(name, name[1:])):
        return False
    return True


def name_generator(root_length):
    while True:
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(root_length))
        if name_filter(word):
            yield word


def get_names(root_length, suffix, n=10):
    sample = islice(name_generator(root_length), n)
    sample = [x + suffix for x in sample]
    return sample


def main():
    parser = argparse.ArgumentParser(description='Generate project/app names.')
    parser.add_argument('--root-length', type=int, default=3,
                        help='length of root word')
    parser.add_argument('--suffix', default='', help='specify a suffix')
    args = parser.parse_args()

    while True:
        pp(get_names(args.root_length, args.suffix))
        input()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
