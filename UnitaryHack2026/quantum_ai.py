"""
quantum_ai.py
-------------
The brain of the Quantum Crows. This module is the "tutorial spine" of the
whole project: every function below corresponds to one teachable quantum
computing concept, in the order you'd encounter it in an intro course.

THE BIG IDEA
============
We want the Crows to move as a coordinated "hive," picking whichever single
move brings the flock closest to a stable arrangement (a Nash equilibrium of
the underlying game). Finding that arrangement classically means checking
every possible split of birds between the two coops -- which doubles in cost
with every additional bird (2^n). That is exactly the kind of combinatorial
search problem where quantum computers offer a genuine, structural advantage
in principle (even though here, on a simulator, we are mostly *demonstrating*
the technique rather than racing classical computers).

THE PIPELINE (each step = one concept):

  1. Game state  -->  Boolean satisfiability problem (NAE-SAT)
       "Concept: problem encoding". Real-world puzzles become logic clauses.

  2. NAE-SAT  -->  NAE-3-SAT  -->  Max-Cut graph
       "Concept: problem reduction". Many NP-hard problems are secretly the
       same problem in disguise. Max-Cut: split a graph's nodes into two
       groups to cut as many heavy edges as possible.

  3. Max-Cut graph  -->  quantum circuit (qubits = nodes, gates = edges)
       "Concept: superposition". Every qubit starts as Hadamard(|0>), i.e.
       a coin-flip of every possible split, all at once.

  4. Cost gates (RZZ between connected qubits)
       "Concept: entanglement & phase". Connected birds' qubits become
       linked: flipping one affects the relative phase of the joint state.

  5. Mixing gates (RX), repeated over several time-steps with a shifting
     ratio of "cost" vs "mixing" strength
       "Concept: quantum annealing / interference". Good splits' amplitudes
       reinforce each other (constructive interference); bad splits cancel
       out (destructive interference) -- a tiny taste of the same physics
       behind Grover's algorithm and adiabatic quantum computing.

  6. Measurement
       "Concept: wavefunction collapse". Until you measure, the circuit
       represents many candidate splits simultaneously. Measuring forces
       one definite classical answer, with the best splits being the most
       *likely* outcomes, not the only possible ones.

The chosen split tells the Crows where they'd ideally like every bird to be.
The AI then makes the single legal move (flip one of its own birds) that
gets the flock closest to that target -- this is `pick_best_move()`.
"""

import random

import numpy as np
import networkx as nx

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


# ---------------------------------------------------------------------------
# STEP 1: Game state -> Not-All-Equal SAT clauses
# ---------------------------------------------------------------------------

_aux_id = 0


def _next_aux_id():
    global _aux_id
    _aux_id -= 1
    return _aux_id


class AuxVar:
    """Lightweight stand-in object so auxiliary variables can be treated
    like Birds when building the graph (they just need an .id)."""
    def __init__(self):
        self.id = _next_aux_id()


def state_to_nae_clauses(birds):
    """
    STEP 1 -- Concept: encoding a real situation as boolean logic.

    For each feather-gene slot (a, b, c) and each value it can take
    (True/False), gather every bird that currently expresses that value.
    Each such group becomes a "Not-All-Equal" clause: birds in the same
    clause are pulling toward the same side, and the optimizer will try to
    keep them grouped (not splitting them all equally), which models flock
    cohesion / peer pressure within a shared trait.
    """
    clauses = {gene + str(val): [] for gene in ["a", "b", "c"] for val in [True, False]}
    for bird in birds:
        for gene in ["a", "b", "c"]:
            if bird.genes[gene] is not None:
                clauses[gene + str(bird.genes[gene])].append(bird)
    return clauses


# ---------------------------------------------------------------------------
# STEP 2: NAE-SAT -> NAE-3-SAT -> Max-Cut graph
# ---------------------------------------------------------------------------

def nae_to_nae3(clause):
    """
    STEP 2a -- Concept: problem reduction (turning a clause of any size into
    only-size-3 clauses by chaining in auxiliary variables). This is a
    standard trick in computational complexity: reduce a general problem to
    a more restricted, well-studied special case (here, NAE-3-SAT).
    """
    k = len(clause)
    if k == 0 or k == 1:
        # A clause with 0 or 1 members has no real "not-all-equal" constraint
        # to express (you need at least 2 literals for "not all the same"
        # to mean anything), so it contributes nothing to the graph.
        return []
    if k == 2:
        aux = AuxVar()
        return [
            [(clause[0], True), (clause[1], True), (aux, True)],
            [(clause[0], False), (clause[1], False), (aux, True)],
        ]
    if k == 3:
        return [[(c, True) for c in clause]]

    # k > 3: chain auxiliary variables together
    aux_chain = [AuxVar() for _ in range(k - 3)]
    triples = [[(clause[0], True), (clause[1], True), (aux_chain[0], True)]]
    for i in range(1, k - 3):
        triples.append([(aux_chain[i - 1], False), (clause[i + 1], True), (aux_chain[i], True)])
    triples.append([(aux_chain[-1], False), (clause[-2], True), (clause[-1], True)])
    return triples


def nae3_to_graph(variables, clauses):
    """
    STEP 2b -- Concept: NAE-3-SAT is exactly Max-Cut on a graph built from
    its clauses. Every variable becomes two graph nodes -- "X is true" and
    "X is false" -- linked by a heavy edge (so a good cut never puts a
    variable on both sides of itself). Every clause becomes a small triangle
    of light edges between its three literals, because "not all equal"
    inside a clause is the same as "cut at least one edge of that triangle."
    """
    m = len(clauses)
    G = nx.Graph()
    for var in variables:
        G.add_node(f"T_{var.id}")
        G.add_node(f"F_{var.id}")
    for var in variables:
        # heavy "consistency" edge: a variable can't be true and false at once
        G.add_edge(f"T_{var.id}", f"F_{var.id}", weight=10 * max(m, 1))

    def label(literal):
        var, is_true = literal
        return f"T_{var.id}" if is_true else f"F_{var.id}"

    for clause in clauses:
        if len(clause) != 3:
            continue
        l0, l1, l2 = label(clause[0]), label(clause[1]), label(clause[2])
        G.add_edge(l0, l1, weight=1)
        G.add_edge(l0, l2, weight=1)
        G.add_edge(l1, l2, weight=1)
    return G


def get_weight_matrix(graph):
    """Flatten the graph into a plain weight matrix, indexed 0..n-1."""
    nodes = list(graph.nodes)
    n = len(nodes)
    index_of = {node: i for i, node in enumerate(nodes)}
    weights = np.zeros((n, n))
    for u, v, data in graph.edges(data=True):
        weights[index_of[u], index_of[v]] = data["weight"]
        weights[index_of[v], index_of[u]] = data["weight"]
    return weights, nodes, index_of


# ---------------------------------------------------------------------------
# STEPS 3-6: build & run the quantum annealing-style circuit
# ---------------------------------------------------------------------------

def build_annealing_circuit(weights, time_steps=4):
    """
    Builds the quantum circuit step by step. Returns the circuit AND a list
    of "snapshots" (partial circuits) after each major stage, so the game UI
    can show the circuit growing piece by piece for the tutorial.

    weights: square numpy array of edge weights between qubits (nodes)
    time_steps: how many alternating mix/cost rounds to anneal through
    """
    n = len(weights)
    if n == 0:
        # Degenerate case: the current flock state produced no NAE
        # constraints at all (e.g. every gene clause currently has fewer
        # than 2 members). There's nothing to anneal -- return an empty
        # circuit with no qubits so the caller can fall back gracefully.
        qc = QuantumCircuit(0, 0)
        return qc, [("Superposition", qc.copy()), ("Measurement", qc.copy())]

    max_weight = np.max(weights) if np.max(weights) > 0 else 1.0
    qc = QuantumCircuit(n, n)
    snapshots = []

    # --- STEP 3: Superposition ---
    # Concept: Hadamard gates put every qubit into an equal mix of |0> and
    # |1>. With n qubits this single layer represents a superposition of
    # all 2^n possible coop arrangements simultaneously.
    for q in range(n):
        qc.h(q)
    snapshots.append(("Superposition", qc.copy()))

    # --- STEPS 4 & 5: Cost + Mixing layers, annealed over time ---
    # Concept: quantum annealing. Early on we mix heavily (explore broadly);
    # later we lean on the cost Hamiltonian (lock in good splits). The RZZ
    # gate entangles two qubits' phases according to the strength of their
    # graph edge -- pairs with a heavy edge get pushed hard toward
    # "different sides," exactly mirroring the Max-Cut objective.
    for t in range(time_steps):
        cost_strength = (t + 1) / (time_steps + 1) / 2     # ramps up
        mix_strength = 0.5 - cost_strength                   # ramps down

        for q in range(n):
            qc.rx(mix_strength, q)

        for i in range(n):
            for j in range(i + 1, n):
                if weights[i, j] != 0:
                    angle = -cost_strength * weights[i, j] / max_weight
                    qc.rzz(angle, i, j)

        snapshots.append((f"Anneal step {t + 1}/{time_steps}", qc.copy()))

    # --- STEP 6: Measurement ---
    # Concept: collapse. The superposition of all candidate splits is
    # forced into one classical bitstring. Splits that interfered
    # constructively are exponentially more likely to be the one we see.
    qc.measure(range(n), range(n))
    snapshots.append(("Measurement", qc.copy()))

    return qc, snapshots


def run_circuit(qc, shots=2000, optimization_level=3):
    """Run on Qiskit Aer's local simulator and return the measurement
    counts -- a histogram of which classical bitstrings appeared, and how
    often. This is the closest a simulator gets to showing you genuine
    quantum statistics.

    optimization_level controls how hard Qiskit's transpiler works to
    simplify the circuit before running it (0 = no optimization, 3 = most
    aggressive). Concept: real quantum hardware has limited qubit
    connectivity and noisy gates, so transpilation rewrites a circuit into
    an equivalent but shallower/cheaper one. We default to level 3 so the
    game stays snappy even as the flock (and qubit count) grows -- more
    birds means more NAE-3-SAT clauses, which means more gates, which means
    transpilation matters more, not less.
    """
    backend = AerSimulator()
    transpiled = transpile(qc, backend, optimization_level=optimization_level)
    job = backend.run(transpiled, shots=shots)
    result = job.result()
    return result.get_counts()


def best_bitstring(counts):
    """The bitstring measured most often is our annealed answer -- the
    split the quantum circuit 'voted for' most strongly."""
    winner = max(counts, key=counts.get)
    # Qiskit returns bitstrings with qubit 0 as the *rightmost* character
    return [int(b) for b in reversed(winner)]


def top_results(counts, n=5):
    """
    Concept: a probability distribution, made visible.

    Returns the top `n` most-measured bitstrings as a list of
    (bitstring_str, count, probability) tuples, sorted from most to least
    likely. This is what makes "the computer thought about it" visibly
    probabilistic rather than a black box that just spits out one answer:
    the player can see that the winning split was, say, 34% likely, with
    several runner-up splits close behind -- not the only outcome the
    circuit could ever produce.
    """
    total_shots = sum(counts.values())
    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return [
        (bitstring, count, count / total_shots if total_shots else 0.0)
        for bitstring, count in ranked[:n]
    ]


def cut_value(bitstring, weights):
    """Classical scorekeeping: how much total edge-weight does this split
    actually cut? Used to judge how good the quantum answer turned out to be,
    and (optionally) compare against brute force for small graphs."""
    n = len(weights)
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += weights[i, j] * bitstring[i] * (1 - bitstring[j])
    return total


def brute_force_best_cut(weights):
    """
    Classical baseline for comparison (only practical for small bird
    counts -- this is exactly the 2^n wall the quantum approach is trying
    to sidestep). Useful in the tutorial to show 'here's the true best
    answer' vs 'here's what the quantum circuit found.'
    """
    n = len(weights)
    best_score, best_bits = -1, None
    for bits_int in range(2 ** n):
        bits = [(bits_int >> i) & 1 for i in range(n)]
        score = cut_value(bits, weights)
        if score > best_score:
            best_score, best_bits = score, bits
    return best_bits, best_score


# ---------------------------------------------------------------------------
# Top-level orchestration used by the game
# ---------------------------------------------------------------------------

class QuantumFlockMind:
    """
    Wraps the whole pipeline for one "turn" of AI thinking. Construct it
    with the current list of birds; it builds the graph, runs the quantum
    circuit, and exposes everything the UI needs to narrate the process.

    time_steps is effectively the Hive's "intelligence dial": it's how many
    alternating mix/cost rounds the annealing schedule gets to work with
    before measurement. Concept: annealing schedule length.
        - Fewer steps (e.g. 2): the circuit barely leaves "explore broadly"
          before being measured, so the cost Hamiltonian never gets to
          dominate. The resulting distribution stays close to uniform --
          lots of near-equally-likely outcomes, i.e. more "noise."
        - More steps (e.g. 10+): the schedule has time to ramp the cost
          Hamiltonian's strength much higher relative to mixing, so
          constructive interference has more rounds to reinforce the truly
          good splits. The distribution sharpens around the best answer(s)
          -- i.e. more "converged," more confidently optimal play.
    This is exposed in the UI as a difficulty control: low time_steps makes
    for a beatable, somewhat erratic Hive; high time_steps makes for a
    sharper, more consistently optimal one.
    """

    def __init__(self, birds, time_steps=4):
        self.birds = birds
        self.time_steps = time_steps
        self.clauses_by_key = state_to_nae_clauses(birds)
        self.nae3_clauses = []
        for key, group in self.clauses_by_key.items():
            self.nae3_clauses.extend(nae_to_nae3(group))

        self.variables = []
        for clause in self.nae3_clauses:
            for var, _ in clause:
                if var not in self.variables:
                    self.variables.append(var)
        # Bugfix: a bird whose genes are all unshared with any other bird
        # (e.g. a freshly bred chick with a rare gene combination) never
        # appears in any NAE-3 clause, and so never became a graph
        # variable here -- meaning the quantum circuit never produced a
        # measured bit for it, and pick_best_move() had to fall back to
        # picking blindly (effectively ignoring the quantum result for
        # that bird). Every bird is now added as a variable explicitly,
        # so every bird always gets two graph nodes (with the usual
        # heavy consistency edge between them) and always gets a real
        # measured bit, even when it has no NAE clause edges of its own.
        for bird in birds:
            if bird not in self.variables:
                self.variables.append(bird)

        self.graph = nae3_to_graph(self.variables, self.nae3_clauses)
        self.weights, self.node_order, self.node_index = get_weight_matrix(self.graph)
        self.circuit, self.snapshots = build_annealing_circuit(self.weights, time_steps)
        self.counts = None
        self.solution_bits = None
        self.top_results = None

    def think(self, shots=2000):
        """Run the circuit and store results. Call once per AI turn."""
        if len(self.weights) == 0:
            self.counts = {}
            self.solution_bits = []
            self.top_results = []
            return self.solution_bits
        self.counts = run_circuit(self.circuit, shots=shots)
        self.solution_bits = best_bitstring(self.counts)
        self.top_results = top_results(self.counts, n=5)
        return self.solution_bits

    def target_side_for_bird(self, bird):
        """
        Looks up what side ('True' literal node) the quantum solution
        assigned to this bird's variable, returning True/False/None
        (None if, oddly, the bird never appeared as a variable).
        """
        node = f"T_{bird.id}"
        if node not in self.node_index:
            return None
        idx = self.node_index[node]
        # bit == 1 means this node is on the "cut" side; we treat that as
        # "the hive wants this bird's coop-side flipped to True/side-A"
        return bool(self.solution_bits[idx])

    def pick_best_move(self, movable_birds):
        """
        Of the birds the AI is allowed to move, pick the one whose current
        side most disagrees with the quantum-annealed target -- i.e. the
        single legal move that brings the flock closest to equilibrium.

        With every bird now guaranteed to be a graph variable (see the
        fix in __init__), every movable bird should have a real
        quantum-derived target. The random fallback below only exists as
        a defensive last resort (e.g. an empty graph with zero qubits)
        and intentionally does NOT default to movable_birds[0], since
        always picking the same list position isn't actually random and
        would silently look like a deterministic "non-quantum" policy.
        """
        best_bird, best_gap = None, -1
        for bird in movable_birds:
            target = self.target_side_for_bird(bird)
            if target is None:
                continue
            gap = 1 if bird.side != target else 0
            if gap > best_gap:
                best_gap, best_bird = gap, bird
        if best_bird is not None:
            return best_bird
        return random.choice(movable_birds) if movable_birds else None
