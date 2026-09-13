"""Check Problem 4 using linear programs and exact covering counts.

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

        # Equivalent multiset certificate for the proof's two counting inequalities.
        allowed = {frozenset(cells) for cells in placements}
        selected = []
        for col in range(0, n, 2):
            for row in range(2):
                for shape in SHAPES[:2]:
                    selected.append([(row + a, col + b) for a, b in shape])
        assert len(selected) == 2 * n

        corners = {(r, c) for r in (0, 3) for c in (0, n - 1)}
        whole_board = {(r, c) for r in range(4) for c in range(n)}
        for pair_index in range(k):
            packing = []
            for strip_index in range(k - 1):
                col = 2 * strip_index
                bottom_col = col if strip_index < pair_index else col + 2
                upper = [(0, col + 1), (0, col + 2),
                         (1, bottom_col), (1, bottom_col + 1)]
                packing.extend([upper, [(3 - r, c) for r, c in upper]])
            holes = corners | {(r, c) for r in (1, 2)
                               for c in (2 * pair_index, 2 * pair_index + 1)}
            covered = [cell for shape in packing for cell in shape]
            assert len(packing) == n - 2
            assert len(covered) == len(set(covered))
            assert set(covered) == whole_board - holes
            selected.extend(packing * 2)

        assert len(selected) == n * n
        counts = {(r, c): 0 for r, c in whole_board}
        for shape in selected:
            assert frozenset(shape) in allowed
            for cell in shape:
                counts[cell] += 1
        assert all(count == (1 if cell in corners else n + 1)
                   for cell, count in counts.items())

    assert all(v >= 0 for row in construction for v in row)
    assert all(sum(construction[r][c] for r, c in cells) >= 1 for cells in placements)
    assert sum(sum(row) for row in construction) == expected
    assert abs(result.fun - float(expected)) < 1e-7
    print(f"n={n}: minimum={expected}; LP, exact construction and applicable double count OK")


if __name__ == "__main__":
    import sys
    for n in map(int, sys.argv[1:] or range(2, 21)):
        solve(n)
