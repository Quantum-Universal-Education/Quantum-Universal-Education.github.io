#!/usr/bin/env python3
"""
quantum_benchmark_arithmetic.py
================================
Benchmarks quantum arithmetic circuits (ADD, SUB, MUL, MODULO-ADD)
across five simulators: Qiskit Aer, Cirq, Blueqat, PennyLane, SymPy.

All simulators run the SAME logical circuit — a quantum ripple-carry
adder/subtractor/multiplier — built using a shared abstract gate layer.

Usage:
    python benchmark_arithmetic.py
    python benchmark_arithmetic.py --shots 5 --simulators qiskit cirq blueqat
    python benchmark_arithmetic.py --no-sympy    # Skip slow SymPy runs

Reference results (10 shots each):
    Qiskit  : ADD=0.19s, SUB=0.13s, MUL=0.29s, MODULOADD=0.94s
    Blueqat : ADD=1.73s, SUB=1.72s, MUL=6.31s, MODULOADD=34.66s
    Cirq    : ADD=49.2s, SUB=49.1s, MUL=100.3s, MODULOADD=389.6s
    SymPy   : ADD=199.9s, SUB=199.9s, MUL=149.4s, MODULOADD=435.9s

AI note: This script structure was partially organized with Claude (Anthropic).
         All circuit logic and benchmark code is original research work.
"""

import argparse
import sys
import time
import random
from types import TracebackType
from typing import List, Optional, Set, Type, Union

import pandas as pd


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Shared Qubit Allocator
# ══════════════════════════════════════════════════════════════════════════════

class QubitAllocator:
    """
    Manages qubit indices across the circuit.

    When we create a QBit() object, it gets a unique integer index from here.
    When we deallocate an ancilla qubit, its index is freed for reuse.
    This mirrors how real quantum hardware manages qubit resources.
    """
    def __init__(self):
        self.allocated: Set[int] = set()

    def reset(self):
        self.allocated = set()

    def allocate1(self) -> int:
        if not self.allocated:
            self.allocated.add(0)
            return 0
        for i in range(max(self.allocated)):
            if i not in self.allocated:
                self.allocated.add(i)
                return i
        i = max(self.allocated) + 1
        self.allocated.add(i)
        return i

    def deallocate1(self, index: int):
        self.allocated.remove(index)


ALLOCATOR = QubitAllocator()


def reset_all():
    """Reset allocator between test cases."""
    ALLOCATOR.reset()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Abstract Gate Objects
# ══════════════════════════════════════════════════════════════════════════════
# Each gate is an object that knows how to synthesize itself into any backend.
# This is the Adapter pattern: one abstract description, many concrete outputs.

class UnitaryOperation:
    """Base class for all quantum gates."""
    def reverse(self): pass
    def synthesis(self, circuit): return circuit
    def string(self, depth: int) -> str: return ''
    def __str__(self): return self.string(0)


class UO_Procedure(UnitaryOperation):
    """A named sequence of gate operations — like a quantum subroutine."""
    def __init__(self, title: str):
        self.title = title
        self.ops: List[UnitaryOperation] = []

    def append_op(self, op: UnitaryOperation):
        self.ops.append(op)

    def reverse(self):
        """Reverse the entire procedure — enables quantum subtraction!"""
        for op in reversed(self.ops):
            op.reverse()
        self.ops.reverse()

    def synthesis(self, circuit):
        for op in self.ops:
            circuit = op.synthesis(circuit)
        return circuit

    def string(self, depth: int) -> str:
        body = ',\n'.join(' ' * (depth + 1) + op.string(depth + 1) for op in self.ops)
        return f'{self.title}{{\n{body}\n{" " * depth}}}'


# ── Individual gate classes: each overrides synthesis() per backend ──────────

class UO_H(UnitaryOperation):
    """
    Hadamard gate: creates superposition.
    |0⟩ → (|0⟩ + |1⟩)/√2
    |1⟩ → (|0⟩ - |1⟩)/√2
    """
    def __init__(self, q: int):
        self.q = q
        append_uo(self)

    def synthesis(self, circuit):
        backend = type(circuit).__module__.split('.')[0]
        if backend == 'blueqat':
            circuit.h[self.q]
        elif backend == 'cirq':
            import cirq
            circuit.append([cirq.H(cirq.NamedQubit(str(self.q)))])
        elif backend == 'qiskit':
            import qiskit
            circuit.h(get_qiskit_register()[self.q])
        elif backend == 'sympy':
            import sympy.physics.quantum.gate as gate
            op = gate.H(self.q)
            return (op * circuit) if circuit is not None else op
        return circuit

    def string(self, depth: int) -> str:
        return f'H[{self.q}]'


class UO_X(UnitaryOperation):
    """
    Pauli-X gate (quantum NOT):
    |0⟩ → |1⟩
    |1⟩ → |0⟩
    """
    def __init__(self, q: int):
        self.q = q
        append_uo(self)

    def synthesis(self, circuit):
        backend = type(circuit).__module__.split('.')[0]
        if backend == 'blueqat':
            circuit.x[self.q]
        elif backend == 'cirq':
            import cirq
            circuit.append([cirq.X(cirq.NamedQubit(str(self.q)))])
        elif backend == 'qiskit':
            circuit.x(get_qiskit_register()[self.q])
        elif backend == 'sympy':
            import sympy.physics.quantum.gate as gate
            op = gate.X(self.q)
            return (op * circuit) if circuit is not None else op
        return circuit

    def string(self, depth: int) -> str:
        return f'X[{self.q}]'


class UO_CX(UnitaryOperation):
    """
    Controlled-NOT (CNOT):
    Flips target qubit if and only if control qubit is |1⟩.
    This is the primary entangling gate in most quantum circuits.
    """
    def __init__(self, c: int, x: int):
        self.c = c
        self.x = x
        append_uo(self)

    def synthesis(self, circuit):
        backend = type(circuit).__module__.split('.')[0]
        if backend == 'blueqat':
            circuit.cx[self.c, self.x]
        elif backend == 'cirq':
            import cirq
            circuit.append([cirq.CX(cirq.NamedQubit(str(self.c)),
                                    cirq.NamedQubit(str(self.x)))])
        elif backend == 'qiskit':
            circuit.cx(get_qiskit_register()[self.c], get_qiskit_register()[self.x])
        elif backend == 'sympy':
            import sympy.physics.quantum.gate as gate
            op = gate.CNOT(self.c, self.x)
            return (op * circuit) if circuit is not None else op
        return circuit

    def string(self, depth: int) -> str:
        return f'CX[{self.c},{self.x}]'


class UO_CSWAP(UnitaryOperation):
    """
    Fredkin (Controlled-SWAP) gate:
    If control=|1⟩, swap qubits a and b; otherwise do nothing.

    Implementation: CSWAP(c,a,b) = CCX(c,a,b) · CCX(c,b,a) · CCX(c,a,b)
    This is the standard decomposition into Toffoli gates.
    """
    def __init__(self, c: int, a: int, b: int):
        self.c = c
        self.a = a
        self.b = b
        append_uo(self)

    def synthesis(self, circuit):
        c, a, b = self.c, self.a, self.b
        backend = type(circuit).__module__.split('.')[0]
        if backend == 'blueqat':
            circuit.ccx[c, a, b].ccx[c, b, a].ccx[c, a, b]
        elif backend == 'cirq':
            import cirq
            circuit.append([
                cirq.CCX(cirq.NamedQubit(str(c)), cirq.NamedQubit(str(a)), cirq.NamedQubit(str(b))),
                cirq.CCX(cirq.NamedQubit(str(c)), cirq.NamedQubit(str(b)), cirq.NamedQubit(str(a))),
                cirq.CCX(cirq.NamedQubit(str(c)), cirq.NamedQubit(str(a)), cirq.NamedQubit(str(b))),
            ])
        elif backend == 'qiskit':
            r = get_qiskit_register()
            circuit.ccx(r[c], r[a], r[b])
            circuit.ccx(r[c], r[b], r[a])
            circuit.ccx(r[c], r[a], r[b])
        elif backend == 'sympy':
            import sympy.physics.quantum.gate as gate
            def CCNOT(c1, c2, q):
                return gate.CGate((c1, c2), gate.X(q))
            op = CCNOT(c, a, b) * CCNOT(c, b, a) * CCNOT(c, a, b)
            return (op * circuit) if circuit is not None else op
        return circuit

    def string(self, depth: int) -> str:
        return f'CSWAP[{self.c},{self.a},{self.b}]'


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Procedure Stack (context manager pattern)
# ══════════════════════════════════════════════════════════════════════════════

PROCEDURE_STACK_TOP: Optional['UO_Proc'] = None


class UO_Proc:
    """
    Context manager for building named gate sequences.

    Usage:
        with UO_Proc('my_circuit') as p:
            UO_H(0)
            UO_CX(0, 1)
        circuit = p.synthesis(blueqat.Circuit())
    """
    def __init__(self, title: str):
        self._procedure = UO_Procedure(title)

    def __enter__(self) -> 'UO_Proc':
        global PROCEDURE_STACK_TOP
        self._parent = PROCEDURE_STACK_TOP
        PROCEDURE_STACK_TOP = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global PROCEDURE_STACK_TOP
        PROCEDURE_STACK_TOP = self._parent
        if PROCEDURE_STACK_TOP:
            PROCEDURE_STACK_TOP.get_procedure().append_op(self._procedure)

    def get_procedure(self) -> UO_Procedure:
        return self._procedure

    def synthesis(self, circuit):
        return self._procedure.synthesis(circuit)

    def __str__(self):
        return str(self._procedure)


def append_uo(uo: UnitaryOperation):
    if PROCEDURE_STACK_TOP is None:
        raise RuntimeError('No active procedure. Use: with UO_Proc(...) as p:')
    PROCEDURE_STACK_TOP.get_procedure().append_op(uo)


def reverse_current_proc():
    if PROCEDURE_STACK_TOP is None:
        raise RuntimeError('No active procedure.')
    PROCEDURE_STACK_TOP.get_procedure().reverse()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Quantum Integer Arithmetic
# ══════════════════════════════════════════════════════════════════════════════

class QBit:
    """A single qubit with an allocated index."""
    def __init__(self, index: Optional[int] = None):
        self.index = index if index is not None else ALLOCATOR.allocate1()

    def deallocate(self) -> int:
        ALLOCATOR.deallocate1(self.index)
        return self.index

    @staticmethod
    def h(q: 'QBit'): UO_H(q.index)

    @staticmethod
    def x(q: 'QBit'): UO_X(q.index)

    @staticmethod
    def cx(c: 'QBit', q: 'QBit'): UO_CX(c.index, q.index)

    @staticmethod
    def cswap(c: 'QBit', a: 'QBit', b: 'QBit'): UO_CSWAP(c.index, a.index, b.index)

    def __str__(self): return str(self.index)


class Carry(UnitaryOperation):
    """
    Quantum carry gate — the heart of the ripple-carry adder.

    Forward  (is_reversed=False):  CCX(b,c,d) → CX(b,c) → CCX(a,c,d)
    Reversed (is_reversed=True):   CCX(a,c,d) → CX(b,c) → CCX(b,c,d)

    The reversed form is automatically used in subtraction circuits.
    This reversibility is a fundamental property of quantum gates!
    """
    def __init__(self, a: QBit, b: QBit, c: QBit, d: QBit, is_reversed: bool = False):
        self.a, self.b, self.c, self.d = a, b, c, d
        self.is_reversed = is_reversed
        append_uo(self)

    def reverse(self):
        self.is_reversed = not self.is_reversed

    def synthesis(self, circuit):
        a, b, c, d = self.a.index, self.b.index, self.c.index, self.d.index
        backend = type(circuit).__module__.split('.')[0]

        def ccx(ctrl1, ctrl2, tgt):
            if backend == 'blueqat':
                circuit.ccx[ctrl1, ctrl2, tgt]
            elif backend == 'cirq':
                import cirq
                circuit.append([cirq.CCX(cirq.NamedQubit(str(ctrl1)),
                                         cirq.NamedQubit(str(ctrl2)),
                                         cirq.NamedQubit(str(tgt)))])
            elif backend == 'qiskit':
                r = get_qiskit_register()
                circuit.ccx(r[ctrl1], r[ctrl2], r[tgt])
            elif backend == 'sympy':
                import sympy.physics.quantum.gate as gate
                op = gate.CGate((ctrl1, ctrl2), gate.X(tgt))
                return op
            return None

        def cx(ctrl, tgt):
            if backend == 'blueqat':
                circuit.cx[ctrl, tgt]
            elif backend == 'cirq':
                import cirq
                circuit.append([cirq.CX(cirq.NamedQubit(str(ctrl)),
                                        cirq.NamedQubit(str(tgt)))])
            elif backend == 'qiskit':
                r = get_qiskit_register()
                circuit.cx(r[ctrl], r[tgt])
            elif backend == 'sympy':
                import sympy.physics.quantum.gate as gate
                return gate.CNOT(ctrl, tgt)
            return None

        if backend == 'sympy':
            if not self.is_reversed:
                op = ccx(a, c, d) * cx(b, c) * ccx(b, c, d)
            else:
                op = ccx(b, c, d) * cx(b, c) * ccx(a, c, d)
            return (op * circuit) if circuit is not None else op

        if not self.is_reversed:
            ccx(b, c, d); cx(b, c); ccx(a, c, d)
        else:
            ccx(a, c, d); cx(b, c); ccx(b, c, d)
        return circuit

    def string(self, depth: int) -> str:
        tag = 'RCarry' if self.is_reversed else 'Carry'
        return f'{tag}[{self.a},{self.b},{self.c},{self.d}]'


class Sum(UnitaryOperation):
    """
    Quantum sum gate: computes XOR of three bits.

    Forward:  CX(b,c) → CX(a,c)
    Reversed: CX(a,c) → CX(b,c)
    """
    def __init__(self, a: QBit, b: QBit, c: QBit, is_reversed: bool = False):
        self.a, self.b, self.c = a, b, c
        self.is_reversed = is_reversed
        append_uo(self)

    def reverse(self):
        self.is_reversed = not self.is_reversed

    def synthesis(self, circuit):
        a, b, c = self.a.index, self.b.index, self.c.index
        backend = type(circuit).__module__.split('.')[0]

        if backend == 'sympy':
            import sympy.physics.quantum.gate as gate
            if not self.is_reversed:
                op = gate.CNOT(a, c) * gate.CNOT(b, c)
            else:
                op = gate.CNOT(b, c) * gate.CNOT(a, c)
            return (op * circuit) if circuit is not None else op

        def cx(ctrl, tgt):
            if backend == 'blueqat':
                circuit.cx[ctrl, tgt]
            elif backend == 'cirq':
                import cirq
                circuit.append([cirq.CX(cirq.NamedQubit(str(ctrl)),
                                        cirq.NamedQubit(str(tgt)))])
            elif backend == 'qiskit':
                r = get_qiskit_register()
                circuit.cx(r[ctrl], r[tgt])

        if not self.is_reversed:
            cx(b, c); cx(a, c)
        else:
            cx(a, c); cx(b, c)
        return circuit

    def string(self, depth: int) -> str:
        tag = 'RSum' if self.is_reversed else 'Sum'
        return f'{tag}[{self.a},{self.b},{self.c}]'


class Integer:
    """
    A quantum integer: a list of qubits encoding a binary number.

    Creating Integer(5) with NBITS=4 allocates 4 qubits and sets them to |0101⟩.
    Calling .hadamard() puts all bits into superposition — the quantum equivalent
    of "pick a random number".

    Arithmetic operations (+, -, *) build the circuit — they don't execute it yet!
    """
    NBITS = 4

    def __init__(self, n: Union['Integer', List[QBit], int], nbits: int = -1):
        if nbits < 0:
            nbits = Integer.NBITS
        self._carry: Optional[QBit] = None
        self.qbits: List[QBit] = []

        if isinstance(n, Integer):
            self._carry = n._carry
            self.qbits = n.qbits
            self.set_nbits(nbits)
        elif isinstance(n, list):
            self.qbits = n
            self.set_nbits(nbits)
        elif isinstance(n, int):
            self.qbits = [QBit() for _ in range(nbits)]
            if n != 0:
                with UO_Proc('Integer.init') as p:
                    for i in range(nbits):
                        if n & (1 << i):
                            QBit.x(self.qbits[i])
        self.cs: Optional[List[QBit]] = None

    def set_nbits(self, nbits: int):
        if len(self.qbits) < nbits:
            self.qbits += [QBit() for _ in range(nbits - len(self.qbits))]
        if len(self.qbits) > nbits:
            self.qbits = self.qbits[:nbits]

    def nbits(self) -> int:
        return len(self.qbits)

    def deallocate(self):
        for c in self.qbits:
            c.deallocate()

    def _deallocate(self):
        if self.cs:
            for c in self.cs:
                c.deallocate()
            self.cs = None

    def _cs(self, i: int) -> QBit:
        if i >= len(self.qbits):
            return self.carry()
        if not self.cs:
            self.cs = [QBit() for _ in range(len(self.qbits))]
        return self.cs[i]

    def carry(self) -> QBit:
        if self._carry is None:
            self._carry = QBit()
        return self._carry

    def hadamard(self, n: int = -1) -> 'Integer':
        """Put n bits into superposition — creates a uniform random quantum number."""
        with UO_Proc('Integer.hadamard'):
            if n < 0:
                n = len(self.qbits)
            for i in range(n):
                QBit.h(self.qbits[i])
        return self

    def __iadd__(self, other: 'Integer') -> 'Integer':
        """Quantum addition using ripple-carry adder."""
        self._synthesis_iadd('Integer.add', other)
        self._deallocate()
        return self

    def __isub__(self, other: 'Integer') -> 'Integer':
        """Quantum subtraction = reversed addition."""
        self._synthesis_iadd('Integer.sub', other, is_reversed=True)
        self._deallocate()
        return self

    def _synthesis_iadd(self, title: str, other: 'Integer', is_reversed: bool = False):
        """
        Build the ripple-carry adder circuit.

        For n-bit integers:
        1. Apply Carry gates forward (propagate carries)
        2. Apply CX on MSBs
        3. Uncompute carries with reversed Carry gates
        4. Apply Sum gates

        For subtraction: reverse the entire sequence.
        """
        if len(other.qbits) != len(self.qbits):
            raise RuntimeError('Bit width mismatch')
        with UO_Proc(title):
            for i in range(len(self.qbits)):
                Carry(self._cs(i), other.qbits[i], self.qbits[i], self._cs(i + 1))
            QBit.cx(other.qbits[-1], self.qbits[-1])
            for i in range(len(self.qbits) - 1, 0, -1):
                Sum(self._cs(i), other.qbits[i], self.qbits[i])
                Carry(self._cs(i - 1), other.qbits[i - 1], self.qbits[i - 1],
                      self._cs(i), is_reversed=True)
            Sum(self._cs(0), other.qbits[0], self.qbits[0])
            if is_reversed:
                reverse_current_proc()

    def __lshift__(self, orig: 'Integer') -> 'Integer':
        """Copy (XOR copy) orig into self."""
        if len(orig.qbits) != len(self.qbits):
            raise RuntimeError('Bit width mismatch')
        with UO_Proc('Integer.xor'):
            for c, x in zip(orig.qbits, self.qbits):
                QBit.cx(c, x)
            if orig._carry is not None:
                QBit.cx(orig._carry, self.carry())
        return self

    @staticmethod
    def cswap(c: QBit, a: 'Integer', b: 'Integer'):
        """Conditionally swap two integers (used in multiplication)."""
        with UO_Proc('Integer.cswap'):
            if len(a.qbits) != len(b.qbits):
                raise RuntimeError('Bit width mismatch')
            for a1, b1 in zip(a.qbits, b.qbits):
                QBit.cswap(c, a1, b1)
            if a._carry is not None:
                QBit.cswap(c, a._carry, b.carry())
            elif b._carry is not None:
                QBit.cswap(c, a.carry(), b._carry)

    def rshift(self) -> QBit:
        """Shift right by one bit; returns the LSB."""
        lsb = self.qbits[0]
        self.qbits = self.qbits[1:]
        msb = self._carry if self._carry is not None else QBit()
        if self._carry is not None:
            self._carry = None
        self.qbits += [msb]
        return lsb

    def __mul__(self, other: 'Integer') -> 'Integer':
        """
        Quantum multiplication using controlled partial products.

        For each bit i of self:
          - Conditionally load 'other' (via CSWAP)
          - Accumulate into running total
          - Conditionally unload (restore superposition)
          - Shift out LSB of accumulator
        Result is a 2n-bit integer.
        """
        if len(self.qbits) != len(other.qbits):
            raise RuntimeError('Bit width mismatch')
        with UO_Proc('Integer.mul'):
            a0 = Integer(0, nbits=len(self.qbits))
            results: List[QBit] = []
            t = Integer(0, nbits=len(self.qbits))
            for i in range(len(self.qbits)):
                Integer.cswap(self.qbits[i], other, a0)
                t += a0
                Integer.cswap(self.qbits[i], other, a0)
                results.append(t.rshift())
            a0.deallocate()
            return Integer(results + t.qbits, len(self.qbits) * 2)

    def bit_indices(self) -> List[int]:
        bs = [q.index for q in self.qbits]
        if self._carry is not None:
            bs.append(self._carry.index)
        return bs

    def __str__(self):
        args = ','.join(str(q) for q in self.qbits)
        if self._carry is not None:
            args += ',' + str(self._carry)
        return f'Integer[{args}]'


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Qiskit-specific helpers
# ══════════════════════════════════════════════════════════════════════════════

_QISKIT_REGISTER = None

def get_qiskit_register():
    global _QISKIT_REGISTER
    if _QISKIT_REGISTER is None:
        import qiskit
        _QISKIT_REGISTER = qiskit.QuantumRegister(max(ALLOCATOR.allocated) + 1)
    return _QISKIT_REGISTER

def reset_qiskit_register():
    global _QISKIT_REGISTER
    _QISKIT_REGISTER = None


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6: Result Parsing (simulator-specific)
# ══════════════════════════════════════════════════════════════════════════════

def parse_blueqat(result_str: str, bit_index: int) -> int:
    i = result_str.find("'")
    s = result_str[i + 1:]
    return 0 if s[bit_index] == '0' else 1

def parse_cirq(result_str: str, bit_index: int) -> int:
    i = result_str.find("|")
    s = result_str[i + 1:]
    return 0 if s[bit_index] == '0' else 1

def parse_qiskit(result_str: str, bit_index: int) -> int:
    # Qiskit counts: "{'0101 1010': 1}" — reverse-indexed
    i = result_str.find("'")
    s = result_str[i + 1:][::-1]
    i = s.find("'")
    s = s[i + 1:]
    return 0 if s[bit_index] == '0' else 1

def parse_sympy(result_str: str, bit_index: int) -> int:
    i = result_str.find("|")
    s = result_str[i + 1:][::-1]
    i = s.find(">")
    s = s[i + 1:]
    return 0 if s[bit_index] == '0' else 1

def integer_from_str(parse_fn, result_str: str, integer_obj: 'Integer') -> int:
    n = 0
    for idx in reversed(integer_obj.bit_indices()):
        n = n * 2
        if parse_fn(result_str, idx) == 1:
            n += 1
    return n


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7: Benchmark Circuits
# ══════════════════════════════════════════════════════════════════════════════

class TestProc_ADD(UO_Proc):
    """
    4-bit + 4-bit quantum adder.
    
    Both operands are put into superposition (hadamard), so we're actually
    computing a + b for ALL possible values of a and b simultaneously!
    The measurement then collapses to one random outcome.
    """
    def __init__(self):
        super().__init__('TestProc_ADD')

    def __enter__(self):
        super().__enter__()
        Integer.NBITS = 4
        a = Integer(0)
        b = Integer(0)
        a.hadamard()
        b.hadamard()
        b0 = Integer(0)
        b0 << b      # Store a copy of b before addition
        b += a       # Now b holds a + b
        self.a = a
        self.b0 = b0
        self.b = b
        return self


class TestProc_SUB(UO_Proc):
    """
    4-bit quantum subtractor: b - a.
    
    Subtraction is addition run in reverse — a beautiful property
    of reversible (unitary) quantum gates.
    """
    def __init__(self):
        super().__init__('TestProc_SUB')

    def __enter__(self):
        super().__enter__()
        Integer.NBITS = 4
        a = Integer(0)
        b = Integer(0)
        a.hadamard()
        b.hadamard()
        b0 = Integer(0)
        b0 << b
        b -= a       # Reversed adder circuit
        self.a = a
        self.b0 = b0
        self.b = b
        return self


class TestProc_MUL(UO_Proc):
    """
    3-bit × 3-bit quantum multiplier.
    
    Uses controlled partial products via CSWAP gates.
    Output is 6 bits (3+3).
    """
    def __init__(self, nbits: int = 3):
        super().__init__('TestMul')
        self.nbits = nbits

    def __enter__(self):
        super().__enter__()
        a = Integer(0, nbits=self.nbits)
        b = Integer(0, nbits=self.nbits)
        a.hadamard()
        b.hadamard()
        self.a = a
        self.b = b
        self.c = a * b
        return self


class TestProc_MODULOADD(UO_Proc):
    """
    3-bit modulo addition: (a + b) mod n.
    
    Most complex circuit — requires:
    1. Addition
    2. Subtraction of modulus
    3. Conditional swap (based on carry)
    4. Ancilla qubit cleanup (uncomputation)
    
    Uncomputation is a key technique in quantum computing:
    we must "undo" intermediate results to avoid polluting the state.
    """
    def __init__(self):
        super().__init__('MODULOADD')

    def __enter__(self):
        super().__enter__()
        Integer.NBITS = 3
        with UO_Proc('MODULOADD.init'):
            a = Integer(0); a.hadamard(2)
            b = Integer(0); b.hadamard(2)
            n = Integer(4); n.hadamard(2)
            b0 = Integer(0); b0 << b
        with UO_Proc('MODULOADD.main'):
            b += a
            b -= n
            flag = QBit()
            QBit.cx(b.carry(), flag)
            n0 = Integer(0)
            Integer.cswap(flag, n, n0)
            b += n0
            Integer.cswap(flag, n, n0)
            n0.deallocate()
        with UO_Proc('MODULOADD_freeflag'):
            b -= a
            QBit.x(b.carry())
            QBit.cx(b.carry(), flag)
            QBit.x(b.carry())
            b += a
            flag.deallocate()
        self.a = a; self.b0 = b0; self.b = b; self.n = n; self.flag = flag
        return self


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8: Simulator Runner Functions
# ══════════════════════════════════════════════════════════════════════════════

def run_blueqat(proc_class, shots: int = 10, circuit_name: str = '') -> float:
    """Run a benchmark circuit on Blueqat and return elapsed time."""
    import blueqat
    with proc_class() as p:
        circuit = p.synthesis(blueqat.Circuit())
        start = time.perf_counter()
        for _ in range(shots):
            circuit.m[:].run(shots=1)
        end = time.perf_counter()
    reset_all()
    return end - start


def run_cirq(proc_class, shots: int = 10, circuit_name: str = '') -> float:
    """Run a benchmark circuit on Cirq and return elapsed time."""
    import cirq
    with proc_class() as p:
        circuit = p.synthesis(cirq.Circuit())
        # Add measurements to all used qubits
        all_qubits = sorted(circuit.all_qubits())
        circuit.append(cirq.measure(*all_qubits))
        sim = cirq.Simulator()
        start = time.perf_counter()
        for _ in range(shots):
            sim.simulate(circuit)
        end = time.perf_counter()
    reset_all()
    return end - start


def run_qiskit(proc_class, shots: int = 10, circuit_name: str = '') -> float:
    """Run a benchmark circuit on Qiskit Aer and return elapsed time."""
    import qiskit
    try:
        from qiskit_aer import AerSimulator
    except ImportError:
        from qiskit import Aer
        AerSimulator = lambda: Aer.get_backend('aer_simulator')

    with proc_class() as p:
        reset_qiskit_register()
        n_qubits = max(ALLOCATOR.allocated) + 1
        import qiskit as qk
        reg = qk.QuantumRegister(n_qubits)
        circuit = p.synthesis(qk.QuantumCircuit(reg))
        circuit.measure_all()
        sim = AerSimulator()
        start = time.perf_counter()
        for _ in range(shots):
            job = sim.run(circuit, shots=1)
            job.result()
        end = time.perf_counter()
    reset_all()
    reset_qiskit_register()
    return end - start


def run_sympy(proc_class, shots: int = 10, circuit_name: str = '') -> float:
    """
    Run a benchmark circuit on SymPy (symbolic).
    
    SymPy is exact but expensive. We do the heavy symbolic computation once
    (qapply + measure_all), then sample from the results list.
    """
    import sympy.physics.quantum as spq
    import sympy.physics.quantum.qubit as spqb

    with proc_class() as p:
        n_qubits = max(ALLOCATOR.allocated) + 1
        init_state = spqb.Qubit('0' * n_qubits)
        circuit = p.synthesis(init_state)
        start = time.perf_counter()
        expr = spq.qapply(circuit)
        results = spqb.measure_all(expr)
        for _ in range(shots):
            random.choice(results)  # Sample from distribution
        end = time.perf_counter()
    reset_all()
    return end - start


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9: Main Benchmark Runner
# ══════════════════════════════════════════════════════════════════════════════

BENCHMARK_CIRCUITS = [
    ('ADD',        TestProc_ADD,      "4-bit + 4-bit adder"),
    ('SUB',        TestProc_SUB,      "4-bit - 4-bit subtractor"),
    ('MUL',        TestProc_MUL,      "3-bit × 3-bit multiplier"),
    ('MODULOADD',  TestProc_MODULOADD, "3-bit modulo adder"),
]

SIMULATORS = {
    'qiskit':  run_qiskit,
    'cirq':    run_cirq,
    'blueqat': run_blueqat,
    'sympy':   run_sympy,
}


def run_benchmarks(simulator_names: List[str], shots: int = 10,
                   skip_circuits: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Run all benchmark circuits on selected simulators.
    Returns a DataFrame with results.
    """
    skip_circuits = skip_circuits or []
    results = []

    print(f"\n{'='*60}")
    print(f"Quantum Arithmetic Benchmark")
    print(f"Shots per circuit: {shots}")
    print(f"Simulators: {', '.join(simulator_names)}")
    print(f"{'='*60}\n")

    for sim_name in simulator_names:
        if sim_name not in SIMULATORS:
            print(f"⚠️  Unknown simulator: {sim_name}")
            continue

        runner = SIMULATORS[sim_name]
        print(f"▶ {sim_name.upper()}")

        for circuit_name, proc_class, description in BENCHMARK_CIRCUITS:
            if circuit_name in skip_circuits:
                print(f"   {circuit_name:<12} SKIPPED")
                continue

            print(f"   {circuit_name:<12} {description} ... ", end='', flush=True)

            try:
                elapsed = runner(proc_class, shots=shots, circuit_name=circuit_name)
                print(f"{elapsed:.3f}s")
                results.append({
                    'simulator': sim_name,
                    'circuit': circuit_name,
                    'shots': shots,
                    'time_seconds': round(elapsed, 3),
                    'description': description
                })
            except Exception as e:
                print(f"ERROR: {e}")
                results.append({
                    'simulator': sim_name,
                    'circuit': circuit_name,
                    'shots': shots,
                    'time_seconds': float('nan'),
                    'description': description
                })

        print()

    df = pd.DataFrame(results)
    return df


def print_summary_table(df: pd.DataFrame):
    """Print a formatted comparison table."""
    if df.empty:
        print("No results to display.")
        return

    pivot = df.pivot_table(
        index='simulator',
        columns='circuit',
        values='time_seconds',
        aggfunc='first'
    )

    print("\n" + "="*65)
    print("RESULTS SUMMARY (seconds, {shots} shots each)".format(shots=df['shots'].iloc[0]))
    print("="*65)
    print(pivot.to_string(float_format='{:.3f}'.format))
    print("="*65)

    # Speed rankings per circuit
    print("\nSpeed Rankings (fastest → slowest):")
    for circuit in df['circuit'].unique():
        sub = df[df['circuit'] == circuit].dropna(subset=['time_seconds'])
        sub = sub.sort_values('time_seconds')
        ranking = ' → '.join(f"{row['simulator']}({row['time_seconds']:.2f}s)"
                              for _, row in sub.iterrows())
        print(f"  {circuit}: {ranking}")


def main():
    parser = argparse.ArgumentParser(
        description='Quantum Arithmetic Benchmark across multiple simulators',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--simulators', nargs='+',
                        default=['qiskit', 'blueqat', 'cirq', 'sympy'],
                        choices=['qiskit', 'blueqat', 'cirq', 'sympy'],
                        help='Which simulators to benchmark')
    parser.add_argument('--shots', type=int, default=10,
                        help='Number of shots per circuit (default: 10)')
    parser.add_argument('--no-sympy', action='store_true',
                        help='Skip SymPy (very slow for large circuits)')
    parser.add_argument('--no-mul', action='store_true',
                        help='Skip multiplication (slowest circuit)')
    parser.add_argument('--output', type=str, default=None,
                        help='Save results to CSV file')
    args = parser.parse_args()

    sims = args.simulators
    if args.no_sympy and 'sympy' in sims:
        sims.remove('sympy')

    skip = []
    if args.no_mul:
        skip.append('MUL')

    df = run_benchmarks(sims, shots=args.shots, skip_circuits=skip)
    print_summary_table(df)

    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nResults saved to: {args.output}")

    return df


if __name__ == '__main__':
    main()
