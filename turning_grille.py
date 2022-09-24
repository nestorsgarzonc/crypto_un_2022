import numpy as np


class TurningGrille:
    def __init__(self):
        self.start_program()

    def start_program(self) -> None:
        selected_mode = self.select_mode()
        while selected_mode != 3:
            if self.validate_options(selected_mode):
                print("Invalid option")
                selected_mode = self.select_mode()
                continue
            if selected_mode == 1:
                self.encrypt()
            elif selected_mode == 2:
                self.decrypt()
            selected_mode = self.select_mode()

    def validate_options(self, option: int) -> bool:
        return option < 1 or option > 3

    def select_mode(self):
        print("Select mode:")
        print("1 - Encrypt")
        print("2 - Decrypt")
        print("3 - Exit")
        mode = int(input(">> "))
        return mode

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
        arr_text = []
        self.rotation_count = 0
        self.text = joined_text
        for i in range(0, len(self.text), self.matrix_size):
            arr_text.append(self.text[i:i + self.matrix_size])
        if len(arr_text[-1]) < self.matrix_size:
            arr_text[-1] += 'X' * (self.matrix_size - len(arr_text[-1]))
        self.text = ''.join(arr_text)
        self.arr_text = arr_text

    def fill_matrix(self, orientation=1) -> None:
        counter = 0
        number_rotations = min(1, self.rotation_count)*orientation
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
        orientation = int(
            input('Enter the orientation of the grille (left 1 or right -1): '))
        if orientation != 1 and orientation != -1:
            print('Invalid orientation')
            return
        for _ in range(4):
            self.fill_matrix(orientation=orientation)
        print(self.numpy_arr_to_str(self.matrix))

    def fill_matrix_cipher(self):
        counter = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = self.text[counter]
                counter += 1

    def fill_matrix_dec(self, orientation=1) -> None:
        counter = 0
        number_rotations = min(1, self.rotation_count)*orientation
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
        orientation = int(
            input('Enter the orientation of the grille (left 1 or right -1): '))
        if orientation != 1 and orientation != -1:
            print('Invalid orientation')
            return
        for _ in range(4):
            plain_text += self.fill_matrix_dec(orientation=orientation)
        print(plain_text)


tg = TurningGrille()
#
# TESHN INCIG LSRGY LRIUS PITSA TLILM REENS ATTOG SIAWG IPVER TOTEH HVAEA XITDT UAIME RANPM TLHIE
