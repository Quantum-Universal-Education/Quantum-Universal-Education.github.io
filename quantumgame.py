import random

class QuantumExplorer:
    def __init__(self):
        self.energy = 10
        self.score = 0
        self.states = ["|0⟩", "|1⟩", "|+⟩", "|-⟩"]
        self.target = random.choice(self.states)

    def measure(self):
        outcome = random.choice(self.states)

        print(f"\nMeasurement result: {outcome}")

        if outcome == self.target:
            self.score += 1
            self.energy += 2
            print("Quantum resonance achieved!")
            print("+1 Score, +2 Energy")
            self.target = random.choice(self.states)
        else:
            self.energy -= 1
            print("Wavefunction collapsed incorrectly.")
            print("-1 Energy")

    def quantum_jump(self):
        self.energy -= 2

        if random.random() < 0.5:
            self.score += 2
            print("\nSuccessful quantum jump!")
            print("+2 Score")
        else:
            print("\nQuantum decoherence occurred!")
            print("No reward.")

    def show_status(self):
        print("\n-----------------------")
        print(f"Energy: {self.energy}")
        print(f"Score : {self.score}")
        print(f"Target State: {self.target}")
        print("-----------------------")

    def play(self):
        print("=== QUANTUM EXPLORER ===")
        print("Find the target quantum state.")
        print("Survive as long as possible.\n")

        while self.energy > 0:
            self.show_status()

            print("\nActions:")
            print("1. Measure")
            print("2. Quantum Jump")
            print("3. Quit")

            choice = input("\nChoose action: ")

            if choice == "1":
                self.measure()

            elif choice == "2":
                self.quantum_jump()

            elif choice == "3":
                print("\nExiting simulation...")
                break

            else:
                print("Invalid choice.")

        print("\n=== GAME OVER ===")
        print(f"Final Score: {self.score}")


if __name__ == "__main__":
    game = QuantumExplorer()
    game.play()
