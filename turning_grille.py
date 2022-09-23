from typing import List
import numpy as np


class TurningGrille:
    def __init__(self):
        pass

    def set_holes(self, number_holes: int) -> None:
        self.number_holes = number_holes
        self.holes_rot = np.zeros(
            (self.matrix_size, self.matrix_size), dtype=str)
        for i in range(number_holes):
            print('Enter the coordinates of the hole #', i + 1)
            row = int(input('Row = '))
            column = int(input('Column = '))
            self.holes_rot[row][column] = 'X'

    def set_matrix_size(self, size: int) -> None:
        self.matrix_size = size
        self.matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=str)

    def process_text(self, text: str) -> None:
        text_upper = text.upper()
        splitted_text = text_upper.split()
        joined_text = ''.join(splitted_text)
        self.text = joined_text
        arr_text = []
        self.rotation_count = 0
        for i in range(0, len(self.text), self.matrix_size):
            arr_text.append(self.text[i:i + self.matrix_size])
        if len(arr_text[-1]) < self.matrix_size:
            arr_text[-1] += 'X' * (self.matrix_size - len(arr_text[-1]))
        self.arr_text = arr_text

    def fill_matrix(self) -> None:
        counter = 0
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                if self.holes_rot[i][j] != '':
                    text_to_add = self.text[(
                        self.rotation_count*self.number_holes)+counter
                    ]
                    print(text_to_add, end='')
                    self.holes_rot[i][j] = text_to_add
                    counter += 1
        self.holes_rot = np.rot90(self.holes_rot, self.rotation_count)
        self.rotation_count += 1
        self.matrix = np.core.defchararray.add(self.matrix, self.holes_rot)



tg = TurningGrille()
tg.set_matrix_size(4)
tg.set_holes(4)
tg.process_text("JIM ATTACKS AT DAWN")
for i in range(4):
    tg.fill_matrix()
