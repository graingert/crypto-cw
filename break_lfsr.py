from __future__ import print_function, division

import binascii
import sys

from itertools import islice, product

from utils.wrapped_bitarray import bitarray
from utils.lfsr import LfsrRandom


def byte_to_unicode(byte):
    try:
        return byte.decode('ascii')
    except UnicodeDecodeError:
        return " 0x" + binascii.hexlify(byte).upper() + " "


def brute_force_LFSR(cypher, plaintext):
    target = cypher[:len(plaintext)] ^ plaintext

    # generator of all possible LFSRs
    possible_lfsr = product(
        xrange(0b100000, 0b111111+1),
        xrange(0b000001, 0b111111+1)
    )

    for charis, state in possible_lfsr:
        # create as much key as we have plaintext
        key = bitarray(islice(LfsrRandom(charis, state), len(plaintext)))
        if key == target:
            keystream = bitarray(
                islice(LfsrRandom(charis, state), len(cypher))
            )
            # if the key matches the target we return the byte stream
            return (cypher ^ keystream).tobytes()

if __name__ == "__main__":
    cypher = bitarray.fromfile(open(sys.argv[1], 'r+b'))
    plaintext = bitarray.frombytes(bytes(sys.argv[2]))
    plain = brute_force_LFSR(cypher, plaintext)

    # print the output, with any non ascii characters as hex
    print(''.join(map(byte_to_unicode, plain)))
