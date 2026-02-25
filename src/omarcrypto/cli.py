import argparse
from .core import encrypt, decrypt


def main():
    parser = argparse.ArgumentParser(
        prog="omarcrypto",
        description="OmarCrypto: custom Python encryption tool (educational)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    enc = sub.add_parser("enc", help="Encrypt plaintext")
    enc.add_argument("-t", "--text", required=True, help="Plaintext to encrypt")
    enc.add_argument("-d", "--depth", type=int, required=True, help="Rail depth (>=2)")
    enc.add_argument("-k", "--key", required=True, help="Key (drives deterministic shuffle + shift)")
    enc.add_argument("--direction", choices=["left", "right"], default="left", help="Rail direction")
    enc.add_argument("--shift", type=int, default=None, help="Optional Caesar shift override (0..25)")

    dec = sub.add_parser("dec", help="Decrypt ciphertext")
    dec.add_argument("-c", "--cipher", required=True, help="Ciphertext to decrypt")
    dec.add_argument("-k", "--key", required=True, help="Key used for encryption")

    args = parser.parse_args()

    if args.cmd == "enc":
        print(encrypt(args.text, depth=args.depth, key=args.key, direction=args.direction, shift=args.shift))
    else:
        print(decrypt(args.cipher, key=args.key))


if __name__ == "__main__":
    main()