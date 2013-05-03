from __future__ import print_function, division

from itertools import islice, product, chain, repeat
from bitarray import bitarray as sub_bitarray
from collections import Counter
from operator import itemgetter

import binascii

from lfsr import LfsrRandom

import string

import numpy as np
import matplotlib.pyplot as plt

from six import iteritems, with_metaclass


class FromFactoryer(type):
    def __getattribute__(cls, attr):
        if attr.startswith("from") and hasattr(getattr(cls(), attr, None), '__call__'):
            def wrapped(*args, **kwargs):
                bit = cls()
                getattr(bit, attr)(*args, **kwargs)
                return bit

            return wrapped
            # Default behaviour
        return super(FromFactoryer, cls).__getattribute__(attr)


class bitarray(with_metaclass(FromFactoryer, sub_bitarray)):
    pass


#cypher = bytearray(b'\xd1\xc1')
cypher = bitarray.fromfile(open('cypher.bin', 'r+b'))
plaintext = bitarray.frombytes(b"Ur")

"""
def auto_correlate(bits):
    bits_copy = bits.copy()
    while len(bits_copy):
        bits_copy.pop()
        yield bitarray.bitdiff(bits, bits_copy)
"""

target = cypher[:len(plaintext)] ^ plaintext

print(plaintext)
print(cypher[:len(plaintext)])
print(target)


def byte_to_unicode(byte):
    try:
        return byte.decode('ascii')
    except UnicodeDecodeError:
        return "0x" + binascii.hexlify(byte).upper()


def brute_force_LFSR():
    for charis, state in product(xrange(0b100000, 0b111111+1), xrange(0b000001, 0b111111+1)):
        if bitarray(islice(LfsrRandom(charis, state), len(plaintext))) == target:
            print(charis, state)
            keystream = bitarray(
                islice(LfsrRandom(charis, state), len(cypher))
            )

            plain = (cypher ^ keystream).tobytes()
            counts_labels = sorted(
                iteritems(Counter(plain)),
                key=itemgetter(1),
                reverse=True
            )
            counts = np.empty(len(counts_labels), dtype=np.int16)
            labels = []
            for (i, (char, count)) in enumerate(counts_labels):
                counts[i] = count
                labels.append(char)

            width = 0.8
            ind = np.arange(len(counts_labels))

            plt.bar(ind, counts, width=width)

            plt.ylabel('Frequency')
            plt.xlabel('Byte')
            plt.title('Byte Frequency')
            plt.xticks(ind+(width/2), map(byte_to_unicode, labels))
            plt.show()

valid_chars = frozenset(chain(string.ascii_lowercase, string.ascii_uppercase, " ,."))

keys = []

for i in range(2**8):
    key = bitarray(islice(LfsrRandom(47, 3), 3*8))
    key.frombytes(chr(i))
    keystream = key * int(len(cypher)/len(key))
    plaintext = (cypher ^ keystream).tobytes()
    if valid_chars.issuperset(plaintext):
        keys.append({
            "key": key,
            "keystream": keystream,
            "plaintext": plaintext

        })

for key in keys:
    print(key["key"])
    print(key["plaintext"])
