from __future__ import print_function

from itertools import islice, product
from bitarray import bitarray

import json

from lfsr import LfsrRandom


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


for charis, state in product(xrange(0b100000, 0b111111+1), xrange(0b000001, 0b011111+1)):
    if bitarray(islice(LfsrRandom(charis, state), len(plaintext))) == target:
        print(charis, state)
        keystream = bitarray(
            islice(LfsrRandom(charis, state), len(cypher))
        )

        print((cypher ^ keystream).tobytes())
