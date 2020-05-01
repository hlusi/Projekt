"""
Functions that helps working with padding (bit padding) as described in
https://en.wikipedia.org/wiki/Padding_(cryptography)#Bit_padding.
"""


def add(file_path, size):
    """Adds padding."""
    with open(file_path, 'ab') as file:
        file.write(b'\x01')
        file.write(b'\x00' * (size - file.tell() % size))


def remove(file_path):
    """Removes padding."""
    cutoff = 1
    with open(file_path, 'ab+') as file:
        while True:
            file.seek(-cutoff, 2)
            char = file.read(1)
            if char == b'\x01':
                file.truncate(file.tell() - 1)
                break

            cutoff += 1
