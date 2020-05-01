"""Main module with CLI."""
import argparse
import pathlib
import sys

from lib import actions


def main(*args):

    """Main function to parse arguments and choose action."""

    parser = argparse.ArgumentParser(
        prog=pathlib.Path(__file__).parent.name
    )
    subparsers = parser.add_subparsers(
        dest='action', required=True,
        help='Decrypt/encrypt file or generate key.', metavar='ACTION'
    )
    decrypt_parser = subparsers.add_parser('decrypt')
    decrypt_parser.add_argument(
        'file_path', help='file to decrypt', metavar='FILE'
    )
    decrypt_parser.add_argument(
        'key_file', help='key to decrypt with', metavar='KEY'
    )
    encrypt_parser = subparsers.add_parser('encrypt')
    encrypt_parser.add_argument(
        'file_path', help='file to encrypt', metavar='FILE'
    )
    encrypt_parser.add_argument(
        'key_file', help='key to encrypt with', metavar='KEY'
    )
    generate_parser = subparsers.add_parser('generate')
    generate_parser.add_argument(
        '-s', '--key-size', default=128, type=int, choices=(128, 192, 256),
        help='size of key', metavar='SIZE'
    )
    generate_parser.add_argument(
        'key_file', help='file to store', metavar='FILE'
    )
    namespace = parser.parse_args(*args)
    if namespace.action == 'generate':
        actions.generate(namespace.key_file, namespace.key_size)
    else:
        action = getattr(actions, namespace.action)
        action(namespace.file_path, namespace.key_file)


if __name__ == '__main__':
    main(sys.argv[1:])
