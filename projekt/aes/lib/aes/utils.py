"""Helper utils."""

from lib.aes import constants


def _xtime(num):
    """Base multiplication function."""
    if num < 0x80:
        res = num << 1
    else:
        res = (num << 1) ^ 0x1b

    return res % 0x100


def _mul_by_03(num):
    """Helper function to multiply number by 0x03."""
    return _xtime(num) ^ num


def _mul_by_09(num):
    """Helper function to multiply number by 0x09."""
    return _xtime(_xtime(_xtime(num))) ^ num


def _mul_by_0b(num):
    """Helper function to multiply number by 0x0b."""
    return _xtime(_xtime(_xtime(num))) ^ _xtime(num) ^ num


def _mul_by_0d(num):
    """Helper function to multiply number by 0x0d."""
    return _xtime(_xtime(_xtime(num))) ^ _xtime(_xtime(num)) ^ num


def _mul_by_0e(num):
    """Helper function to multiply number by 0x0e."""
    return _xtime(_xtime(_xtime(num))) ^ _xtime(_xtime(num)) ^ _xtime(num)


_MUL_OPS_MAPPING = {
    0x01: lambda num: num,
    0x02: _xtime,
    0x03: _mul_by_03,
    0x09: _mul_by_09,
    0x0b: _mul_by_0b,
    0x0d: _mul_by_0d,
    0x0e: _mul_by_0e
}


def multiply_matrix_by_vector(matrix, vector):
    """Multiplies matrix by vector."""
    result = []

    for row in matrix:
        num = 0x00
        for elem, multiplier in zip(vector, row):
            num ^= _MUL_OPS_MAPPING[multiplier](elem)
        result.append(num)

    return result


def rot_word(word, *, inverse=False, times=1):
    """Helper function to rotate the word."""
    if inverse:
        direction = -1
    else:
        direction = 1

    split = times * direction
    return [*word[split:], *word[:split]]


def sub_word(word, *, inverse=False):
    """Helper function to substitute bytes in the word."""
    if inverse:
        sbox = constants.INVERSE_SBOX
    else:
        sbox = constants.FORWARD_SBOX

    return [sbox[b] for b in word]


def xor_vectors(*vectors):
    """Helper function to xor vectors."""
    if not vectors:
        return []

    result = vectors[0]
    for vector in vectors[1:]:
        result = [e1 ^ e2 for e1, e2 in zip(result, vector)]

    return result


def next_word(words, idx, *, n_words):
    """Returns next word for key expansion."""
    if not idx % n_words:
        vectors = (
            [word[idx - n_words] for word in words],
            sub_word(rot_word([word[idx - 1] for word in words])),
            [r[idx // n_words - 1] for r in constants.RCON],
        )
    elif n_words > 6 and idx % n_words == 4:
        vectors = (
            [word[idx - n_words] for word in words],
            sub_word([word[idx - 1] for word in words]),
        )
    else:
        vectors = (
            [word[idx - n_words] for word in words],
            [word[idx - 1] for word in words],
        )
    return xor_vectors(*vectors)
