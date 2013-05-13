def multiply_matrices(A, B, fieldSize=2):
    """
    multiply matrices over a particular finite field,
    as given in fieldSize.
    http://ze.phyr.us/matrix-multiplication-in-galois-fields-with-python
    """

    assert(len(A[0]) == len(B))

    C = [[0] * len(B[0]) for i in range(len(A))]

    for ci in range(len(C)):
        for cj in range(len(C[ci])):
            C[ci][cj] = sum([(A[ci][i] * B[i][cj]) for i in range(len(A[0]))])
            if fieldSize > 0:
                C[ci][cj] %= fieldSize
    return C