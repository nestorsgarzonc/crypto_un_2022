from typing import List

PADDING_LETTER = 'X'


class TableElement:
    def __init__(self, letter, alt_letter=None, row_location=None, column_location=None):
        self.letter = letter
        self.alt_letter = alt_letter
        self.row_location = row_location
        self.column_location = column_location

    def set_location(self, row_location: int, column_location: int) -> None:
        self.row_location = row_location
        self.column_location = column_location

    def get_only_letters(self):
        if self.alt_letter:
            return f'({self.letter}|{self.alt_letter})'
        return self.letter

    def __str__(self) -> str:
        return f'TableElement(letter: {self.letter}, alt_letter: {self.alt_letter}, column_location: {self.column_location}, row_location: {self.row_location}, )'

    def element_to_str(self) -> str:
        return f'{self.letter}{ f",{self.alt_letter}" if self.alt_letter else ""}{ f",{self.column_location},{self.row_location}" if self.row_location and self.column_location else ""}'

    def __repr__(self) -> str:
        return self.element_to_str()

    def __eq__(self, other) -> bool:
        return self.letter == other.letter and self.alt_letter == other.alt_letter

    def __hash__(self) -> int:
        return hash(self.element_to_str())


TABLE_ELEMENTS = [
    [
        TableElement('Y'),
        TableElement('O'),
        TableElement('A'),
        TableElement('N'),
        TableElement('P'),
    ],
    [
        TableElement('I', alt_letter='J'),
        TableElement('Z'),
        TableElement('B'),
        TableElement('C'),
        TableElement('D'),
    ],
    [
        TableElement('E'),
        TableElement('F'),
        TableElement('G'),
        TableElement('H'),
        TableElement('K'),
    ],
    [
        TableElement('L'),
        TableElement('M'),
        TableElement('Q'),
        TableElement('R'),
        TableElement('S'),
    ],
    [
        TableElement('T'),
        TableElement('U'),
        TableElement('V'),
        TableElement('W'),
        TableElement('X'),
    ],
]


class Playfair:
    def __init__(self, table_elements: List[List[TableElement]]):
        self.table_elements = table_elements
        self.rows = len(table_elements)-1
        self.columns = len(table_elements[0])-1

    def __str__(self) -> str:
        return f'Table(table_elements: {self.table_elements})'

    def print_table(self):
        for row in self.table_elements:
            for column in row:
                print(column.element_to_str(), end=' | ')
            print('')

    def add_padding(self, text: str) -> str:
        newText = text[0]
        for i in text[1:]:
            if newText[-1] == i:
                newText += PADDING_LETTER
            newText += i
        return newText

    def split_text_in_pairs(self, text: str) -> List[str]:
        splitted_text = []
        for i in range(0, len(text), 2):
            splitted_text.append(text[i:i+2])
        if len(splitted_text[-1]) == 1:
            splitted_text[-1] += PADDING_LETTER
        return splitted_text

    def process_dec_text(self, text: str) -> List[str]:
        if not text or text == '':
            raise ValueError('Text is empty ;(')
        alt_text = text.upper()
        padded_text = self.add_padding(alt_text)
        # Remove whitespaces
        joined_text = ''.join(padded_text.split())
        return self.split_text_in_pairs(joined_text)

    def process_enc_text(self, text: str) -> List[str]:
        if not text or text == '':
            raise ValueError('Text is empty ;(')
        alt_text = text.upper()
        joined_text = ''.join(alt_text.split())
        return self.split_text_in_pairs(joined_text)

    def get_letter_location(self, letter: str) -> TableElement:
        for col_idx, row in enumerate(self.table_elements):
            for row_idx, column in enumerate(row):
                if column.letter == letter or column.alt_letter == letter:
                    return TableElement(
                        letter=letter,
                        alt_letter=column.alt_letter,
                        column_location=col_idx,
                        row_location=row_idx
                    )
        raise ValueError(
            f'Letter {letter.element_to_str()} not found in table')

    def get_pair_letter_location(self, letters: str) -> List[TableElement]:
        if len(letters) != 2:
            raise ValueError('Should have two elements: ' + letters)
        return [self.get_letter_location(i) for i in letters]

    def exchange_validation(self, texts: List[TableElement]) -> None:
        if len(texts) != 2:
            raise ValueError('Should have two elements: ' + texts)
        for i in texts:
            if i.column_location == None:
                raise ValueError(
                    'Column location is None for element: ' + i.element_to_str())
            if i.row_location == None:
                raise ValueError(
                    'Row location is None for element: ' + i.element_to_str())

    def rows_exchange_enc(self, texts: List[TableElement]) -> List[TableElement]:
        self.exchange_validation(texts)
        return [self.row_exchange_enc(i) for i in texts]

    def row_exchange_enc(self, text: TableElement) -> TableElement:
        if text.row_location < self.rows:
            return self.table_elements[text.column_location][text.row_location+1]
        else:
            return self.table_elements[text.column_location][self.rows-text.row_location]

    def columns_exchange_enc(self, texts: List[TableElement]) -> List[TableElement]:
        self.exchange_validation(texts)
        return [self.column_exchange_enc(i) for i in texts]

    def column_exchange_enc(self, text: TableElement) -> TableElement:
        if text.column_location < self.columns:
            return self.table_elements[text.column_location+1][text.row_location]
        else:
            return self.table_elements[self.columns-text.column_location][text.row_location]

    def rows_exchange_dec(self, texts: List[TableElement]) -> List[TableElement]:
        self.exchange_validation(texts)
        return [self.row_exchange_dec(i) for i in texts]

    def row_exchange_dec(self, text: TableElement) -> TableElement:
        if text.row_location > 0:
            return self.table_elements[text.column_location][text.row_location-1]
        else:
            return self.table_elements[text.column_location][self.rows]

    def columns_exchange_dec(self, texts: List[TableElement]) -> List[TableElement]:
        self.exchange_validation(texts)
        return [self.column_exchange_dec(i) for i in texts]

    def column_exchange_dec(self, text: TableElement) -> TableElement:
        if text.column_location > 0:
            return self.table_elements[text.column_location-1][text.row_location]
        else:
            return self.table_elements[self.columns][text.row_location]

    def intersections_exchange(self, texts: List[TableElement]) -> List[TableElement]:
        self.exchange_validation(texts)
        first = self.table_elements[texts[0]
                                    .column_location][texts[1].row_location]
        second = self.table_elements[texts[1]
                                     .column_location][texts[0].row_location]
        return [first, second]

    def decrypt_pair(self, pair: List[TableElement]) -> List[TableElement]:
        if pair[0].row_location == pair[1].row_location:
            return self.columns_exchange_dec(pair)
        elif pair[0].column_location == pair[1].column_location:
            return self.rows_exchange_dec(pair)
        else:
            return self.intersections_exchange(pair)

    def encrypt_pair(self, pair: List[TableElement]) -> List[TableElement]:
        if pair[0].row_location == pair[1].row_location:
            return self.columns_exchange_enc(pair)
        elif pair[0].column_location == pair[1].column_location:
            return self.rows_exchange_enc(pair)
        else:
            return self.intersections_exchange(pair)

    def encrypt(self, text: str) -> str:
        processed_text = self.process_dec_text(text)
        letters_with_location = [
            self.get_pair_letter_location(i) for i in processed_text
        ]
        encrypted_text = ''
        for i in letters_with_location:
            org_str = ''
            for j in i:
                org_str += j.get_only_letters()
            enc = self.encrypt_pair(i)
            enc_str = ''
            for i in enc:
                enc_str += i.get_only_letters()
            encrypted_text += enc_str + ' '
        return encrypted_text

    def decrypt(self, text: str) -> str:
        processed_text = self.process_enc_text(text)
        letters_with_location = [
            self.get_pair_letter_location(i) for i in processed_text
        ]
        encrypted_text = ''
        for i in letters_with_location:
            org_str = ''
            for j in i:
                org_str += j.get_only_letters()
            enc = self.decrypt_pair(i)
            enc_str = ''
            for i in enc:
                enc_str += i.get_only_letters()
            encrypted_text += enc_str + ' '
        return encrypted_text


def get_table_from_input(columns=5) -> List[TableElement]:
    print("Enter table elements:")
    print("Example: J G H I J")
    print("If contains an alter letter write as follows: I|J G H I J")
    table = []
    for i in range(columns):
        print("Enter column", i+1, ":")
        row = []
        elements = input().split()
        for j in elements:
            if '|' in j:
                el = j.split('|')
                row.append(TableElement(el[0], el[1]))
            else:
                row.append(TableElement(j))
        table.append(row)
    return table


if __name__ == '__main__':
    choice = None
    while choice != 3:
        print('\nWELCOME TO THE PLAYFAIR CIPHER')
        print('1. Encrypt')
        print('2. Decrypt')
        print('3. Exit')
        choice = int(input('Enter your choice: '))
        if choice == 1:
            table = get_table_from_input()
            playfair = Playfair(table)
            playfair.print_table()
            text = input('Enter text to encrypt: ')
            print('Encrypted text: ' + playfair.encrypt(text))
        elif choice == 2:
            table = get_table_from_input()
            playfair = Playfair(table)
            playfair.print_table()
            text = input('Enter text to decrypt: ')
            print('Decrypted text: ' + playfair.decrypt(text))
        elif choice == 3:
            print('Goodbye :)')
        else:
            print('Invalid choice')
