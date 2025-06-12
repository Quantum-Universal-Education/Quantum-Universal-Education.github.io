import pyzx as zx
import numpy as np
import math # Still useful for phases if describing targets in pi

class QuantumGame:
    """
    Manages the game flow for the "Build the Diagram Challenge" using pyzx.
    """
    def __init__(self):
        self.total_score = 0
        self.levels = [
            {
                "name": "Level 1: Build the Identity Gate (1 Qubit)",
                "target_sqasm": "qreg q[1];", # Represents the identity (single wire)
                "description": "Your goal is to write an SQASM string that simplifies to the identity gate on one qubit.",
                "base_score": 100,
                "max_attempts": 3,
                "target_matrix": np.array([[1.+0.j]]) # For direct comparison or display
            },
            {
                "name": "Level 2: Build a Pauli-X Gate (1 Qubit)",
                "target_sqasm": "qreg q[1];x q[0];", # Represents Pauli X
                "description": "Your goal is to write an SQASM string that simplifies to a Pauli-X gate on one qubit.",
                "base_score": 150,
                "max_attempts": 4,
                "target_matrix": np.array([[0.+0.j, 1.+0.j], [1.+0.j, 0.+0.j]]) # Matrix for Pauli X
            },
            {
                "name": "Level 3: Build a Hadamard Gate (1 Qubit)",
                "target_sqasm": "qreg q[1];h q[0];", # Represents Hadamard
                "description": "Your goal is to write an SQASM string that simplifies to a Hadamard gate on one qubit.",
                "base_score": 200,
                "max_attempts": 5,
                "target_matrix": (1/np.sqrt(2)) * np.array([[1.+0.j, 1.+0.j], [1.+0.j, -1.+0.j]]) # Matrix for Hadamard
            },
            {
                "name": "Level 4: Build a CNOT Gate (2 Qubits)",
                "target_sqasm": "qreg q[2];cx q[0],q[1];",
                "description": "Your goal is to write an SQASM string that simplifies to a CNOT gate with q[0] as control and q[1] as target.",
                "base_score": 250,
                "max_attempts": 6,
                "target_matrix": np.array([
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0]
                ])
            },
            {
                "name": "Level 5: Build a Z-Spider (Phase pi/2)",
                # This uses a specific feature of SQASM for Z-spiders directly
                # A Z spider with phase 0.5pi on a single qubit
                "target_sqasm": "qreg q[1]; s q[0];", # 's' gate applies Z(pi/2)
                "description": "Your goal is to write an SQASM string that creates a Z-spider with a phase of pi/2 (e.g., an S gate) on one qubit.",
                "base_score": 300,
                "max_attempts": 7,
                "target_matrix": np.array([[1.+0.j, 0.+0.j], [0.+0.j, 0.+1.j]]) # Matrix for S gate
            }
            # Add more levels as you like, potentially with more complex gates or multiple qubits
        ]

    def _get_diagram_matrix(self, sqasm_string):
        """
        Helper to convert an SQASM string into a pyzx Graph and get its matrix representation.
        Includes simplification.
        """
        try:
            # Create the pyzx graph from SQASM
            g = zx.sqasm(sqasm_string)
            
            # Reduce the diagram to its simplest form before getting the matrix
            # This is crucial because different SQASM strings can represent the same
            # operation, and simplification makes them comparable.
            zx.full_reduce(g)

            # Get the matrix. preserve_scalar=False ensures we get the exact scalar factor.
            # We then handle proportionality in _check_equivalence.
            return g.to_matrix(preserve_scalar=False)
        except Exception as e:
            print(f"Error parsing or processing SQASM: {e}")
            return None

    def _check_equivalence(self, user_matrix, target_matrix, tolerance=1e-9):
        """
        Checks if two complex matrices are equivalent, considering a global scalar factor.
        This handles cases where matrices represent the same operation but differ by a scalar (e.g., normalization).
        """
        if user_matrix is None or target_matrix is None:
            return False

        if user_matrix.shape != target_matrix.shape:
            print(f"Matrix shape mismatch: User ({user_matrix.shape}) vs Target ({target_matrix.shape})")
            return False

        # Handle zero matrices explicitly to avoid division by zero
        if np.allclose(target_matrix, 0, atol=tolerance):
            return np.allclose(user_matrix, 0, atol=tolerance)

        # Find a non-zero element in target to establish a reference ratio
        # Flatten and iterate to find the first non-zero element reliably
        target_flat = target_matrix.flatten()
        user_flat = user_matrix.flatten()

        non_zero_idx = -1
        for i, val in enumerate(target_flat):
            if not np.isclose(val, 0, atol=tolerance):
                non_zero_idx = i
                break

        if non_zero_idx == -1: # Target matrix is all zeros, handled above
            return False

        target_ref = target_flat[non_zero_idx]
        user_ref = user_flat[non_zero_idx]

        # Calculate scalar factor based on reference elements
        if np.isclose(target_ref, 0, atol=tolerance):
            # This case should ideally not be reached if non_zero_idx is correctly found
            return False 
        
        scalar_factor = user_ref / target_ref

        # Check if all elements are proportional by this scalar factor
        return np.allclose(user_matrix, scalar_factor * target_matrix, atol=tolerance)

    def play_level(self, level_info):
        """
        Plays a single level of the "Build the Diagram Challenge".
        """
        level_name = level_info["name"]
        description = level_info["description"]
        target_sqasm = level_info["target_sqasm"]
        base_score = level_info["base_score"]
        max_attempts = level_info["max_attempts"]
        target_matrix = level_info["target_matrix"] # Pre-calculated target matrix for display

        print(f"\n--- Starting {level_name} ---")
        print(description)
        print("\nTarget Diagram's Matrix (simplified):")
        # numpy.set_printoptions helps in pretty-printing complex matrices
        np.set_printoptions(precision=4, suppress=True)
        print(target_matrix)
        print("--------------------------------------")

        attempts = 0
        level_won = False

        while attempts < max_attempts:
            print(f"\n--- Attempt {attempts + 1}/{max_attempts} for {level_name} ---")
            print("Enter your SQASM string (multiline input, type 'END' on a new line to finish):")
            user_sqasm_lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                user_sqasm_lines.append(line)
            user_sqasm_string = "\n".join(user_sqasm_lines)

            user_matrix = self._get_diagram_matrix(user_sqasm_string)

            if user_matrix is None:
                print("Invalid SQASM. Please try again.")
                attempts += 1
                continue

            print("\nYour Diagram's Matrix (simplified):")
            print(user_matrix)

            if self._check_equivalence(user_matrix, target_matrix):
                level_won = True
                break
            else:
                print("Your diagram is not equivalent to the target. Keep trying!")
                attempts += 1

        level_score = 0
        if level_won:
            print(f"\n⭐⭐⭐ You successfully completed {level_name}! ⭐⭐⭐")
            level_score = base_score
            print(f"Score for {level_name}: {level_score}")
        else:
            print(f"\nTime's up for {level_name}! You ran out of attempts.")
            print(f"The correct SQASM for this level was:\n{target_sqasm}")
            print("Keep practicing!")

        self.total_score += level_score
        print(f"Current Total Score: {self.total_score}")
        return level_won

    def start_game(self):
        """
        Starts the main game, playing through all defined levels.
        """
        print("Welcome to ZX-Simplifier: The Diagram Builder!")
        print("Your challenge is to write SQASM strings that represent target quantum operations.")
        print("Good luck!")

        for i, level_info in enumerate(self.levels):
            if not self.play_level(level_info):
                print("\nGame Over! You failed to complete a level.")
                break

            if i < len(self.levels) - 1:
                input("\nPress Enter to proceed to the next level...")
            else:
                print("\nCongratulations! You have completed all levels!")
        
        print(f"\n--- Game Finished ---")
        print(f"Your Final Score: {self.total_score}")
        print("Thanks for playing ZX-Simplifier!")
