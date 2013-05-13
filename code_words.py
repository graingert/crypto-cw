import numpy as np

from oct2py import octave as oc

from utils.matrix import multiply_matrices

h, g = oc.hammgen(6, np.array((1, 1, 0, 0, 0, 0, 1), dtype=np.float))

h = h.astype(dtype=int)

code_words = (
   "101001111000000000000000000000000000000000000000000000000000000",
   "100001100000000000000000000000000000000000000000000000001000011",
   "100001100000000000000000000010000000000000000000000000001000011"
)

for i, code_word in enumerate(code_words, start=1):
    cw = np.array(tuple(reversed(code_word)), dtype=int)
    cw = cw.reshape((len(cw), 1))
    if not any(np.array(multiply_matrices(h, cw)).T[0]):
        print "m{i} = {code_word} is a valid code word".format(
            i=i,
            code_word=code_word
        )
    else:
        print "m{i} = {code_word} is not a valid code word".format(
            i=i,
            code_word=code_word
        )
