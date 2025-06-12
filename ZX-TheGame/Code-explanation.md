# 📘 Code Explanation: Quantum Diagram Simplifier - A ZX-Calculus Game

This document provides a detailed explanation of the Python code used to build the **ZX-Simplifier** game — a puzzle-style application that helps users learn and interact with the ZX-calculus rules through step-by-step diagram simplification.

---

## 🧩 Node Class

### `__init__(self, node_id, node_type, phase=0.0)`
- Initializes a new **Node** object.
- **Parameters:**
  - `node_id`: A unique identifier for the node.
  - `node_type`: Can be `'Z'`, `'X'`, `'H'`, or `'WIRE_END'`.
  - `phase`: A real number between `[0, 2π)` relevant only for spiders.
- **Connections**: Maintains a set of connected node IDs for efficient lookup and no duplicates.

### `__repr__(self)`
- Returns a readable string representation of the node for debugging and diagram visualization.
- Example: `Z(1, φ=0.50π)`

---

## 📐 ZXDiagram Class

### `__init__(self)`
- Creates an empty diagram structure.
- Maintains:
  - `nodes`: A dictionary mapping `node_id` to `Node` objects.
  - `next_node_id`: Auto-increments as new nodes are added.

### `add_node(node_type, phase=0.0)`
- Adds a new node to the diagram with optional phase.
- Returns the `node_id` of the new node.

### `add_connection(id1, id2)`
- Creates a **bidirectional connection** between two nodes by updating their `connections` sets.

### `remove_node(node_id)`
- Deletes a node and removes all its connections in both directions.

### `remove_connection(id1, id2)`
- Removes a specific connection between two nodes.

### `get_neighbors(node_id)`
- Returns a set of connected node IDs for the given node.

### `get_node(node_id)`
- Returns the `Node` object associated with `node_id`, or `None` if not found.

### `display(self)`
- Prints the entire diagram state clearly:
  - Lists all nodes
  - Lists each node's connections

### `simplify_phase(self, phase)`
- Ensures all phase values are wrapped within `[0, 2π)`, which is a standard domain in ZX-calculus.

---

## 🔁 ZXRules Class

This class provides **static rewrite rules** that directly modify the `ZXDiagram` in place.

### `apply_spider_fusion(diagram, node_id1, node_id2)`
- **Purpose**: Fuse two connected spiders of the same color.
- **Checks**:
  - Both nodes must exist.
  - Both must be spiders (`Z` or `X`) and of the same type.
  - They must be directly connected.
- **Action**:
  - Combine phases.
  - Merge connections from `node_id2` into `node_id1`.
  - Remove `node_id2`.

### `apply_identity_rule(diagram, node_id)`
- **Purpose**: Remove an identity spider.
- **Checks**:
  - Node is a spider with phase = 0.
  - Has exactly two connections.
- **Action**:
  - Connect the two neighbors directly.
  - Remove the spider node.

### `apply_hadamard_color_change(diagram, hadamard_id, spider_id)`
- **Purpose**: Remove a Hadamard and flip the color of the spider it’s connected to.
- **Checks**:
  - One node must be a Hadamard and the other a spider.
  - They must be connected.
- **Action**:
  - Flip spider type (`Z` ↔ `X`).
  - Redirect any additional Hadamard connections to the spider.
  - Remove the Hadamard node.

---

## 🕹 QuantumGame Class

### `__init__(self)`
- Initializes the main game state:
  - Instantiates a new `ZXDiagram`.
  - Sets `max_moves` (default: 10).
  - Calls `setup_initial_diagram()` to define the game puzzle.

### `setup_initial_diagram(self)`
- Creates a simple puzzle to be solved.
- Example: A diagram representing `WIRE_END -- Z(0) -- WIRE_END`, reducible with the Identity Rule.

### `get_available_rules(self)`
- Returns a dictionary of rule IDs and their descriptions to guide user input.

### `check_win_condition(self)`
- **Win Check**:
  - Diagram contains only **two WIRE_END nodes**.
  - They are directly connected (no intermediate nodes).

### `run(self)`
- Main interactive game loop:
  1. Display diagram and rules.
  2. Prompt user for a rule and relevant node IDs.
  3. Validate and apply the rule.
  4. Track move count.
  5. Continue until win condition or move limit is reached.

- **Game Outcome**:
  - If simplified correctly: 🎉 Success message!
  - If moves run out: ❌ Failure message with retry option.

---

## 🚀 Summary

This modular design allows the ZX-calculus tutorial to be:
- Intuitive (through visual diagrams and step-by-step rules)
- Educational (demonstrating algebraic properties of quantum systems)
- Interactive (through a puzzle-solving game loop)

Whether you're a beginner or brushing up on ZX-calculus, this game offers an engaging and practical learning tool.

---

> Created as part of the **ZX-Simplifier Game**: A playful approach to mastering the ZX-calculus.
