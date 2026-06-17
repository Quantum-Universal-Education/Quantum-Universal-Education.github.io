"""
cost_function.py
-----------------
Concept: distance in state-space.

This module is a STANDALONE, ALTERNATIVE way to turn the quantum-annealed
target arrangement into a single legal move, operating on the whole flock
as one bitstring and Euclidean distance (closer in spirit to the original
MILQ Simulator's cost_function.py). The main game (cluck_and_crow.py) uses
the simpler per-bird comparison in QuantumFlockMind.pick_best_move() instead,
but this version is kept here as a reference -- and as a nice example of how
the same idea ("which legal move gets me closest to the quantum answer?")
can be implemented multiple equivalent ways. Feel free to swap it in.

Given the flock's current arrangement and the quantum-annealed "ideal"
arrangement, this finds which single legal flip (one bird crossing to the
other coop) gets us closest to that ideal -- measured with ordinary
Euclidean distance between the two bitstrings.
"""

from numpy.linalg import norm
from numpy import array


def closest_legal_move(current_state, optimal_state, movable_indices):
    """
    current_state:  list[int] of 0/1, current side of every tracked bird-bit
    optimal_state:  list[int] of 0/1, the quantum-annealed target state
    movable_indices: which positions in current_state are allowed to flip

    Returns the resulting state (as a numpy array) after the single best
    flip. Raises if there are no legal moves to consider.
    """
    if not movable_indices:
        raise ValueError("No movable indices provided -- nothing this side can legally flip.")

    candidates = []
    for i in movable_indices:
        flipped = list(current_state)
        if current_state[i] not in (0, 1):
            raise ValueError("Error: state bits must be 0 or 1")
        flipped[i] = 1 - current_state[i]
        candidates.append((i, array(flipped)))

    optimal = array(optimal_state)
    best_index, best_state = candidates[0]
    best_distance = norm(optimal - best_state)
    for i, state in candidates[1:]:
        d = norm(optimal - state)
        if d < best_distance:
            best_distance = d
            best_index, best_state = i, state

    return best_index, best_state
