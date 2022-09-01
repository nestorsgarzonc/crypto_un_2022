import numpy as np

DEFAULT_KEY = np.array([[11, 8], [3, 7]])
INITIAL_LETTER_ASCCI = 65
NUMBER_LETTERS = 26


class Hill:
    def __init__(self) -> None:
        self.start_program()

    def start_program(self) -> None:
        selected_mode = self.select_mode()
        while selected_mode != 3:
            if self.validate_options(selected_mode):
                print("Invalid option")
                selected_mode = self.select_mode()
                continue
            if selected_mode == 1:
                plaintext = input("Enter plaintext: ")
                key = self.input_and_process_key()
                print(
                    f'Encrypted text: {self.encrypt(key=key, plaintext=plaintext)}'
                )
            elif selected_mode == 2:
                ciphertext = input("Enter ciphertext: ")
                key = self.input_and_process_key()
                print(
                    f'Decrypted text: {self.decrypt(ciphertext=ciphertext, key=key)}'
                )
            selected_mode = self.select_mode()

    def input_and_process_key(self) -> str:
        print('Enter key:')
        key = []
        for i in range(2):
            print(f'Enter row {i+1} separated values by ",":')
            row = input('>> ')
            row = row.split(',')
            row = [int(i) for i in row]
            if(len(row) != 2):
                raise Exception('Invalid key format')
            key.append(row)
        return np.array(key)

    def validate_options(self, option: int) -> bool:
        return option < 1 or option > 3

    def select_mode(self):
        print("Select mode:")
        print("1 - Encrypt")
        print("2 - Decrypt")
        print("3 - Exit")
        mode = int(input(">> "))
        return mode

    def get_ascii_from_char(self, char: str) -> int:
        return ord(char) - INITIAL_LETTER_ASCCI

    def get_char_from_ascii(self, ascii: int) -> str:
        return chr(ascii + INITIAL_LETTER_ASCCI)

    def process_encryption_text(self, text: str):
        upper_text = text.upper()
        joined_text = ''.join(upper_text.split())
        if len(joined_text) % 2 != 0:
            joined_text += 'X'
        proccesed_text = []
        for i in range(0, len(joined_text), 2):
            proccesed_text.append([
                self.get_ascii_from_char(joined_text[i]),
                self.get_ascii_from_char(joined_text[i + 1])
            ])
        return np.array(proccesed_text)

    def encrypt(self, plaintext, key=DEFAULT_KEY) -> str:
        proccesed_text = self.process_encryption_text(plaintext)
        res_arr = np.array([])
        for i in proccesed_text:
            res_arr = np.append(res_arr, np.dot(i, key))
        res_arr = (res_arr.flatten() % NUMBER_LETTERS).astype(int)
        res_text = np.vectorize(self.get_char_from_ascii)(res_arr)
        return ''.join(res_text)

    def determinant_is_valid(self, determinant) -> bool:
        return determinant != 0

    def get_deternminant(self, matrix) -> int:
        return np.linalg.det(matrix).astype(int)

    def is_coprime(self, a, b) -> bool:
        return np.gcd(a, b) == 1

    def matrix_has_inverse_mod(self, matrix):
        determinant = self.get_deternminant(matrix)
        if(not self.determinant_is_valid(determinant)):
            print('Determinant is 0')
            return False
        elif(not self.is_coprime(determinant, NUMBER_LETTERS)):
            print(f'Determinant is not coprime with {NUMBER_LETTERS}')
            return False
        return True

    def process_key(self, key):
        det = 1/(self.get_deternminant(key) % NUMBER_LETTERS)
        adjoint = np.array([[key[1, 1], -key[0, 1]], [-key[1, 0], key[0, 0]]])
        res = det * adjoint
        return res

    def decrypt(self, ciphertext, key=DEFAULT_KEY) -> str:
        if(not self.matrix_has_inverse_mod(key)):
            return 'Invalid key'
        proccesed_text = self.process_encryption_text(ciphertext)
        res_arr = np.array([])
        proccesed_key_enc = self.process_key(key)
        for i in proccesed_text:
            res_arr = np.append(res_arr, np.dot(i, proccesed_key_enc))
        res_arr = (res_arr.flatten() % NUMBER_LETTERS).astype(int)
        res_text = np.vectorize(self.get_char_from_ascii)(res_arr)
        return ''.join(res_text)


if __name__ == '__main__':
    Hill()
