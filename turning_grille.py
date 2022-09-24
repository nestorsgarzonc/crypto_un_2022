import numpy as np


class TurningGrille:
    def __init__(self, is_test=False):
        self.is_test = is_test

    def set_holes(self, number_holes: int) -> None:
        self.number_holes = number_holes
        self.holes_rot = np.zeros(
            (self.matrix_size, self.matrix_size), dtype=str)
        if self.is_test:
            self.holes_rot[0][0] = 'X'
            self.holes_rot[2][1] = 'X'
            self.holes_rot[2][3] = 'X'
            self.holes_rot[3][2] = 'X'
            return
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
        arr_text = []
        self.rotation_count = 0
        self.text = joined_text
        for i in range(0, len(self.text), self.matrix_size):
            arr_text.append(self.text[i:i + self.matrix_size])
        if len(arr_text[-1]) < self.matrix_size:
            arr_text[-1] += 'X' * (self.matrix_size - len(arr_text[-1]))
        self.text = ''.join(arr_text)
        self.arr_text = arr_text

    def fill_matrix(self) -> None:
        counter = 0
        number_rotations = min(1, self.rotation_count)
        self.holes_rot = np.rot90(self.holes_rot, number_rotations)
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                if self.holes_rot[i][j] != '':
                    text_to_add = self.text[(
                        self.rotation_count*self.number_holes)+counter
                    ]
                    self.holes_rot[i][j] = text_to_add
                    counter += 1
        self.rotation_count += 1
        self.matrix = np.core.defchararray.add(self.matrix, self.holes_rot)

    def numpy_arr_to_str(self, arr) -> str:
        string = ''
        for i in arr:
            for j in i:
                string += j
        return string

    def encrypt(self):
        matrix_size = int(input('Enter the size of the matrix: '))
        self.set_matrix_size(matrix_size)
        holes_number = int(input('Enter the number of holes: '))
        self.set_holes(holes_number)
        text = input('Enter the text to encrypt: ')
        self.process_text(text)
        for _ in range(4):
            self.fill_matrix()
        print(self.numpy_arr_to_str(self.matrix))

    def fill_matrix_cipher(self):
        counter = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = self.text[counter]
                counter += 1

    def fill_matrix_dec(self) -> None:
        counter = 0
        number_rotations = min(1, self.rotation_count)
        self.holes_rot = np.rot90(self.holes_rot, number_rotations)
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                if self.holes_rot[i][j] != '':
                    self.holes_rot[i][j] = self.matrix[i][j]
                    counter += 1
        self.rotation_count += 1
        return self.numpy_arr_to_str(self.holes_rot)

    def decrypt(self):
        matrix_size = int(input('Enter the size of the matrix: '))
        self.set_matrix_size(matrix_size)
        holes_number = int(input('Enter the number of holes: '))
        self.set_holes(holes_number)
        text = input('Enter the text to encrypt: ')
        self.process_text(text)
        self.fill_matrix_cipher()
        plain_text = ''
        for _ in range(4):
            plain_text += self.fill_matrix_dec()
        print(plain_text)


tg = TurningGrille()
tg.decrypt()
#
# TESHN INCIG LSRGY LRIUS PITSA TLILM REENS ATTOG SIAWG IPVER TOTEH HVAEA XITDT UAIME RANPM TLHIE
