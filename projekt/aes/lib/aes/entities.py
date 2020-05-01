"""State and Key objects."""

import collections
import sys

from itertools import chain

from lib.aes import constants, utils


class _Key:  # pylint: disable=too-few-public-methods
    """Represents a secret key."""
    def __init__(self, data):
        self.data = data
        self.__size = None

    @property
    def size(self):
        """Key size in bits."""
        if self.__size is None:
            self.__size = len(self.data) << 3

        return self.__size

    @property
    def words(self):
        """Key size in 32-bit words."""
        return self.size >> 5


class _KeySchedule(collections.UserList):  # pylint: disable=too-many-ancestors
    """Represents key schedule."""
    def __init__(self, key):
        super().__init__()

        for i in range(4):
            self.data.append(list(key.data[i::4]))

        for i in range(4, 4 * (constants.ROUNDS[key.size] + 1)):
            word = utils.next_word(self.data, i, n_words=key.words)
            for j in range(4):
                self.data[j].append(word[j])


class _State(collections.UserList):  # pylint: disable=too-many-ancestors
    """Represents state to act over."""
    def __init__(self, data):
        super().__init__()

        for i in range(4):
            self.data.append(list(data[i::4]))


def get_key(key_file):
    """"Reads a key file."""
    with open(key_file, 'rb') as file:
        return _Key(file.read())


def get_key_schedule(key):
    """Returns keys schedule."""
    if not isinstance(key, _Key):
        key = get_key(key)

    return _KeySchedule(key)


def read_state(file_path, offset):
    """Reads state from file."""
    with open(file_path, 'rb') as file:
        file.seek(offset)
        data = file.read(16)
        if data:
            return _State(data.ljust(16, b'\0'))

        return None


def write_state(state, file_path, offset):
    """Writes state to file"""
    with open(file_path, 'rb+') as file:
        file.seek(offset)

        for i in chain.from_iterable(zip(*state)):
            file.write(i.to_bytes(1, sys.byteorder))
