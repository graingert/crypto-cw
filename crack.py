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


print plaintext
print target
print cypher[:len(plaintext)]

for charis, state in product(xrange(0b10000, 0b11111), xrange(0b00001, 0b01111)):
    keystream = bitarray(islice(LfsrRandom(charis, state), len(plaintext)))
    if keystream == target:
        print charis, state
        keystream = bitarray(
            islice(LfsrRandom(charis, state), len(cypher))
        )

        print (cypher ^ keystream).tobytes()
