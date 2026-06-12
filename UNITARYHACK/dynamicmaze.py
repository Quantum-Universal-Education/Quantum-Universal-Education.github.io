import random

WIDTH = 7
HEIGHT = 7


class QuantumMaze:
    def __init__(self):
        self.player_x = 0
        self.player_y = 0
        self.exit_x = WIDTH - 1
        self.exit_y = HEIGHT - 1

        self.coherence = 20
        self.scans = 3

    def generate_hazards(self):
        hazards = set()

        for _ in range(random.randint(4, 8)):
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)

            if (x, y) not in [
                (self.player_x, self.player_y),
                (self.exit_x, self.exit_y),
            ]:
                hazards.add((x, y))

        return hazards

    def display(self):
        print("\n=== QUANTUM MAZE ===")
        print(f"Coherence: {self.coherence}")
        print(f"Scans Left: {self.scans}")
        print()

        for y in range(HEIGHT):
            row = ""

            for x in range(WIDTH):
                if (x, y) == (self.player_x, self.player_y):
                    row += " Q "
                elif (x, y) == (self.exit_x, self.exit_y):
                    row += " E "
                else:
                    row += " . "

            print(row)

    def scan(self):
        if self.scans <= 0:
            print("\nNo scans remaining!")
            return

        self.scans -= 1

        distance = abs(self.player_x - self.exit_x) + abs(
            self.player_y - self.exit_y
        )

        print("\nQuantum Scan Activated!")

        if distance <= 3:
            print("The exit is very close!")
        elif distance <= 6:
            print("The exit signal is moderate.")
        else:
            print("The exit feels far away.")

        if random.random() < 0.3:
            self.coherence -= 1
            print("Scan caused decoherence! -1 coherence")

    def move(self, direction):
        nx = self.player_x
        ny = self.player_y

        if direction == "w":
            ny -= 1
        elif direction == "s":
            ny += 1
        elif direction == "a":
            nx -= 1
        elif direction == "d":
            nx += 1

        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
            self.player_x = nx
            self.player_y = ny
        else:
            print("Quantum boundary detected!")
            self.coherence -= 1

    def play(self):
        print("Welcome to Quantum Maze!")
        print("Reach the exit (E) before coherence reaches zero.")
        print("Controls: W A S D to move, Q to scan")
        print()

        while self.coherence > 0:

            hazards = self.generate_hazards()

            self.display()

            action = input("\nAction: ").lower().strip()

            if action == "q":
                self.scan()
                continue

            if action in ["w", "a", "s", "d"]:
                self.move(action)
            else:
                print("Invalid action.")
                continue

            self.coherence -= 1

            if (self.player_x, self.player_y) in hazards:
                loss = random.randint(2, 4)
                self.coherence -= loss

                print(
                    f"\nYou entered a quantum anomaly!"
                )
                print(f"Lost {loss} coherence!")

            if random.random() < 0.15:
                gain = random.randint(1, 3)
                self.coherence += gain

                print(
                    f"\nYou found a coherence crystal!"
                )
                print(f"Gained {gain} coherence!")

            if (
                self.player_x == self.exit_x
                and self.player_y == self.exit_y
            ):
                print("\nYou escaped the Quantum Maze!")
                print(
                    f"Remaining Coherence: {self.coherence}"
                )
                return

        print("\nYour quantum state fully decohered.")
        print("Game Over.")


if __name__ == "__main__":
    game = QuantumMaze()
    game.play()
