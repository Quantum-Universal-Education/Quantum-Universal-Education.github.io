import math

# --- Node Class (Same as before) ---
class Node:
    """
    Represents a node (spider, Hadamard, or wire end) in a ZX-diagram.
    Each node has a unique ID, a type, an optional phase, and a set of connections
    to other nodes.
    """
    def __init__(self, node_id, node_type, phase=0.0):
        self.id = node_id
        # node_type can be 'Z_SPIDER', 'X_SPIDER', 'HADAMARD', 'WIRE_END'
        self.type = node_type
        self.phase = phase
        self.connections = set() # Stores IDs of connected nodes

    def __repr__(self):
        """
        Provides a string representation of the node for display.
        """
        if self.type == 'Z_SPIDER':
            return f"Z({self.id}, φ={self.phase/math.pi:.2f}π)" # Represent phase in terms of pi
        elif self.type == 'X_SPIDER':
            return f"X({self.id}, φ={self.phase/math.pi:.2f}π)"
        elif self.type == 'HADAMARD':
            return f"H({self.id})"
        elif self.type == 'WIRE_END':
            return f"W({self.id})" # Represents an input/output wire end
        return f"Node({self.id}, {self.type})"

# --- ZXDiagram Class (Same as before) ---
class ZXDiagram:
    """
    Manages the overall ZX-diagram as a collection of nodes and their connections.
    Provides methods for manipulating the diagram structure.
    """
    def __init__(self):
        self.nodes = {} # Dictionary to store nodes by their ID
        self.next_node_id = 0 # Counter for assigning unique node IDs

    def add_node(self, node_type, phase=0.0):
        """
        Adds a new node to the diagram.
        """
        node = Node(self.next_node_id, node_type, phase)
        self.nodes[self.next_node_id] = node
        self.next_node_id += 1
        return node.id

    def add_connection(self, id1, id2):
        """
        Establishes a bidirectional connection between two nodes.
        """
        if id1 in self.nodes and id2 in self.nodes:
            self.nodes[id1].connections.add(id2)
            self.nodes[id2].connections.add(id1)
        else:
            raise ValueError("Error: Node IDs not found for connection.")

    def remove_node(self, node_id):
        """
        Removes a node and all its connections from the diagram.
        """
        if node_id in self.nodes:
            node_to_remove = self.nodes[node_id]
            for connected_id in list(node_to_remove.connections):
                if connected_id in self.nodes:
                    self.nodes[connected_id].connections.discard(node_id)
            del self.nodes[node_id]
        else:
            raise ValueError(f"Error: Node {node_id} not found for removal.")

    def remove_connection(self, id1, id2):
        """
        Removes a connection between two specific nodes.
        """
        if id1 in self.nodes and id2 in self.nodes:
            self.nodes[id1].connections.discard(id2)
            self.nodes[id2].connections.discard(id1)
        else:
            raise ValueError("Error: Node IDs not found for connection removal.")

    def get_neighbors(self, node_id):
        """
        Returns a list of IDs of nodes connected to a given node.
        """
        if node_id in self.nodes:
            return list(self.nodes[node_id].connections)
        return []

    def get_node(self, node_id):
        """
        Retrieves a node object by its ID.
        """
        return self.nodes.get(node_id)

    def display(self):
        """
        Prints a textual representation of the current diagram.
        """
        print("\n--- Current ZX Diagram ---")
        if not self.nodes:
            print("Diagram is empty.")
            print("--------------------------")
            return

        # Sort nodes by ID for consistent display
        sorted_node_ids = sorted(self.nodes.keys())
        for node_id in sorted_node_ids:
            node = self.nodes[node_id]
            connections_str = ", ".join(str(conn_id) for conn_id in sorted(list(node.connections)))
            print(f"{node} -> Connected to: [{connections_str}]")
        print("--------------------------")

    def simplify_phase(self, phase):
        """
        Normalizes a phase to be within [0, 2*pi).
        """
        return phase % (2 * math.pi)

# --- ZXRules Class (Same as before) ---
class ZXRules:
    """
    Implements the core ZX-calculus rewrite rules as static methods.
    """
    @staticmethod
    def apply_spider_fusion(diagram, node_id1, node_id2):
        """
        Applies the spider fusion rule: merges two adjacent spiders of the same color.
        Their phases add up.
        """
        node1 = diagram.get_node(node_id1)
        node2 = diagram.get_node(node_id2)

        if not node1 or not node2:
            print("Rule failed: One or both nodes not found.")
            return False

        if node1.type != node2.type or node1.type not in ['Z_SPIDER', 'X_SPIDER']:
            print("Rule failed: Nodes must be spiders of the same color to fuse.")
            return False

        if node2.id not in node1.connections:
            print("Rule failed: Nodes must be directly connected to fuse.")
            return False

        # Apply fusion
        node1.phase = diagram.simplify_phase(node1.phase + node2.phase)

        # Reconnect all neighbors of node2 to node1, except node1 itself
        for neighbor_id in list(node2.connections):
            if neighbor_id != node1.id:
                diagram.remove_connection(node2.id, neighbor_id)
                diagram.add_connection(node1.id, neighbor_id)
        
        diagram.remove_node(node2.id)
        print(f"Rule applied: Fused {node2.type} spider {node2.id} into {node1.type} spider {node1.id}. New phase: {node1.phase / math.pi:.2f}π")
        return True

    @staticmethod
    def apply_identity_rule(diagram, node_id):
        """
        Applies the identity rule: removes a 0-phase spider with exactly two connections.
        """
        node = diagram.get_node(node_id)

        if not node:
            print("Rule failed: Node not found.")
            return False

        if node.type not in ['Z_SPIDER', 'X_SPIDER']:
            print("Rule failed: Node must be a spider.")
            return False

        # Phase must be effectively zero (allowing for floating point inaccuracies)
        if abs(diagram.simplify_phase(node.phase)) > 1e-9 and abs(diagram.simplify_phase(node.phase) - 2 * math.pi) > 1e-9:
             print(f"Rule failed: Spider {node_id} must have a phase of 0 (or 2π). Current phase: {node.phase / math.pi:.2f}π")
             return False

        if len(node.connections) != 2:
            print("Rule failed: Identity rule applies to spiders with exactly 2 connections.")
            return False

        # Get the two neighbors
        neighbors = list(node.connections)
        neighbor1_id, neighbor2_id = neighbors[0], neighbors[1]

        # Reconnect neighbors directly
        diagram.remove_connection(node_id, neighbor1_id)
        diagram.remove_connection(node_id, neighbor2_id)
        diagram.add_connection(neighbor1_id, neighbor2_id)

        diagram.remove_node(node_id)
        print(f"Rule applied: Applied identity rule. Removed spider {node_id}.")
        return True

    @staticmethod
    def apply_hadamard_color_change(diagram, hadamard_id, spider_id):
        """
        Applies the Hadamard color change rule: A Hadamard gate connected to a spider
        changes the spider's color and is removed from the diagram.
        """
        hadamard_node = diagram.get_node(hadamard_id)
        spider_node = diagram.get_node(spider_id)

        if not hadamard_node or not spider_node:
            print("Rule failed: Hadamard or spider node not found.")
            return False

        if hadamard_node.type != 'HADAMARD' or spider_node.type not in ['Z_SPIDER', 'X_SPIDER']:
            print("Rule failed: First node must be a Hadamard, second must be a spider.")
            return False

        if spider_node.id not in hadamard_node.connections:
            print("Rule failed: Hadamard and spider must be directly connected.")
            return False
        
        # Apply Hadamard color change
        if spider_node.type == 'Z_SPIDER':
            spider_node.type = 'X_SPIDER'
            print(f"Rule applied: Hadamard {hadamard_id} changed Z-spider {spider_id} to X-spider.")
        else: # X_SPIDER
            spider_node.type = 'Z_SPIDER'
            print(f"Rule applied: Hadamard {hadamard_id} changed X-spider {spider_id} to Z-spider.")
        
        # Reconnect the Hadamard's other side to the spider, then remove the Hadamard node
        h_neighbors = list(hadamard_node.connections)
        if len(h_neighbors) == 2: # Typical Hadamard with two connections
            other_h_neighbor_id = [n_id for n_id in h_neighbors if n_id != spider_id][0]
            diagram.remove_connection(hadamard_id, spider_id)
            diagram.remove_connection(hadamard_id, other_h_neighbor_id)
            diagram.add_connection(spider_id, other_h_neighbor_id)
        elif len(h_neighbors) == 1 and h_neighbors[0] == spider_id:
            # Hadamard is only connected to the spider, meaning it's an end gate.
            diagram.remove_connection(hadamard_id, spider_id)
        else:
            print("Rule failed: Hadamard must have 1 or 2 connections for this simplified rule.")
            return False

        diagram.remove_node(hadamard_id)
        return True

# --- QuantumGame Class (Modified) ---
class QuantumGame:
    """
    Manages the game flow, user interaction, levels, and scoring.
    """
    def __init__(self):
        self.total_score = 0
        # Define levels with their specific setup functions, win conditions, and scoring parameters
        self.levels = [
            {
                "name": "Level 1: The Simple Identity",
                "setup_func": self._setup_level1,
                "win_condition_func": self._check_standard_win,
                "optimal_moves": 1,
                "base_score": 100,
                "bonus_score": 50,
                "penalty_per_move": 10,
                "max_moves": 3 # Max moves allowed for this level
            },
            {
                "name": "Level 2: Fusing Spiders",
                "setup_func": self._setup_level2,
                "win_condition_func": self._check_standard_win,
                "optimal_moves": 2,
                "base_score": 150,
                "bonus_score": 75,
                "penalty_per_move": 15,
                "max_moves": 5
            },
            {
                "name": "Level 3: Hadamard Challenges",
                "setup_func": self._setup_level3,
                "win_condition_func": self._check_standard_win,
                "optimal_moves": 4,
                "base_score": 200,
                "bonus_score": 100,
                "penalty_per_move": 20,
                "max_moves": 8
            }
        ]
        self.diagram = ZXDiagram() # Initialize diagram object (will be reset for each level)

    # --- Level Setup Functions ---
    def _setup_level1(self):
        """
        Sets up the initial ZX-diagram for Level 1.
        Diagram: Input -- Z(0) -- Output
        Optimal moves: 1 (Identity Rule)
        """
        self.diagram = ZXDiagram() # Reset diagram for the new level
        self.node_w_in = self.diagram.add_node('WIRE_END')
        self.node_z = self.diagram.add_node('Z_SPIDER', 0.0)
        self.node_w_out = self.diagram.add_node('WIRE_END')
        self.diagram.add_connection(self.node_w_in, self.node_z)
        self.diagram.add_connection(self.node_z, self.node_w_out)
        print("Initial Diagram Setup for Level 1:")
        self.diagram.display()
        print("Your goal is to simplify this diagram to just an input and output wire directly connected.")

    def _setup_level2(self):
        """
        Sets up the initial ZX-diagram for Level 2.
        Diagram: Input -- Z(π) -- Z(π) -- Output
        Optimal moves: 2 (Spider Fusion, then Identity Rule)
        """
        self.diagram = ZXDiagram() # Reset diagram for the new level
        self.node_w_in = self.diagram.add_node('WIRE_END')
        self.node_z1 = self.diagram.add_node('Z_SPIDER', math.pi) # Z-spider with phase pi
        self.node_z2 = self.diagram.add_node('Z_SPIDER', math.pi) # Another Z-spider with phase pi
        self.node_w_out = self.diagram.add_node('WIRE_END')
        
        self.diagram.add_connection(self.node_w_in, self.node_z1)
        self.diagram.add_connection(self.node_z1, self.node_z2)
        self.diagram.add_connection(self.node_z2, self.node_w_out)
        
        print("Initial Diagram Setup for Level 2:")
        self.diagram.display()
        print("Your goal is to simplify this diagram to just an input and output wire directly connected.")

    def _setup_level3(self):
        """
        Sets up the initial ZX-diagram for Level 3.
        Diagram: Input -- Z(0) -- H -- X(0) -- H -- Output
        Optimal moves: 4 (Hadamard Color Change, Spider Fusion, Hadamard Color Change, Identity Rule)
        """
        self.diagram = ZXDiagram() # Reset diagram for the new level
        self.node_w_in = self.diagram.add_node('WIRE_END')
        self.node_z1 = self.diagram.add_node('Z_SPIDER', 0.0)
        self.node_h2 = self.diagram.add_node('HADAMARD')
        self.node_x3 = self.diagram.add_node('X_SPIDER', 0.0)
        self.node_h4 = self.diagram.add_node('HADAMARD')
        self.node_w_out = self.diagram.add_node('WIRE_END')
        
        self.diagram.add_connection(self.node_w_in, self.node_z1)
        self.diagram.add_connection(self.node_z1, self.node_h2)
        self.diagram.add_connection(self.node_h2, self.node_x3)
        self.diagram.add_connection(self.node_x3, self.node_h4)
        self.diagram.add_connection(self.node_h4, self.node_w_out)
        
        print("Initial Diagram Setup for Level 3:")
        self.diagram.display()
        print("Your goal is to simplify this diagram to just an input and output wire directly connected.")

    # --- Win Condition Check ---
    def _check_standard_win(self):
        """
        Checks if the diagram has been simplified to a single wire.
        This win condition applies to all levels in this game.
        """
        # Win condition: Exactly two nodes remaining, both are WIRE_END, and they are directly connected.
        if len(self.diagram.nodes) == 2:
            nodes = list(self.diagram.nodes.values())
            # Ensure both remaining nodes are wire ends
            if nodes[0].type == 'WIRE_END' and nodes[1].type == 'WIRE_END':
                # Ensure they are connected to each other
                if nodes[0].id in nodes[1].connections:
                    return True
        return False

    def get_available_rules(self):
        """
        Lists the rules available to the player.
        """
        rules = {
            1: "Spider Fusion (Merge same-color adjacent spiders) - requires 2 spider IDs.",
            2: "Identity Rule (Remove 0-phase, 2-connected spider) - requires 1 spider ID.",
            3: "Hadamard Color Change (Apply Hadamard to a spider, removing H node) - requires 1 Hadamard ID and 1 spider ID."
        }
        return rules

    def play_level(self, level_info):
        """
        Runs a single level of the game.
        """
        level_name = level_info["name"]
        level_setup_func = level_info["setup_func"]
        level_win_condition_func = level_info["win_condition_func"]
        optimal_moves = level_info["optimal_moves"]
        base_score = level_info["base_score"]
        bonus_score = level_info["bonus_score"]
        penalty_per_move = level_info["penalty_per_move"]
        max_moves = level_info["max_moves"]

        print(f"\n--- Starting {level_name} ---")
        level_setup_func() # Set up the diagram for the current level
        self.current_move = 0 # Reset move count for the level
        level_won = False

        while self.current_move < max_moves:
            self.diagram.display() # Show current state of the diagram
            if level_win_condition_func(): # Check if win condition is met
                level_won = True
                break

            print(f"\n--- Move {self.current_move + 1}/{max_moves} for {level_name} ---")
            print("Available Rules:")
            rules = self.get_available_rules()
            for key, desc in rules.items():
                print(f"  {key}: {desc}")

            try:
                rule_choice = int(input("Choose a rule to apply (number): "))
                if rule_choice not in rules:
                    print("Invalid rule choice. Please select from the numbers provided.")
                    continue

                rule_applied_successfully = False
                if rule_choice == 1: # Spider Fusion
                    id1 = int(input("Enter ID of first spider to fuse: "))
                    id2 = int(input("Enter ID of second spider to fuse (must be adjacent and same color): "))
                    rule_applied_successfully = ZXRules.apply_spider_fusion(self.diagram, id1, id2)
                elif rule_choice == 2: # Identity Rule
                    node_id = int(input("Enter ID of spider to apply identity rule to (0-phase, 2 connections): "))
                    rule_applied_successfully = ZXRules.apply_identity_rule(self.diagram, node_id)
                elif rule_choice == 3: # Hadamard Color Change
                    h_id = int(input("Enter ID of Hadamard node: "))
                    spider_id = int(input("Enter ID of spider connected to Hadamard: "))
                    rule_applied_successfully = ZXRules.apply_hadamard_color_change(self.diagram, h_id, spider_id)
                else:
                    print("Rule not implemented or invalid for this game version. Try again.")

                if rule_applied_successfully:
                    self.current_move += 1 # Only increment move if rule was successfully applied

            except ValueError:
                print("Invalid input. Please enter numbers for IDs and choices.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please check your inputs and try again.")

        # Calculate and display score for the level
        level_score = 0
        if level_won:
            print(f"\n⭐⭐⭐ You successfully completed {level_name}! ⭐⭐⭐")
            level_score = base_score
            if self.current_move <= optimal_moves:
                level_score += bonus_score
                print(f"Bonus! Completed in optimal {optimal_moves} moves.")
            else:
                extra_moves = self.current_move - optimal_moves
                level_score -= (extra_moves * penalty_per_move)
                # Ensure score doesn't go below zero for the level
                level_score = max(0, level_score) 
                print(f"Took {extra_moves} extra moves. Penalty applied.")
            print(f"Score for {level_name}: {level_score}")
        else:
            print(f"\nTime's up for {level_name}! You ran out of moves without completing the diagram.")
            self.diagram.display()
            print("Keep practicing!")

        self.total_score += level_score # Add level score to total
        print(f"Current Total Score: {self.total_score}")
        return level_won # Return whether the level was won for game flow control

    def start_game(self):
        """
        Starts the main game, playing through all defined levels.
        """
        print("Welcome to ZX-Simplifier: A Quantum Diagram Game!")
        print("Your goal is to simplify each given ZX-diagram using rewrite rules to a single wire.")
        print("Good luck!")

        for i, level_info in enumerate(self.levels):
            if not self.play_level(level_info):
                print("\nGame Over! You failed to complete a level.")
                break # End game if a level is failed

            if i < len(self.levels) - 1:
                input("\nPress Enter to proceed to the next level...")
            else:
                print("\nCongratulations! You have completed all levels and mastered the basics of ZX-calculus!")
        
        print(f"\n--- Game Finished ---")
        print(f"Your Final Score: {self.total_score}")
        print("Thanks for playing ZX-Simplifier!")

# Main execution block
if __name__ == "__main__":
    game = QuantumGame()
    game.start_game()
