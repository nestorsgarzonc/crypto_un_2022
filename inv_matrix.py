from sympy import Matrix, pprint

A = Matrix([
    [14,  5],
    [9, 9],
])
A_inv = A.inv_mod(37)
pprint(A_inv)
