"""
cluck_and_crow.py
==================
MAIN GAME FILE. Run this one:  python cluck_and_crow.py

CLUCK & CROW: THE QUANTUM COOP
-------------------------------
A reimagining of the original "MILQ Simulator" hackathon game (hens vs.
quantum crows instead of chocolate vs. strawberry milk cows), modernized to
run on current Qiskit (Aer simulator, no deprecated APIs) and built as a
guided quantum-computing tutorial: every time the Quantum Crow Hive "thinks,"
the game pauses and walks you through what the quantum circuit is actually
doing, concept by concept.

STORY
-----
Two coops, one field. You raise Hens; a Quantum Hive Mind raises Crows.
Each round has three phases:
  1. FLAP phase: you move one of your birds across the fence to the other
     coop, then the Quantum Hive moves one of its birds.
  2. BREED phase: two random birds on each side pair up and produce a
     chick, whose feather-genes are a mix of its parents'.
  3. MOLT (death) phase: one older bird from each side leaves the flock,
     weighted by age (older birds are more likely to retire).
Whichever species (Hen or Crow) eventually claims every bird on the field
wins.

THE QUANTUM TWIST
------------------
The Crow side doesn't move randomly or follow simple heuristics. Every Crow
turn, the game builds a brand new quantum circuit (see quantum_ai.py) that
encodes the *entire current flock arrangement* as a Max-Cut graph problem,
runs it on Qiskit's Aer simulator using a small quantum-annealing-style
routine, and only then decides which Crow to move. In FULL TUTORIAL MODE
(the default), the game pauses at each stage of circuit-building and shows
you, in plain language, what just happened physically inside the circuit.

CONTROLS
--------
  - Click a bird you control, then click it again to send it across the fence.
  - SPACE: advance the tutorial popup / continue.
  - G: toggle the live Max-Cut graph visualization panel.
  - T: toggle Full Tutorial Mode on/off mid-game.
  - ESC or window close: quit.

DEPENDENCIES
------------
    pip install qiskit qiskit-aer pygame networkx numpy matplotlib

(matplotlib is only used to render the optional graph-visualization panel.)
"""

import sys
import time
from random import sample, choice

import pygame
import networkx as nx
import matplotlib
matplotlib.use("Agg")  # render to an image buffer, not a separate window
import matplotlib.pyplot as plt

from bird import Bird
from quantum_ai import QuantumFlockMind

# ---------------------------------------------------------------------------
# Visual constants
# ---------------------------------------------------------------------------

SCREEN_WIDTH = 760
SCREEN_HEIGHT = 760
GRAPH_PANEL_WIDTH = 420
TICK_RATE = 60

HEN_COLOR = (235, 200, 110)        # warm gold
CROW_COLOR = (70, 60, 95)          # deep indigo
FONT_COLOR = (245, 245, 245)
PANEL_BG = (28, 30, 42)
COOP_BG = (90, 130, 80)
FENCE_COLOR = (120, 90, 60)
TUTORIAL_BG = (20, 22, 30)
TUTORIAL_BORDER = (235, 200, 110)
BUTTON_BG = (60, 65, 90)
BUTTON_HOVER = (90, 95, 130)

BIRD_RADIUS = 34


def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# ---------------------------------------------------------------------------
# Tutorial content: one short lesson per quantum-concept moment
# ---------------------------------------------------------------------------

TUTORIAL_TEXT = {
    "intro": (
        "WELCOME TO CLUCK & CROW",
        [
            "Every time it's the Crows' turn, a real quantum circuit decides",
            "their move. We'll pause at each step so you can see exactly",
            "what's happening inside the circuit -- no physics degree needed.",
            "",
            "Press SPACE to begin.",
        ],
    ),
    "encoding": (
        "STEP 1: ENCODING THE PROBLEM",
        [
            "The flock's arrangement gets turned into logic statements:",
            "'these birds share a feather gene, so the Hive prefers they",
            "stay grouped.' This is how real-world puzzles (scheduling,",
            "routing, chip design) get translated into something a quantum",
            "computer can actually work with: boolean satisfiability.",
        ],
    ),
    "reduction": (
        "STEP 2: PROBLEM REDUCTION",
        [
            "Those logic statements get rewritten as a graph-cutting puzzle",
            "called Max-Cut: split the graph's nodes into two groups so the",
            "heaviest possible set of connections gets 'cut' between them.",
            "Many hard problems are secretly Max-Cut in disguise -- this",
            "reduction is a core technique in computer science.",
        ],
    ),
    "superposition": (
        "STEP 3: SUPERPOSITION",
        [
            "Each possible Max-Cut split becomes one qubit. A Hadamard gate",
            "puts every qubit into an equal blend of 0 and 1 at once.",
            "With N qubits, the circuit now represents ALL 2^N possible",
            "flock arrangements simultaneously -- not one guess at a time.",
        ],
    ),
    "entanglement": (
        "STEP 4: ENTANGLEMENT & PHASE",
        [
            "An RZZ gate links two qubits whenever their birds are",
            "connected in the graph. This doesn't just correlate their",
            "values -- it links their quantum PHASE, which is what lets",
            "the next step (interference) actually sort good splits from",
            "bad ones.",
        ],
    ),
    "annealing": (
        "STEP 5: QUANTUM ANNEALING & INTERFERENCE",
        [
            "Over several tiny time-steps, the circuit slides smoothly from",
            "'explore everything' (mixing gates) toward 'lock in the cheapest",
            "cut' (cost gates). Good splits reinforce each other",
            "(constructive interference); bad splits cancel out",
            "(destructive interference) -- the same trick behind Grover's",
            "search algorithm.",
        ],
    ),
    "measurement": (
        "STEP 6: MEASUREMENT & COLLAPSE",
        [
            "Right now the circuit holds many candidate answers at once.",
            "Measuring forces it to collapse into ONE definite classical",
            "bitstring. The best splits aren't guaranteed -- they're just",
            "exponentially more LIKELY to be the one you see. We run it",
            "2000 times and take the most common result.",
        ],
    ),
    "decision": (
        "THE HIVE DECIDES",
        [
            "The Crow Hive now knows its ideal flock arrangement. It checks",
            "every Crow it's allowed to move and picks whichever single move",
            "gets the flock closest to that ideal -- nudging the whole game",
            "toward equilibrium, one legal step at a time.",
        ],
    ),
}

TUTORIAL_SEQUENCE = ["encoding", "reduction", "superposition", "entanglement", "annealing", "measurement", "decision"]


class TutorialPopup:
    """A simple modal box that blocks input until SPACE is pressed."""

    def __init__(self, font_title, font_body):
        self.font_title = font_title
        self.font_body = font_body
        self.active_key = None
        self.queue = []

    def queue_sequence(self, keys):
        self.queue = list(keys)
        self._advance()

    def show(self, key):
        self.active_key = key

    def _advance(self):
        self.active_key = self.queue.pop(0) if self.queue else None

    @property
    def is_active(self):
        return self.active_key is not None

    def handle_continue(self):
        if self.queue:
            self._advance()
        else:
            self.active_key = None

    def draw(self, surface):
        if not self.active_key:
            return
        title, lines = TUTORIAL_TEXT[self.active_key]
        box_w, box_h = SCREEN_WIDTH - 80, 230
        box_x, box_y = 40, SCREEN_HEIGHT - box_h - 40
        pygame.draw.rect(surface, TUTORIAL_BG, (box_x, box_y, box_w, box_h), border_radius=12)
        pygame.draw.rect(surface, TUTORIAL_BORDER, (box_x, box_y, box_w, box_h), width=3, border_radius=12)

        title_surf = self.font_title.render(title, True, TUTORIAL_BORDER)
        surface.blit(title_surf, (box_x + 24, box_y + 18))

        for i, line in enumerate(lines):
            line_surf = self.font_body.render(line, True, FONT_COLOR)
            surface.blit(line_surf, (box_x + 24, box_y + 60 + i * 26))

        hint = self.font_body.render("[ SPACE to continue ]", True, (180, 180, 190))
        surface.blit(hint, (box_x + box_w - 230, box_y + box_h - 32))


# ---------------------------------------------------------------------------
# Entity: visual wrapper around a Bird
# ---------------------------------------------------------------------------

class BirdSprite:
    def __init__(self, bird: Bird, pos=(0, 0)):
        self.bird = bird
        self.pos = list(pos)
        self.target = list(pos)

    def set_target(self, pos):
        self.target = list(pos)

    def step_towards_target(self, speed=18):
        dx = self.target[0] - self.pos[0]
        dy = self.target[1] - self.pos[1]
        d = (dx ** 2 + dy ** 2) ** 0.5
        if d < speed:
            self.pos = list(self.target)
            return True
        self.pos[0] += dx / d * speed
        self.pos[1] += dy / d * speed
        return False

    def draw(self, surface, font, selected=False):
        color = HEN_COLOR if self.bird.species else CROW_COLOR
        pygame.draw.circle(surface, color, self.pos, BIRD_RADIUS)
        ring_color = (255, 255, 255) if selected else (20, 20, 20)
        pygame.draw.circle(surface, ring_color, self.pos, BIRD_RADIUS, 3)

        gene_text = "".join("H" if v else ("C" if v is False else "_") for v in self.bird.genes.values())
        label = font.render(gene_text, True, (15, 15, 15))
        rect = label.get_rect(center=(self.pos[0], self.pos[1] + BIRD_RADIUS + 14))
        pygame.draw.rect(surface, FONT_COLOR, rect.inflate(8, 4))
        surface.blit(label, rect)


# ---------------------------------------------------------------------------
# Layout helper: arrange sprites into two coop rows
# ---------------------------------------------------------------------------

def layout_positions(sprites, field_width, field_height, row_capacity=5):
    hen_sprites = [s for s in sprites if s.bird.side is True]
    crow_sprites = [s for s in sprites if s.bird.side is False]

    def rows_for(n):
        rows, remaining = [], n
        while remaining > 0:
            rows.append(min(row_capacity, remaining))
            remaining -= row_capacity
        return rows or [0]

    margin_y = field_height * 0.22
    for group, y_start, y_dir in ((crow_sprites, margin_y, 1), (hen_sprites, field_height - margin_y, -1)):
        rows = rows_for(len(group))
        idx = 0
        for r, count in enumerate(rows):
            y = y_start + y_dir * r * 90
            for c in range(count):
                x = field_width / (count + 1) * (c + 1)
                group[idx].set_target((x, y))
                idx += 1


# ---------------------------------------------------------------------------
# Graph visualization (rendered to an image, blitted onto the panel)
# ---------------------------------------------------------------------------

def render_graph_image(graph, highlight_bits=None, node_index=None, size_px=(GRAPH_PANEL_WIDTH - 20, 360)):
    fig = plt.figure(figsize=(size_px[0] / 100, size_px[1] / 100), dpi=100)
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(graph, seed=7)

    colors = []
    valid_highlight = (
        highlight_bits is not None
        and node_index is not None
        and len(highlight_bits) == len(node_index)
    )
    if valid_highlight:
        for node in graph.nodes:
            colors.append("#e8c86e" if highlight_bits[node_index[node]] else "#46405f")
    else:
        colors = ["#7a7a90"] * len(graph.nodes)

    nx.draw_networkx(graph, pos=pos, ax=ax, node_color=colors, node_size=180,
                      font_size=5, with_labels=False, edge_color="#55555f", width=0.6)
    ax.set_facecolor("#1c1e2a")
    fig.patch.set_facecolor("#1c1e2a")
    ax.axis("off")
    fig.tight_layout(pad=0.2)

    canvas = fig.canvas
    canvas.draw()
    raw = canvas.buffer_rgba()
    img = pygame.image.frombuffer(raw, canvas.get_width_height(), "RGBA")
    plt.close(fig)
    return img


# ---------------------------------------------------------------------------
# Game Manager
# ---------------------------------------------------------------------------

class GameManager:
    def __init__(self, screen, full_tutorial=True):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.full_tutorial = full_tutorial

        self.font_small = pygame.font.SysFont("consolas", 16)
        self.font_med = pygame.font.SysFont("consolas", 20)
        self.font_title = pygame.font.SysFont("consolas", 24, bold=True)

        self.sprites = []
        self.show_graph = True
        self.current_graph = None
        self.current_node_index = None
        self.current_bits = None

        self.popup = TutorialPopup(self.font_title, self.font_med)
        self.phase_message = "Your move: click a bird, then click it again to send it across the fence."
        self.player_turn = True
        self.selected = None
        self.move_counter = 0
        self.game_over = False

    # --- setup -------------------------------------------------------
    def add_bird(self, species, genes=(None, None, None)):
        bird = Bird(species, *genes)
        sprite = BirdSprite(bird, pos=(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.5))
        self.sprites.append(sprite)

    def field_width(self):
        return SCREEN_WIDTH - (GRAPH_PANEL_WIDTH if self.show_graph else 0)

    def relayout(self, animate=True):
        layout_positions(self.sprites, self.field_width(), SCREEN_HEIGHT)
        if not animate:
            for s in self.sprites:
                s.pos = list(s.target)

    # --- drawing -------------------------------------------------------
    def draw(self):
        self.screen.fill(COOP_BG)
        fw = self.field_width()
        pygame.draw.rect(self.screen, FENCE_COLOR, (0, SCREEN_HEIGHT // 2 - 5, fw, 10))

        for sprite in self.sprites:
            sprite.draw(self.screen, self.font_small, selected=(sprite is self.selected))

        msg_surf = self.font_med.render(self.phase_message, True, FONT_COLOR)
        self.screen.blit(msg_surf, (16, 12))

        hint = self.font_small.render("[G] graph  [T] tutorial:%s  [ESC] quit" %
                                       ("ON" if self.full_tutorial else "off"), True, (230, 230, 230))
        self.screen.blit(hint, (16, SCREEN_HEIGHT - 28))

        if self.show_graph:
            self.draw_graph_panel(fw)

        self.popup.draw(self.screen)
        pygame.display.flip()

    def draw_graph_panel(self, fw):
        panel_rect = (fw, 0, GRAPH_PANEL_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)
        title = self.font_med.render("Max-Cut Graph (live)", True, FONT_COLOR)
        self.screen.blit(title, (fw + 14, 12))

        if self.current_graph is not None and len(self.current_graph.nodes) > 0:
            img = render_graph_image(self.current_graph, self.current_bits, self.current_node_index)
            self.screen.blit(img, (fw + 10, 48))
        else:
            placeholder = self.font_small.render("(graph appears after the Crows' first turn)", True, (170, 170, 180))
            self.screen.blit(placeholder, (fw + 14, 60))

    # --- animation helper -----------------------------------------------
    def animate_until_settled(self):
        settled = False
        while not settled:
            settled = True
            for s in self.sprites:
                if s.pos != s.target:
                    if not s.step_towards_target():
                        settled = False
            self.draw()
            self.clock.tick(TICK_RATE)

    # --- game phases -------------------------------------------------------
    def breed_phase(self):
        self.phase_message = "Breeding phase: two birds on each side are pairing up..."
        self.draw()
        time.sleep(0.6)

        for species in (True, False):
            group = [s for s in self.sprites if s.bird.species == species]
            if len(group) >= 2:
                parents = sample(group, 2)
                chick_bird = parents[0].bird.breed(parents[1].bird)
                chick_sprite = BirdSprite(chick_bird, pos=parents[0].pos)
                self.sprites.append(chick_sprite)
        self.relayout()
        self.animate_until_settled()

    def molt_phase(self):
        self.phase_message = "Molt phase: the oldest birds on each side may retire from the flock..."
        self.draw()
        time.sleep(0.6)

        for species in (True, False):
            group = [s for s in self.sprites if s.bird.species == species]
            weighted = []
            for s in group:
                weighted.extend([s] * max(s.bird.age, 1))
            if weighted:
                victim = choice(weighted)
                self.sprites.remove(victim)
        self.relayout()
        self.animate_until_settled()

    def age_all(self):
        for s in self.sprites:
            s.bird.age += 1

    def check_winner(self):
        species_set = {s.bird.species for s in self.sprites}
        if len(species_set) == 1:
            return species_set.pop()
        return None

    # --- player input -------------------------------------------------------
    def handle_click(self, pos):
        if self.popup.is_active or not self.player_turn:
            return
        for sprite in self.sprites:
            if dist(sprite.pos, pos) < BIRD_RADIUS + 6:
                if sprite.bird.species is not True:
                    return  # can only control your own Hens
                if self.selected is sprite:
                    sprite.bird.move()
                    self.relayout()
                    self.animate_until_settled()
                    self.selected = None
                    self.player_turn = False
                    self.take_full_turn()
                    return
                self.selected = sprite
                return

    def take_full_turn(self):
        """Called right after the player moves: runs the Crows' quantum
        turn, advances the move counter, and handles breed/molt phases
        and win-checking on every second move (mirroring the original
        game's pacing)."""
        self.run_quantum_turn()
        self.player_turn = True
        self.move_counter += 1

        if self.move_counter % 2 == 0:
            self.age_all()
            self.breed_phase()
            self.molt_phase()

            winner = self.check_winner()
            if winner is not None:
                self.phase_message = "You win! All birds are Hens." if winner else "The Crows have taken the farm..."
                self.draw()
                time.sleep(4)
                self.game_over = True

    # --- the quantum AI turn, fully narrated -------------------------------------------------------
    def run_quantum_turn(self):
        crow_birds = [s.bird for s in self.sprites if s.bird.species is False]
        all_birds = [s.bird for s in self.sprites]

        if self.full_tutorial:
            self.popup.queue_sequence(TUTORIAL_SEQUENCE)
            self.wait_for_popup_clear()

        self.phase_message = "The Quantum Hive is thinking... (building circuit)"
        self.draw()

        mind = QuantumFlockMind(all_birds, time_steps=4)
        self.current_graph = mind.graph
        self.current_node_index = mind.node_index

        self.phase_message = "Running the circuit on Qiskit's Aer simulator..."
        self.draw()
        solution = mind.think(shots=2000)
        self.current_bits = solution

        movable = [b for b in crow_birds]
        chosen = mind.pick_best_move(movable)
        if chosen is not None:
            chosen.move()
        self.relayout()
        self.animate_until_settled()
        self.phase_message = "The Hive has moved. Your turn!"

    def wait_for_popup_clear(self):
        """Pump events until the queued tutorial popups are dismissed."""
        while self.popup.is_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.popup.handle_continue()
            self.draw()
            self.clock.tick(TICK_RATE)


# ---------------------------------------------------------------------------
# Menu screen
# ---------------------------------------------------------------------------

def run_menu(screen):
    font_title = pygame.font.SysFont("consolas", 48, bold=True)
    font_btn = pygame.font.SysFont("consolas", 24)
    clock = pygame.time.Clock()

    title_surf = font_title.render("CLUCK & CROW", True, FONT_COLOR)
    subtitle_surf = font_btn.render("The Quantum Coop", True, (230, 210, 160))

    options = [("Easy  (2 vs 2)", 2), ("Medium  (3 vs 3)", 3), ("Hard  (5 vs 5)", 5)]
    buttons = []
    for i, (label, n) in enumerate(options):
        surf = font_btn.render(label, True, FONT_COLOR)
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, 380 + i * 70))
        buttons.append((surf, rect, n))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                for surf, rect, n in buttons:
                    if rect.collidepoint(event.pos):
                        return n

        screen.fill(COOP_BG)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 180)))
        screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 235)))
        for surf, rect, n in buttons:
            pygame.draw.rect(screen, BUTTON_BG, rect.inflate(40, 24), border_radius=10)
            screen.blit(surf, rect)
        pygame.display.flip()
        clock.tick(60)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cluck & Crow: The Quantum Coop")

    flock_size = run_menu(screen)

    manager = GameManager(screen, full_tutorial=True)

    starter_genes_hen = [(True, True, True), (True, True, None), (True, None, None), (True, None, None), (True, True, None)]
    starter_genes_crow = [(False, False, False), (False, False, None), (False, None, None), (False, None, None), (False, False, None)]
    for i in range(flock_size):
        manager.add_bird(True, starter_genes_hen[i % len(starter_genes_hen)])
        manager.add_bird(False, starter_genes_crow[i % len(starter_genes_crow)])
    manager.relayout(animate=False)
    manager.age_all()

    manager.popup.queue_sequence(["intro"])
    manager.wait_for_popup_clear()

    running = True
    while running and not manager.game_over:
        manager.clock.tick(TICK_RATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_g:
                    manager.show_graph = not manager.show_graph
                    manager.relayout(animate=False)
                elif event.key == pygame.K_t:
                    manager.full_tutorial = not manager.full_tutorial
                elif event.key == pygame.K_SPACE:
                    manager.popup.handle_continue()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                manager.handle_click(event.pos)

        manager.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
