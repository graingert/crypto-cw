from itertools import islice, product
from bitarray import bitarray
import json

from lfsr import LfsrRandom

#cypher = bytearray(b'\xd1\xc1')
cypher = bytearray(json.load(open("cypher.json")))
plaintext = bytearray(b"Ur")


def xor_bytearray(first, second):
    return bytearray((x ^ y for x, y in zip(first, second)))

target = bitarray(xor_bytearray(cypher, plaintext))

cypher_bits = len(cypher) * int(255).bit_length()


for charis, state in product(xrange(0b10000, 0b11111),xrange(0b00001, 0b01111)):
    if bitarray(islice(LfsrRandom(charis, state), 2)) == target:
        print charis, state
        try:
            keystream = bytearray(
                bitarray(
                    islice(LfsrRandom(charis, state), cypher_bits)
                ).tostring()
            )

            xor_bytearray(cypher, keystream).decode('ascii')
            print "ding:", charis, state
        except:
            pass
