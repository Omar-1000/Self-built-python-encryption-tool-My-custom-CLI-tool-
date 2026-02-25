from __future__ import annotations
import hashlib
import random
from typing import List


def _derive_seed_and_shift(key: str, shift_override: int | None = None) -> tuple[int, int]:
    if not key:
        raise ValueError("Key must be non-empty.")
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    seed = int.from_bytes(digest[:8], "big")
    shift = (digest[8] % 26) if shift_override is None else shift_override
    if not (0 <= shift <= 25):
        raise ValueError("Shift must be 0..25.")
    return seed, shift


def caesar_cipher_standard(text: str, shift: int) -> str:
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)


def _zigzag_split(plaintext: str, depth: int) -> List[str]:
    rails = [""] * depth
    row = 0
    step = 1
    for ch in plaintext:
        rails[row] += ch
        if row == 0:
            step = 1
        elif row == depth - 1:
            step = -1
        row += step
    return rails


def _rail_lengths(n: int, depth: int) -> List[int]:
    return [len(r) for r in _zigzag_split("X" * n, depth)]


def _make_perm(depth: int, seed: int) -> List[int]:
    rng = random.Random(seed)
    perm = list(range(depth))
    rng.shuffle(perm)
    return perm


def encrypt(plaintext: str, *, depth: int, key: str, direction: str = "left", shift: int | None = None) -> str:
    if depth < 2:
        raise ValueError("depth must be >= 2")
    if direction not in ("left", "right"):
        raise ValueError("direction must be 'left' or 'right'")

    seed, real_shift = _derive_seed_and_shift(key, shift)

    rails = _zigzag_split(plaintext, depth)
    rails = [caesar_cipher_standard(r, real_shift) for r in rails]

    if direction == "right":
        rails = [r[::-1] for r in rails]

    perm = _make_perm(depth, seed)
    shuffled = [rails[i] for i in perm]

    header = ".".join(map(str, perm))
    return f"RF{depth}|{direction}|{real_shift}|{header}::{''.join(shuffled)}"


def decrypt(ciphertext: str, *, key: str) -> str:
    if "::" not in ciphertext:
        raise ValueError("Invalid ciphertext format.")
    meta, body = ciphertext.split("::", 1)

    if not meta.startswith("RF"):
        raise ValueError("Invalid header.")

    try:
        rf_depth, direction, shift_str, perm_str = meta.split("|", 3)
        depth = int(rf_depth[2:])
        shift = int(shift_str)
        perm = list(map(int, perm_str.split(".")))
    except Exception as e:
        raise ValueError("Invalid ciphertext header format.") from e

    if depth < 2 or len(perm) != depth:
        raise ValueError("Invalid depth/permutation in header.")

    _seed, real_shift = _derive_seed_and_shift(key, shift)

    n = len(body)
    lengths = _rail_lengths(n, depth)

    idx = 0
    shuffled_rails = [""] * depth
    for pos, rail_id in enumerate(perm):
        ln = lengths[rail_id]
        shuffled_rails[pos] = body[idx : idx + ln]
        idx += ln

    rails = [""] * depth
    for pos, rail_id in enumerate(perm):
        rails[rail_id] = shuffled_rails[pos]

    if direction == "right":
        rails = [r[::-1] for r in rails]

    rails = [caesar_cipher_standard(r, (-real_shift) % 26) for r in rails]

    rail_lists = [list(r) for r in rails]
    row = 0
    step = 1
    out = []
    for _ in range(n):
        out.append(rail_lists[row].pop(0))
        if row == 0:
            step = 1
        elif row == depth - 1:
            step = -1
        row += step

    return "".join(out)