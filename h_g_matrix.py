import numpy as np

from oct2py import Oct2Py

oc = Oct2Py()


def multiply_matrices(A, B, fieldSize=2):
    """http://ze.phyr.us/matrix-multiplication-in-galois-fields-with-python"""
    assert(len(A[0]) == len(B))  # The number of columns of A must equal the number of rows of B

    # Prepare an empty matrix with |rows(A)| rows and |columns(B)| columns.
    C = [[0] * len(B[0]) for i in range(len(A))]

    for ci in range(len(C)):
        for cj in range(len(C[ci])):
            C[ci][cj] = sum([(A[ci][i] * B[i][cj]) for i in range(len(A[0]))])
            if fieldSize > 0:
                C[ci][cj] %= fieldSize
    return C


h, g = oc.hammgen(6, np.array((1, 1, 0, 0, 0, 0, 1), dtype=np.float))

print(("h matrix", h))
print(("g matrix", g))


code_words = np.array((
    tuple("101001111000000000000000000000000000000000000000000000000000000"),
    tuple("100001100000000000000000000000000000000000000000000000001000011"),
    tuple("100001100000000000000000000010000000000000000000000000001000011")
), dtype=float)
