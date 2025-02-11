from typing import List


def matrix_multiply(
    matrix_1: List[List[int]], matrix_2: List[List[int]]
) -> List[List[int]]:
    """
    Use multiplication of two matrices.

      >>> matrix_multiply([[1, 2], [3, 4]], [[5, 6],[7,8]])
      [[19, 22], [43, 50]]

      >>> matrix_multiply([[1,2,3],[4,5,6]], [[7,8],[9,1],[2,3]])
      [[31, 19], [85, 55]]

    """
    cols_matrix_1 = len(matrix_1[0])
    rows_matrix_2 = len(matrix_2)
    if cols_matrix_1 != rows_matrix_2:
        raise ValueError(
            "The number of columns of the first matrix must be equal to the number of rows of the second matrix"
        )

    rows_matrix_1 = len(matrix_1)
    cols_matrix_2 = len(matrix_2[0])

    return [
        [
            sum(matrix_1[i][k] * matrix_2[k][j] for k in range(cols_matrix_1))
            for j in range(cols_matrix_2)
        ]
        for i in range(rows_matrix_1)
    ]


def transpose_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Transpose the matrix

      >>> transpose_matrix([[1, 2], [3, 4]])
      [[1, 3], [2, 4]]

      >>> transpose_matrix([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
      [[1, 6], [2, 7], [3, 8], [4, 9], [5, 10]]

      >>> transpose_matrix([[7]])
      [[7]]
    """
    return list(map(list, zip(*matrix)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
