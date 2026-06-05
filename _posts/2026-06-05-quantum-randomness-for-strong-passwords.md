---
title: "Quantum Randomness for Strong Passwords and Keys"
categories:
  - Blog
tags:
  - tutorial
  - quantum computing
  - quantum cryptography
  - quantum random number generation
  - Python
author:
  - rijojose999
---

<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

Passwords, encryption keys, recovery codes, and session tokens all depend on one
quiet ingredient: randomness. If the random numbers are predictable, the rest of
the security system can look strong while still being easy to attack.

In this tutorial we will build a beginner-friendly quantum random number
generator (QRNG) simulation and use it for two daily-life security tasks:

- generating a password from quantum measurement bits;
- building a toy one-time-pad style key for a short message.

The code is intentionally small and runs with only Python's standard library.
That makes it easier to focus on the quantum idea before using a real quantum
device or a full quantum software development kit.

## Learning Goals

By the end of the tutorial, you should be able to:

1. Explain why randomness matters for passwords and encryption keys.
2. Describe how a Hadamard gate turns \(|0\rangle\) into a 50/50 quantum
   measurement.
3. Generate ideal quantum measurement bits in Python.
4. Convert random bits into password characters without modulo bias.
5. Explain the difference between an educational simulator and a real QRNG.

## Demo Video

The short walkthrough below summarizes the full project.

<video controls width="100%" poster="/assets/images/qrng_passwords/qrng_password_demo_cover.png">
  <source src="/assets/images/qrng_passwords/qrng_password_demo.mp4" type="video/mp4">
  Your browser does not support the video tag. You can download the video from
  /assets/images/qrng_passwords/qrng_password_demo.mp4.
</video>

The code used in this post is also available as:

- [Python script](/assets/quantum_programs/qrng_passwords/qrng_passwords.py)
- [Jupyter notebook](/assets/quantum_programs/qrng_passwords/qrng_passwords.ipynb)
- [README with run instructions](/assets/quantum_programs/qrng_passwords/README.md)

## Requirements

To run the example:

- Python 3.10 or newer
- No third-party Python packages

From the repository root:

```bash
python assets/quantum_programs/qrng_passwords/qrng_passwords.py
```

You can also change the password length and the number of sample bits:

```bash
python assets/quantum_programs/qrng_passwords/qrng_passwords.py --password-length 20 --bits 2048
```

## Why Randomness Is a Security Tool

A password generator should not "feel random." It should actually make each
allowed password hard to guess. If a generator uses a weak pattern, an attacker
can search the likely outputs first.

For example, these passwords may look different:

```text
Summer2026!
Summer2027!
Summer2028!
```

but they follow a human pattern. A good generator should avoid that kind of
structure. It should produce values that are unpredictable even when an attacker
knows the program.

Randomness also matters for encryption. A one-time pad, for example, can hide a
message only when the key is:

- truly random;
- at least as long as the message;
- never reused.

That is why random number generation is not a side detail in cryptography. It
is one of the foundations.

## The Quantum Idea

A classical coin can be biased by its shape, weight, or the way it is thrown. A
quantum measurement can be random for a deeper reason: before measurement, the
state can be in a superposition.

Start with one qubit in the state:

$$
|0\rangle
$$

Apply a Hadamard gate:

$$
H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle
$$

This state has two amplitudes:

$$
\frac{1}{\sqrt{2}} \quad \text{for } |0\rangle
$$

and

$$
\frac{1}{\sqrt{2}} \quad \text{for } |1\rangle
$$

The probability of a measurement outcome is the squared magnitude of its
amplitude:

$$
P(0) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}
$$

$$
P(1) = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}
$$

So one measured qubit gives one fair random bit.

## Simulator Versus Real QRNG

The program below is a teaching simulator. It samples the ideal 50/50 result
with Python's `secrets` module so that the tutorial can run on any laptop.

A real QRNG is different. It measures a physical quantum process, checks the
device behavior, estimates entropy, and usually applies extraction or
conditioning before the bits are used in security systems. Standards such as
NIST SP 800-90B discuss how entropy sources should be analyzed for random bit
generation.

This distinction matters:

- use this tutorial to understand the workflow;
- do not claim that the simulator produces hardware quantum randomness;
- for production security, use a vetted operating-system or hardware random
  source.

## Step 1: Measure One Ideal Qubit

Here is the core of the simulator:

```python
import math
import secrets


def measure_hadamard_qubit() -> int:
    """Return one ideal measurement outcome from H|0>."""

    amplitudes = (1 / math.sqrt(2), 1 / math.sqrt(2))
    probabilities = tuple(round(abs(amplitude) ** 2, 10) for amplitude in amplitudes)

    if probabilities != (0.5, 0.5):
        raise RuntimeError("The ideal Hadamard state should measure 0 and 1 equally.")

    return secrets.randbelow(2)
```

The first part computes the ideal quantum probabilities. The final line samples
one bit. In a hardware QRNG, this final line would be replaced by a measurement
from a real physical device.

## Step 2: Generate Many Bits

One bit is not enough for a password or key, so we repeat the measurement:

```python
def quantum_bits(length: int) -> list[int]:
    """Generate `length` ideal quantum measurement bits."""

    if length < 0:
        raise ValueError("length must be non-negative")
    return [measure_hadamard_qubit() for _ in range(length)]
```

If we generate 1024 bits, we should expect the number of zeros and ones to be
close, but not exactly equal. Randomness does not mean perfect alternation. It
means the output is unpredictable.

The script includes a small balance check:

```python
from collections import Counter


def monobit_report(bits: list[int]) -> str:
    """Return a short balance check for a generated bit string."""

    counts = Counter(bits)
    zeros = counts[0]
    ones = counts[1]
    total = zeros + ones
    difference = ones - zeros
    z_score = difference / math.sqrt(total)
    return (
        f"Generated {total} bits: zeros={zeros}, ones={ones}, "
        f"z-score={z_score:.2f}"
    )
```

This is not a complete randomness test suite. It is a first sanity check for
students: the result should usually stay reasonably close to balanced when the
sample is large.

## Step 3: Avoid Modulo Bias

Suppose a password alphabet has 74 possible characters. We might try to turn
random bits into an integer and then do:

```python
index = random_value % 74
```

That looks simple, but it creates a subtle bias. If we draw 7 bits, we get 128
possible values from 0 to 127. Since 128 is not evenly divisible by 74, some
password characters will appear more often than others.

The fix is rejection sampling:

1. Compute how many bits are needed to cover the alphabet.
2. Draw that many bits.
3. If the number fits inside the alphabet range, use it.
4. If it is too large, discard it and try again.

```python
def bits_to_int(bits: list[int]) -> int:
    """Interpret a list of bits as one binary integer."""

    value = 0
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("bits must contain only 0 and 1")
        value = (value << 1) | bit
    return value


def sample_alphabet_index(alphabet_size: int) -> int:
    """Sample an unbiased index in range(alphabet_size)."""

    if alphabet_size < 2:
        raise ValueError("alphabet must contain at least two characters")

    bits_needed = math.ceil(math.log2(alphabet_size))
    while True:
        candidate = bits_to_int(quantum_bits(bits_needed))
        if candidate < alphabet_size:
            return candidate
```

This keeps every character equally likely.

## Step 4: Generate a Password

Now we choose an alphabet and sample one unbiased index per password character:

```python
import string


DEFAULT_ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"


def quantum_password(length: int = 16, alphabet: str = DEFAULT_ALPHABET) -> str:
    """Build a password from unbiased quantum-bit samples."""

    if length <= 0:
        raise ValueError("length must be positive")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet must not contain duplicate characters")

    return "".join(alphabet[sample_alphabet_index(len(alphabet))] for _ in range(length))
```

Example output:

```text
Generated 1024 bits: zeros=513, ones=511, z-score=-0.06
First 32 bits: 10001011011100101001100110101100
Example password: V4gW*7Eb%Em_#9NE
```

Your result will be different when you run the script.

## Step 5: Use Random Bytes as a Toy Key

A one-time pad combines a message and a key with XOR. The same operation
encrypts and decrypts:

```python
def xor_bytes(message: bytes, key: bytes) -> bytes:
    """Apply a one-time-pad style XOR to a message."""

    if len(key) < len(message):
        raise ValueError("key must be at least as long as the message")
    return bytes(message_byte ^ key_byte for message_byte, key_byte in zip(message, key))
```

To build key bytes, collect eight measurement bits per byte:

```python
def quantum_key_bytes(length: int) -> bytes:
    """Generate `length` bytes from ideal quantum measurement bits."""

    if length < 0:
        raise ValueError("length must be non-negative")

    output = bytearray()
    for _ in range(length):
        output.append(bits_to_int(quantum_bits(8)))
    return bytes(output)
```

Then try it on a short message:

```python
message = b"meet at 5"
key = quantum_key_bytes(len(message))
ciphertext = xor_bytes(message, key)
recovered = xor_bytes(ciphertext, key)

print(f"Toy message: {message!r}")
print(f"Quantum-style key bytes: {key.hex()}")
print(f"Ciphertext bytes: {ciphertext.hex()}")
print(f"Recovered message: {recovered!r}")
```

This demonstrates the shape of the idea, but remember the real security rules:
the key must come from a trusted random source, must be at least as long as the
message, and must never be reused.

## Full Demo Function

The script ties the pieces together like this:

```python
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
```

## What To Try Next

Here are a few extensions:

- Increase the sample size and watch how the zero/one balance changes.
- Try different password alphabets and confirm the rejection sampler still
  works.
- Add a histogram for character frequencies.
- Replace the ideal simulator with measurements from a real quantum backend or
  a public QRNG service.
- Study how randomness extraction turns noisy physical measurements into
  cleaner random bits.

## How This Tutorial Started

This tutorial started from a simple security question: where does a strong
password actually get its unpredictability? That question is a friendly entry
point into quantum computing because a single Hadamard gate already shows one
of the field's most important ideas: measurement can turn a carefully prepared
quantum state into a random classical bit.

For students, QRNGs are a useful bridge. They connect abstract notation like
\(|+\rangle\) and \(P(0)=P(1)=1/2\) to something people use every day:
passwords, keys, and secure communication.

## AI Assistance Disclosure

AI assistance was used to help outline the tutorial structure, draft wording,
and review the Python examples. The code paths included in the tutorial were
run locally, and the quantum concepts were checked against the references below.

## References

1. Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum
   Information*, Cambridge University Press.
2. NIST SP 800-90B, [Recommendation for the Entropy Sources Used for Random Bit
   Generation](https://csrc.nist.gov/pubs/sp/800/90/b/final).
3. ANU Quantum Optics, [Quantum random number generator](https://www.anuquantumoptics.org/anu/research-topics/qrng).
4. ID Quantique, [Quantum Random Number Generation overview](https://www.idquantique.com/random-number-generation/overview/).
