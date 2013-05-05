from __future__ import print_function, division

import sys
import string
from itertools import chain

from utils.wrapped_bitarray import bitarray

valid_chars = frozenset(chain(
    string.ascii_lowercase,
    string.ascii_uppercase,
    " ,.")
)

first_bits_key = bitarray('100001001011001111100011')


def bruteforce_last_byte(cypher):
    for i in range(2**8):
        key = first_bits_key.copy()
        key.frombytes(chr(i))
        keystream = key * int(len(cypher)/len(key))
        plaintext = (cypher ^ keystream).tobytes()
        if valid_chars.issuperset(plaintext):
            yield {
                "key": key,
                "keystream": keystream,
                "plaintext": plaintext
            }

if __name__ == "__main__":
    cypher = bitarray.fromfile(open(sys.argv[1], 'r+b'))
    for key in bruteforce_last_byte(cypher):
        print(key["plaintext"])
