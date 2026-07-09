# Quantum Random Passwords

This folder contains the runnable code for the tutorial
`Quantum Randomness for Strong Passwords and Keys`.

## Requirements

- Python 3.10 or newer
- No third-party Python packages

## Run the demo

```bash
python assets/quantum_programs/qrng_passwords/qrng_passwords.py
```

Optional arguments:

```bash
python assets/quantum_programs/qrng_passwords/qrng_passwords.py --password-length 20 --bits 2048
```

The program simulates ideal measurements of a qubit prepared with a Hadamard
gate, then uses those bits to build an unbiased password and a toy one-time-pad
style encryption example.
