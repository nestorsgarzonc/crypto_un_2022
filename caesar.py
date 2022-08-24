from typing import List


class Caesar:
    def __init__(self):
        selected_mode = self.select_mode()
        while selected_mode != 3:
            if self.validate_options(selected_mode):
                print("Invalid option")
                selected_mode = self.select_mode()
                continue
            if selected_mode == 1:
                text = input("Enter text: ")
                rotation = int(input("Enter rotation: "))
                print(f'Encrypted text: {self.encrypt(text, rotation)}')
            elif selected_mode == 2:
                text = input("Enter text: ")
                rotation = int(input("Enter rotation: "))
                print(f'Decrypted text: {self.decrypt(text, rotation)}')
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

    def process_text(self, text: str) -> List[str]:
        text_upper = text.upper()
        splitted_text = text_upper.split()
        joined_text = ''.join(splitted_text)
        processed_text = []
        for i in range(0, len(joined_text), 5):
            processed_text.append(joined_text[i:i+5])
        return processed_text

    def decrypt(self, text: str, rotation: int) -> str:
        processed_text = self.process_text(text)
        decrypted_text = []
        for i in processed_text:
            aux_arr = []
            for letter in i:
                text_ascii = ord(letter)
                if text_ascii < 65 + rotation:
                    text_ascii += 26
                aux_arr.append(chr(text_ascii-rotation))
            decrypted_text.append("". join(aux_arr))
        return " ".join(decrypted_text)

    def encrypt(self, text: str, rotation: int) -> str:
        processed_text = self.process_text(text)
        encrypted_text = []
        for i in processed_text:
            aux_arr = []
            for letter in i:
                text_ascii = ord(letter)
                if text_ascii > 90 - rotation:
                    text_ascii -= 26
                aux_arr.append(chr(text_ascii+rotation))
            encrypted_text.append("". join(aux_arr))
        return " ". join(encrypted_text)


if __name__ == "__main__":
    Caesar()
