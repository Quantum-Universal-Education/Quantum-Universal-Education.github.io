"""Quantum random bits for passwords and toy encryption keys.

This educational script simulates the measurement of a qubit prepared in the
Hadamard state:

    |+> = (|0> + |1>) / sqrt(2)

Measuring |+> in the computational basis gives 0 or 1 with equal probability.
The script uses Python's cryptographic random source to sample that ideal
measurement outcome, then shows how those bits can be turned into passwords
without modulo bias.

Run:
    python qrng_passwords.py
"""

from __future__ import annotations

import argparse
import math
import secrets
import string
from collections import Counter


DEFAULT_ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"


def measure_hadamard_qubit() -> int:
    """Return one ideal measurement outcome from H|0>."""

    amplitudes = (1 / math.sqrt(2), 1 / math.sqrt(2))
    probabilities = tuple(round(abs(amplitude) ** 2, 10) for amplitude in amplitudes)

    if probabilities != (0.5, 0.5):
        raise RuntimeError("The ideal Hadamard state should measure 0 and 1 equally.")

    return secrets.randbelow(2)


def quantum_bits(length: int) -> list[int]:
    """Generate `length` ideal quantum measurement bits."""

    if length < 0:
        raise ValueError("length must be non-negative")
    return [measure_hadamard_qubit() for _ in range(length)]


def bits_to_int(bits: list[int]) -> int:
    """Interpret a list of bits as one binary integer."""

    value = 0
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("bits must contain only 0 and 1")
        value = (value << 1) | bit
    return value


def sample_alphabet_index(alphabet_size: int) -> int:
    """Sample an unbiased index in range(alphabet_size).

    The rejection step is important. If the alphabet has 74 characters, using
    random_value % 74 would make some characters slightly more likely than
    others because powers of two are not usually divisible by 74.
    """

    if alphabet_size < 2:
        raise ValueError("alphabet must contain at least two characters")

    bits_needed = math.ceil(math.log2(alphabet_size))
    while True:
        candidate = bits_to_int(quantum_bits(bits_needed))
        if candidate < alphabet_size:
            return candidate


def quantum_password(length: int = 16, alphabet: str = DEFAULT_ALPHABET) -> str:
    """Build a password from unbiased quantum-bit samples."""

    if length <= 0:
        raise ValueError("length must be positive")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet must not contain duplicate characters")

    return "".join(alphabet[sample_alphabet_index(len(alphabet))] for _ in range(length))


def monobit_report(bits: list[int]) -> str:
    """Return a short balance check for a generated bit string."""

    counts = Counter(bits)
    zeros = counts[0]
    ones = counts[1]
    total = zeros + ones
    if total == 0:
        return "No bits generated."

    difference = ones - zeros
    z_score = difference / math.sqrt(total)
    return (
        f"Generated {total} bits: zeros={zeros}, ones={ones}, "
        f"z-score={z_score:.2f}"
    )


def xor_bytes(message: bytes, key: bytes) -> bytes:
    """Apply a one-time-pad style XOR to a message."""

    if len(key) < len(message):
        raise ValueError("key must be at least as long as the message")
    return bytes(message_byte ^ key_byte for message_byte, key_byte in zip(message, key))


def quantum_key_bytes(length: int) -> bytes:
    """Generate `length` bytes from ideal quantum measurement bits."""

    if length < 0:
        raise ValueError("length must be non-negative")

    output = bytearray()
    for _ in range(length):
        output.append(bits_to_int(quantum_bits(8)))
    return bytes(output)


def demo(password_length: int, bit_count: int) -> None:
    """Print the tutorial demo."""

    bits = quantum_bits(bit_count)
    print(monobit_report(bits))
    print(f"First 32 bits: {''.join(str(bit) for bit in bits[:32])}")
    print(f"Example password: {quantum_password(password_length)}")

    message = b"meet at 5"
    key = quantum_key_bytes(len(message))
    ciphertext = xor_bytes(message, key)
    recovered = xor_bytes(ciphertext, key)

    print(f"Toy message: {message!r}")
    print(f"Quantum-style key bytes: {key.hex()}")
    print(f"Ciphertext bytes: {ciphertext.hex()}")
    print(f"Recovered message: {recovered!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--password-length", type=int, default=16)
    parser.add_argument("--bits", type=int, default=1024)
    args = parser.parse_args()
    demo(password_length=args.password_length, bit_count=args.bits)


if __name__ == "__main__":
    main()
