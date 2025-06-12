# ZX-Simplifier: A Quantum Diagram Game

This project implements a command-line game to help you learn and practice
simplifying quantum ZX-diagrams using fundamental rewrite rules.

## Project Structure

* `zx_TheGame/`: This directory contains the core implementation of the ZX-calculus elements.
    * `zx.py`: Defines the `Node` (for spiders, Hadamard, wire ends), `ZXDiagram` (for graph representation), and `ZXRules` (for applying rewrite rules) classes.
* `game/`: This directory contains the game-specific logic.
    * `quantum_game.py`: Defines the `QuantumGame` class, which manages levels, scoring, and user interaction.
* `run_game.py`: The main script to run the game.

## How to Run

1.  **Navigate to the `zx_game_package` directory:**
    ```bash
    cd zx_game_package
    ```
2.  **Run the game script:**
    ```bash
    python run_game.py
    ```

## Game Play

The game presents you with various ZX-diagrams and a set of rewrite rules.
Your goal is to apply these rules strategically to simplify the diagram down to a
single, direct wire (representing an identity operation). Each level has an
optimal number of moves for maximum score.

**Available Rules:**

1.  **Spider Fusion:** Merge two adjacent spiders of the same color.
2.  **Identity Rule:** Remove a 0-phase spider with exactly two connections.
3.  **Hadamard Color Change:** Apply a Hadamard gate to a spider, changing its color and removing the Hadamard node.

Follow the on-screen prompts to input rule choices and node IDs.

## Dependencies

* Python 3.x (standard library only)

Enjoy simplifying!
