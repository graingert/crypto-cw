from __future__ import print_function

from functools import partial
from six.moves import map

import numpy as np
from oct2py import Oct2Py, Oct2PyError

from utils.wrapped_bitarray import bitarray

oc = Oct2Py()

pols = np.array((
    (1, 1, 1, 1, 0, 0, 1),
    (1, 0, 0, 1, 1, 1, 1),
    (0, 0, 0, 0, 0, 1, 1),
    (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 0, 0, 0, 0, 1)
), dtype=np.float)

function_style = "f{i}(x), ({pol})"

for i, pol in enumerate(pols, start=1):
    f = function_style.format(i=i, pol=pol)
    try:
        oc.hammgen(6, pol)
        print (f+" is a generator polynomial for a Hamming code")
    except Oct2PyError:
        print (f+" is not a generator polynomial for a Hamming code")


h, g = oc.hammgen(6, np.array((1, 1, 0, 0, 0, 0, 1), dtype=np.float))

print(("h matrix", h))
print(("g matrix", g))


code_words = np.array((
    tuple("101001111000000000000000000000000000000000000000000000000000000"),
    tuple("100001100000000000000000000000000000000000000000000000001000011"),
    tuple("100001100000000000000000000010000000000000000000000000001000011")
), dtype=float)