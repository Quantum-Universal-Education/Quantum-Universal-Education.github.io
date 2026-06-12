import random

class QuantumTicTacToe:
    def __init__(self):
        self.board = [[] for _ in range(9)]
        self.player = "X"
        self.move_id = 1

    def display(self):
        print("\nBoard:")
        for r in range(3):
            row = []
            for c in range(3):
                idx = r * 3 + c
                if len(self.board[idx]) == 0:
                    row.append(str(idx))
                elif len(self.board[idx]) == 1 and isinstance(self.board[idx][0], str):
                    row.append(self.board[idx][0])
                else:
                    row.append(f"Q{len(self.board[idx])}")
            print(" | ".join(row))
        print()

    def quantum_move(self, pos1, pos2):
        move_label = f"{self.player}{self.move_id}"

        self.board[pos1].append(move_label)
        self.board[pos2].append(move_label)

        print(f"{self.player} creates quantum move {move_label} between {pos1} and {pos2}")

        self.move_id += 1

        if len(self.board[pos1]) >= 4:
            self.measure(pos1)

        if len(self.board[pos2]) >= 4:
            self.measure(pos2)

        self.player = "O" if self.player == "X" else "X"

    def measure(self, square):
        print(f"\n⚛ Measurement triggered at square {square}!")

        quantum_moves = [m for m in self.board[square] if not isinstance(m, str) or len(m) > 1]

        if not quantum_moves:
            return

        chosen = random.choice(self.board[square])

        winner_symbol = chosen[0]

        self.board[square] = [winner_symbol]

        print(f"Square {square} collapsed into {winner_symbol}\n")

    def check_winner(self):
        classical = []

        for cell in self.board:
            if len(cell) == 1 and cell[0] in ["X", "O"]:
                classical.append(cell[0])
            else:
                classical.append(None)

        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for a,b,c in wins:
            if classical[a] and classical[a] == classical[b] == classical[c]:
                return classical[a]

        return None


def main():
    game = QuantumTicTacToe()

    print("=== Quantum Tic-Tac-Toe ===")
    print("Each move occupies TWO squares in superposition.")
    print("If a square gets crowded, it may collapse!\n")

    while True:
        game.display()

        winner = game.check_winner()
        if winner:
            print(f"🏆 {winner} wins the quantum universe!")
            break

        try:
            p1 = int(input(f"{game.player} first square: "))
            p2 = int(input(f"{game.player} second square: "))

            if p1 == p2:
                print("Choose two different squares.")
                continue

            if not (0 <= p1 < 9 and 0 <= p2 < 9):
                print("Squares must be 0-8.")
                continue

            game.quantum_move(p1, p2)

        except ValueError:
            print("Enter valid numbers.")


if __name__ == "__main__":
    main()
