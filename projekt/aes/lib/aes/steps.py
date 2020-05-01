"""AES methods."""

from lib.aes import constants, utils


def add_round_key(state, key_schedule, *, current_round):
    """The AddRoundKey step."""
    start, stop = 4 * current_round, 4 * (current_round + 1)

    for i, row in enumerate(state):
        state[i] = utils.xor_vectors(row, key_schedule[i][start:stop])


def mix_columns(state, *, inverse=False):
    """The MixColumns step."""
    if inverse:
        matrix = constants.INVERSE_MIX_COLUMNS
    else:
        matrix = constants.FORWARD_MIX_COLUMNS

    for j, column in enumerate(zip(*state)):
        new_column = utils.multiply_matrix_by_vector(matrix, column)
        for i, elem in enumerate(new_column):
            state[i][j] = elem


def shift_rows(state, *, inverse=False):
    """The ShiftRows step."""
    for i, row in enumerate(state):
        state[i] = utils.rot_word(row, inverse=inverse, times=i)


def sub_bytes(state, *, inverse=False):
    """The SubBytes step."""
    for i, row in enumerate(state):
        state[i] = utils.sub_word(row, inverse=inverse)
