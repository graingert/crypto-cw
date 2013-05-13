from __future__ import print_function

import numpy as np
from oct2py import octave as oc, Oct2PyError

pols = np.array((
    (1, 1, 1, 1, 0, 0, 1),
    (1, 0, 0, 1, 1, 1, 1),
    (0, 1, 0, 0, 0, 1, 1),
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
