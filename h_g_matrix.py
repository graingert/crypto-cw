from __future__ import print_function

import sys
from contextlib import closing

import numpy as np
from oct2py import octave as oc
from six import StringIO


def format_int_matrix(m):
    with closing(StringIO()) as out:
        for row in m.astype(dtype=int):
            for item in row:
                out.write(str(item))
            out.write('\n')
        return out.getvalue()


if __name__ == "__main__":
    h, g = oc.hammgen(6, np.array((1, 1, 0, 0, 0, 0, 1), dtype=np.float))
    if sys.argv[1] == "h":
        print(format_int_matrix(h))
    elif sys.argv[1] == "g":
        print(format_int_matrix(g))
