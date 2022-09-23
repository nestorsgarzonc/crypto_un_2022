from typing import List
import numpy as np


class Hole:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def __repr__(self):
        return f"Hole({self.row}, {self.column})"

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __hash__(self):
        return hash((self.row, self.column))


class TurningGrille:
    def __init__(self):
        self.holes: List[Hole] = []

    def set_holes(self, number_holes: int) -> None:
        for i in range(number_holes):
            print('Enter the coordinates of the hole #', i + 1)
            row = int(input('Row = '))
            column = int(input('Column = '))
            self.holes.append(Hole(row, column))

    def set_matrix_size(self, size: int) -> None:
        self.matrix_size = size
        self.matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=str)

    def process_text(self, text: str) -> None:
        text_upper = text.upper()
        splitted_text = text_upper.split()
        joined_text = ''.join(splitted_text)
        self.text = joined_text
        arr_text = []
        for i in range(0, len(self.text), self.matrix_size):
            arr_text.append(self.text[i:i + self.matrix_size])
        if len(arr_text[-1]) < self.matrix_size:
            arr_text[-1] += 'X' * (self.matrix_size - len(arr_text[-1]))
        self.arr_text = arr_text

    def fill_matrix(self) -> None:
        for i in range(len(self.holes)):
            self.matrix[self.holes[i].row][self.holes[i].column] = self.text[i]
        print(self.matrix)


tg = TurningGrille()
tg.set_holes(4)
tg.set_matrix_size(4)
tg.process_text("JIM ATTACKS AT DAWNN")
tg.fill_matrix()
