# ZX-Simplifier: A Quantum Diagram Game

This project implements a command-line game to help you learn and practice
simplifying quantum ZX-diagrams using fundamental rewrite rules.

## Project Structure
# ZX-TheGame: Rules and File Overview

This document outlines the key files and structure of the **ZX-TheGame** project — a command-line game designed to help you learn and practice ZX-calculus simplification rules through interactive levels and challenges.

---

## 📁 Project Directory Structure

```bash
ZX-TheGame/
├── ZX-Rules.md                   # ← You're here: Overview of rules and file roles
├── getting-started-in quantum.md # Beginner guide to ZX-calculus and running the game
├── advance-level-rules.md       # Advanced simplification rules and strategies
├── Code-explanation.md          # Detailed explanation of how core game code works
├── zx.py                        # Core implementation of ZXDiagram, Node, and transformation logic
├── zx-pygame.py                 # Optional Pygame version for interactive GUI (in development)
├── Build-the-circuit-challenge.py # Circuit construction challenge levels (custom puzzles)
├── Level2.py                    # Script for Level 2 puzzle logic and flow
└── run_game.py                  # Main entry script to launch the game
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
