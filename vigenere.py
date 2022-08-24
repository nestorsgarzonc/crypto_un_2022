from math import ceil
from typing import List


class Vigenere:
    def __init__(self) -> None:
        self.tableau = self.build_tableau()
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
                t = int(input("Enter t: "))
                key = input("Enter key: ")
                print(
                    f'Encrypted text: {self.encrypt(key=key, t=t, plaintext=plaintext)}'
                )
            elif selected_mode == 2:
                ciphertext = input("Enter ciphertext: ")
                t = int(input("Enter t: "))
                key = input("Enter key: ")
                print(
                    f'Decrypted text: {self.decrypt(ciphertext=ciphertext, key=key, t=t)}'
                )
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

    def build_tableau(self) -> List[List[str]]:
        tableau = []
        for i in range(26):
            aux_tableau = []
            for j in range(i, i+26):
                aux_tableau.append(chr((j % 26)+65))
            tableau.append(aux_tableau)
        return tableau

    def print_pretty_tableau(self) -> None:
        for i in self.tableau:
            print(' | '.join(i))

    def process_text(self, text: str, t: int) -> List[str]:
        upper_text = text.upper()
        spplitted_text = upper_text.split()
        joined_text = ''.join(spplitted_text)
        processed_text = []
        for i in range(0, len(joined_text), t):
            processed_text.append(joined_text[i:i+t])
        return processed_text

    def process_key(self, key: str, processed_text: str, t: int) -> List[str]:
        text_len = len(processed_text)
        key_len = len(key)
        n_key_in_text = ceil(text_len/key_len)
        key_repeated = (key * n_key_in_text)[:text_len]
        return self.process_text(key_repeated, t)

    def search_row_loc(self, value: str) -> int:
        for i in range(len(self.tableau)):
            if value == self.tableau[0][i]:
                return i
        raise Exception("Value not found")

    def search_column_loc(self, value: str) -> int:
        for i in range(len(self.tableau)):
            if value == self.tableau[i][0]:
                return i
        raise Exception("Value not found")

    def search_intersection_loc(self, cipher_val: str, row_pos: int) -> int:
        for i in range(len(self.tableau[row_pos])):
            if cipher_val == self.tableau[i][row_pos]:
                return i
        raise Exception("Value not found")

    def get_enc_intersection_letter(self, key_val: str, plaintext_val: str) -> str:
        row_loc = self.search_row_loc(key_val)
        col_loc = self.search_column_loc(plaintext_val)
        return self.tableau[col_loc][row_loc]

    def get_dec_intersection_letter(self, key_val: str, ciphertext_val: str) -> str:
        row_loc = self.search_row_loc(key_val)
        col_loc = self.search_intersection_loc(ciphertext_val, row_pos=row_loc)
        return self.tableau[col_loc][0]

    def encrypt(self, plaintext: str, key: str, t: int) -> str:
        processed_text_arr = self.process_text(plaintext, t)
        processed_text = ''.join(processed_text_arr)
        processed_key_arr = self.process_key(key, processed_text, t)
        encrypted_arr = []
        for i in range(len(processed_text_arr)):
            group_arr = ''
            for j in range(len(processed_text_arr[i])):
                intersection = self.get_enc_intersection_letter(
                    key_val=processed_key_arr[i][j],
                    plaintext_val=processed_text_arr[i][j]
                )
                group_arr += intersection
            encrypted_arr.append(group_arr)
        return ' '.join(encrypted_arr)

    def decrypt(self, ciphertext: str, key: str, t: int) -> List[str]:
        processed_text_arr = self.process_text(ciphertext, t)
        processed_key_arr = self.process_key(key, ciphertext, t)
        decrypted_arr = []
        for i in range(len(processed_text_arr)):
            group_arr = ''
            for j in range(len(processed_text_arr[i])):
                intersection = self.get_dec_intersection_letter(
                    key_val=processed_key_arr[i][j],
                    ciphertext_val=processed_text_arr[i][j]
                )
                group_arr += intersection
            decrypted_arr.append(group_arr)
        return ' '.join(decrypted_arr)


if __name__ == "__main__":
    Vigenere()
