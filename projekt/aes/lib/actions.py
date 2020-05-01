"""Main action functions."""

import secrets

from lib.aes import actions, constants, entities


def decrypt(file_path, key_file):
    """Decrypts file with given key."""
    key = entities.get_key(key_file)
    key_schedule = entities.get_key_schedule(key)

    offset = 0
    while True:
        state = entities.read_state(file_path, offset)
        if state is None:
            break

        actions.decrypt(state, key_schedule, rounds=constants.ROUNDS[key.size])
        entities.write_state(state, file_path, offset)

        offset += 16


def encrypt(file_path, key_file):
    """Encrypts file with given key."""
    key = entities.get_key(key_file)
    key_schedule = entities.get_key_schedule(key)

    offset = 0
    while True:
        state = entities.read_state(file_path, offset)
        if state is None:
            break

        actions.encrypt(state, key_schedule, rounds=constants.ROUNDS[key.size])
        entities.write_state(state, file_path, offset)

        offset += 16


def generate(key_file, key_size):
    """Generates key for further usage."""
    with open(key_file, 'wb') as file:
        file.write(secrets.token_bytes(key_size >> 3))
