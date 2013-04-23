from __future__ import print_function, division

from itertools import islice, product
from bitarray import bitarray
from collections import Counter
from operator import itemgetter

import binascii
import json

from lfsr import LfsrRandom

import numpy as np
import matplotlib.pyplot as plt

from six import iteritems


def bitarray_frombytes(some_bytes):
    ret = bitarray()
    ret.frombytes(some_bytes)
    return ret

#cypher = bytearray(b'\xd1\xc1')
cypher = bitarray_frombytes(bytes(bytearray(json.load(open("cypher.json")))))
plaintext = bitarray_frombytes(b"Ur")


target = cypher[:len(plaintext)] ^ plaintext

print(plaintext)
print(cypher[:len(plaintext)])
print(target)


def byte_to_unicode(byte):
    try:
        return byte.decode('ascii')
    except UnicodeDecodeError:
        return "0x" + binascii.hexlify(byte).upper()

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
