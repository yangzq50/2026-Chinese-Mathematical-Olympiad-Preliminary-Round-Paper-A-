"""Small linear programs used to check the conjectured answer to Problem 4.

Run with: uv run --with scipy python check_s_shapes.py
This numerical check is supplementary; the PDF gives an exact proof.
"""

from fractions import Fraction

import numpy as np
from scipy.optimize import linprog


SHAPES = (
    ((0, 0), (1, 0), (1, 1), (2, 1)),
    ((0, 1), (1, 1), (1, 0), (2, 0)),
    ((0, 0), (0, 1), (1, 1), (1, 2)),
    ((0, 1), (0, 2), (1, 0), (1, 1)),
)


def solve(n):
    assert n >= 2
    rows, placements = [], []
    for shape in SHAPES:
        for r in range(4 - max(a for a, b in shape)):
            for c in range(n - max(b for a, b in shape)):
                row = np.zeros(4 * n)
                cells = [(r + a, c + b) for a, b in shape]
                for a, b in cells:
                    row[a * n + b] = 1
                rows.append(row)
                placements.append(cells)
    matrix = np.array(rows)
    result = linprog(np.ones(4 * n), A_ub=-matrix, b_ub=-np.ones(len(rows)), bounds=(0, None))
    assert result.success, result.message
    if n % 2:
        expected = Fraction(n - 1)
        construction = [[Fraction(c % 2, 2) for c in range(n)] for _ in range(4)]
    else:
        k = n // 2
        expected = Fraction(n * n, n + 1)
        outer = [Fraction((c // 2 if c % 2 == 0 else k - 1 - c // 2), n + 1)
                 for c in range(n)]
        inner = [v + Fraction(1, n + 1) for v in outer]
        construction = [outer, inner, inner, outer]

        # Exact expansion of the weighted identity in the written proof.
        coefficients = [0] * (2 * n)

        def add(weight, cells):
            for kind, col in cells:
                coefficients[kind * n + col - 1] += weight

        for r in range(1, k + 1):
            j = 2 * r - 1
            add(1, [(0, j), (1, j), (1, j + 1), (1, j + 1)])
            add(1, [(1, j), (1, j), (0, j + 1), (1, j + 1)])
        for r in range(1, k):
            j = 2 * r
            add(2 * r, [(0, j), (0, j + 1), (1, j + 1), (1, j + 2)])
            j = 2 * r - 1
            add(2 * (k - r), [(1, j), (1, j + 1), (0, j + 1), (0, j + 2)])
        assert coefficients == [1] + [n + 1] * (n - 2) + [1] + [n + 1] * n

    assert all(v >= 0 for row in construction for v in row)
    assert all(sum(construction[r][c] for r, c in cells) >= 1 for cells in placements)
    assert sum(sum(row) for row in construction) == expected
    assert abs(result.fun - float(expected)) < 1e-7
    print(f"n={n}: minimum={expected}; LP, exact construction and applicable weighted identity OK")


if __name__ == "__main__":
    import sys
    for n in map(int, sys.argv[1:] or range(2, 21)):
        solve(n)
