## ZX-Simplifier: The Diagram Builder Challenge
- Objective: The core objective of "ZX-Simplifier" is to accurately construct specific quantum gate operations by writing corresponding SQASM (Simplified Quantum Assembly) strings. Players must create SQASM code that, when converted into a ZX-diagram and simplified, represents the target quantum gate.

Gameplay:

Levels: The game is structured into multiple levels, each introducing a different target quantum gate (e.g., Identity, Pauli-X, Hadamard, CNOT, Z-Spider with a specific phase).
Target Operation: For each level, you are given a description of the target quantum operation. In the command-line version, you also see the simplified matrix representation of this target.
SQASM Input: Your task is to input an SQASM string that you believe performs the desired quantum operation. SQASM is a textual representation used by the pyzx library to define quantum circuits as ZX-diagrams.
Verification and Simplification: Behind the scenes, the game uses the pyzx library to:
Parse your SQASM string into a ZX-diagram.
Simplify this diagram using pyzx's powerful reduction algorithms. This is crucial because many different SQASM strings can represent the same underlying quantum operation.
Convert the simplified diagram into its matrix representation.
Compare your diagram's matrix with the target matrix. The comparison accounts for global scalar factors, meaning diagrams representing the same physical operation (even if they differ by an overall phase or normalization factor) are considered equivalent.
Feedback and Scoring:
You receive immediate feedback on whether your submitted SQASM correctly generates the target operation.
Successfully completing a level earns you points towards your total score.
Each level has a maximum number of attempts, adding a strategic element to finding the most efficient or correct SQASM.
Game Progression: If you successfully complete a level, you advance to the next, more complex challenge. If you run out of attempts on a level, the game ends.
Skills Required:

This challenge is ideal for anyone interested in:

Quantum Computing: Understanding the fundamental operations of quantum gates.
Quantum Assembly/Circuit Design: Practicing how quantum gates are expressed in a textual format.
ZX-Calculus: Gaining an intuitive understanding of how quantum operations can be represented and simplified using ZX-diagrams, even if you don't manually draw them.
Problem-Solving: Devising creative SQASM sequences to achieve a desired quantum transformation.
