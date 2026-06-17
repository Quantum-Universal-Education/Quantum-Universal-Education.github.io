"""
cluck_and_crow.py
==================
MAIN GAME FILE. Run this one:  python cluck_and_crow.py

CLUCK & CROW: THE QUANTUM COOP
-------------------------------
A  to
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
  2. BREED phase: two birds sharing a coop pair up and produce a chick,
     whose feather-genes are a mix of its parents'. On any coop side with
     2+ of YOUR birds, you choose the breeding pair yourself (or skip with
     SPACE to let it be random); the Crow Hive's own side always breeds
     randomly.
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
  - During Breed phase: click two of your birds sharing a coop to choose
    them as breeding parents, or press SPACE to let that pairing be random.
  - SPACE: advance the tutorial overlay immediately / dismiss the intro screen.
  - G: toggle the live Max-Cut graph visualization panel.
  - T: toggle Full Tutorial Mode on/off mid-game.
  - +/-: increase/decrease the Hive's annealing steps (its "intelligence dial")
         live, mid-game -- watch the probability chart sharpen or flatten.
  - ESC or window close: quit.

DEPENDENCIES
------------
    pip install qiskit qiskit-aer pygame networkx numpy matplotlib

(matplotlib is only used to render the optional graph-visualization panel.)
"""

import sys
import time
import math
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


class TutorialOverlay:
    """
    A non-blocking tutorial panel docked in a corner of the screen.

    Unlike a modal popup, this does NOT halt the game loop: the graph
    panel keeps updating, entanglement-pulse animations keep playing, and
    the Hive's "thinking" process keeps visibly progressing underneath
    while the explanation text sits in the corner. This creates a much
    tighter link between "what the text says" and "what's happening on
    screen right now" -- you read about entanglement while watching the
    qubits that just got entangled visibly pulse on the graph.

    The ONE exception is the very first "intro" screen, which still blocks
    (there's nothing to show yet, so there's no value in non-blocking it,
    and it doubles as a "press SPACE to begin" gate).
    """

    CORNER_WIDTH = 360
    CORNER_HEIGHT = 250

    def __init__(self, font_title, font_body):
        self.font_title = font_title
        self.font_body = font_body
        self.active_key = None
        self.queue = []
        self.blocking = False
        self.auto_advance_timer = 0.0
        self.auto_advance_seconds = 3.2  # how long each step lingers before auto-advancing

    def queue_sequence(self, keys, blocking=False):
        self.queue = list(keys)
        self.blocking = blocking
        self.auto_advance_timer = 0.0
        self._advance()

    def _advance(self):
        self.active_key = self.queue.pop(0) if self.queue else None
        self.auto_advance_timer = 0.0

    @property
    def is_active(self):
        return self.active_key is not None

    def handle_continue(self):
        if self.queue:
            self._advance()
        else:
            self.active_key = None

    def tick(self, dt_seconds):
        """Call once per frame with elapsed time. In non-blocking mode the
        overlay auto-advances after a few seconds so the player isn't
        forced to keep pressing SPACE while the Hive is mid-turn; SPACE
        still works to skip ahead immediately."""
        if not self.is_active or self.blocking:
            return
        self.auto_advance_timer += dt_seconds
        if self.auto_advance_timer >= self.auto_advance_seconds:
            self.handle_continue()

    def draw(self, surface):
        if not self.active_key:
            return
        title, lines = TUTORIAL_TEXT[self.active_key]
        if self.blocking:
            self._draw_modal(surface, title, lines)
        else:
            self._draw_corner(surface, title, lines)

    def _draw_modal(self, surface, title, lines):
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

    def _draw_corner(self, surface, title, lines):
        box_w, box_h = self.CORNER_WIDTH, self.CORNER_HEIGHT
        box_x, box_y = 16, SCREEN_HEIGHT - box_h - 16
        pygame.draw.rect(surface, TUTORIAL_BG, (box_x, box_y, box_w, box_h), border_radius=10)
        pygame.draw.rect(surface, TUTORIAL_BORDER, (box_x, box_y, box_w, box_h), width=2, border_radius=10)

        title_surf = self.font_body.render(title, True, TUTORIAL_BORDER)
        surface.blit(title_surf, (box_x + 16, box_y + 12))

        for i, line in enumerate(lines):
            line_surf = self.font_small_for_corner(line)
            surface.blit(line_surf, (box_x + 16, box_y + 42 + i * 20))

        # progress dots + skip hint
        hint = self.font_small_for_corner("[SPACE] next   (auto-advances)")
        surface.blit(hint, (box_x + 16, box_y + box_h - 22))

    def font_small_for_corner(self, text):
        # Slightly smaller body font keeps the corner box compact; reuse
        # font_body but callers pass already-short lines so default size
        # is fine in practice. Kept as a seam in case a smaller font is
        # wanted later.
        return self.font_body.render(text, True, FONT_COLOR)


# Backwards-compatible alias: earlier versions of this file called this
# class TutorialPopup. Keep the name importable in case anything external
# references it.
TutorialPopup = TutorialOverlay


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

def render_graph_image(graph, highlight_bits=None, node_index=None, pulse_edges=None,
                        pulse_phase=0.0, size_px=(GRAPH_PANEL_WIDTH - 20, 360)):
    """
    Renders the Max-Cut graph. If pulse_edges is given (a list of (u, v)
    edge tuples), those edges -- and the nodes at their endpoints -- are
    drawn brighter/thicker, with intensity following pulse_phase (expected
    to cycle smoothly so the caller can animate a "pulsing" glow). This is
    the visual feedback for entanglement: an RZZ gate "acting on" two
    qubits becomes a visible, glowing connection between them instead of
    an abstract gate symbol in a circuit diagram.
    """
    fig = plt.figure(figsize=(size_px[0] / 100, size_px[1] / 100), dpi=100)
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(graph, seed=7)

    colors = []
    valid_highlight = (
        highlight_bits is not None
        and node_index is not None
        and len(highlight_bits) == len(node_index)
    )
    pulsing_nodes = set()
    if pulse_edges:
        for u, v in pulse_edges:
            pulsing_nodes.add(u)
            pulsing_nodes.add(v)

    if valid_highlight:
        for node in graph.nodes:
            colors.append("#e8c86e" if highlight_bits[node_index[node]] else "#46405f")
    else:
        colors = ["#7a7a90"] * len(graph.nodes)

    # base graph first
    nx.draw_networkx(graph, pos=pos, ax=ax, node_color=colors, node_size=180,
                      font_size=5, with_labels=False, edge_color="#55555f", width=0.6)

    # pulsing entanglement overlay: brighter edges + glowing ring on their endpoints
    if pulse_edges:
        # pulse_phase in [0, 1] -> intensity oscillates via sine for a glow effect
        intensity = 0.55 + 0.45 * math.sin(pulse_phase * 2 * math.pi)
        glow_width = 1.6 + 2.2 * intensity
        nx.draw_networkx_edges(graph, pos=pos, ax=ax, edgelist=pulse_edges,
                                edge_color="#7fe8ff", width=glow_width, alpha=0.55 + 0.4 * intensity)
        if pulsing_nodes:
            ring_size = 240 + 80 * intensity
            nx.draw_networkx_nodes(graph, pos=pos, ax=ax, nodelist=list(pulsing_nodes),
                                    node_color="none", node_size=ring_size,
                                    edgecolors="#7fe8ff", linewidths=2.2)

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
    def __init__(self, screen, full_tutorial=True, time_steps=4):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.full_tutorial = full_tutorial
        self.time_steps = time_steps  # the Hive's "intelligence dial" -- see quantum_ai.QuantumFlockMind

        self.font_small = pygame.font.SysFont("consolas", 16)
        self.font_med = pygame.font.SysFont("consolas", 20)
        self.font_title = pygame.font.SysFont("consolas", 24, bold=True)

        self.sprites = []
        self.show_graph = True
        self.current_graph = None
        self.current_node_index = None
        self.current_bits = None
        self.current_top_results = None
        self.pulse_edges = []
        self.pulse_phase = 0.0

        self.popup = TutorialOverlay(self.font_title, self.font_med)
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

        hint = self.font_small.render("[G] graph  [T] tutorial:%s  [+/-] anneal steps:%d  [ESC] quit" %
                                       ("ON" if self.full_tutorial else "off", self.time_steps), True, (230, 230, 230))
        self.screen.blit(hint, (16, SCREEN_HEIGHT - 28))

        self.pulse_phase = (self.pulse_phase + 1.0 / TICK_RATE / 1.1) % 1.0

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
            img = render_graph_image(
                self.current_graph, self.current_bits, self.current_node_index,
                pulse_edges=self.pulse_edges, pulse_phase=self.pulse_phase,
            )
            self.screen.blit(img, (fw + 10, 48))
        else:
            placeholder = self.font_small.render("(graph appears after the Crows' first turn)", True, (170, 170, 180))
            self.screen.blit(placeholder, (fw + 14, 60))

        # Probability distribution bar chart: shown once we have a fresh
        # measurement result, stacked below the graph image so both are
        # visible at once -- the graph shows WHAT was measured, the bars
        # show HOW LIKELY that (and its runner-ups) were.
        if self.current_top_results:
            self.draw_probability_chart(fw, y_offset=420)

    def draw_probability_chart(self, fw, y_offset):
        """
        Concept made visible: a probability distribution, not a single
        answer. Draws a small horizontal bar chart of the top measured
        bitstrings and how often each one came up out of 2000 shots.
        """
        chart_x = fw + 14
        chart_w = GRAPH_PANEL_WIDTH - 28
        title = self.font_small.render("Top measured outcomes (2000 shots):", True, FONT_COLOR)
        self.screen.blit(title, (chart_x, y_offset))

        max_prob = max(prob for _, _, prob in self.current_top_results) or 1.0
        bar_h = 22
        for i, (bitstring, count, prob) in enumerate(self.current_top_results):
            y = y_offset + 26 + i * (bar_h + 6)
            bar_w = int((chart_w - 90) * (prob / max_prob))
            color = (232, 200, 110) if i == 0 else (90, 95, 130)
            pygame.draw.rect(self.screen, color, (chart_x, y, max(bar_w, 2), bar_h), border_radius=4)
            label = self.font_small.render(f"{prob*100:4.1f}%  ({count})", True, FONT_COLOR)
            self.screen.blit(label, (chart_x + chart_w - 86, y + 2))

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
        """
        Pair up birds that currently share a COOP SIDE (not a fixed
        species) and let them breed. This is the mechanic that makes
        player and Hive moves matter: a bird that has crossed the fence
        breeds with its new neighbors, and the chick's species follows
        the genetic majority vote of THOSE parents -- which is how a
        coop can gradually convert from Crows to Hens (or vice versa)
        over the course of the game.

        On whichever coop side currently has 2+ Hen-species birds, the
        PLAYER gets to pick which two birds breed (real tactical depth:
        you can deliberately pair two strong Hen-gened birds to try to
        "breed out" any Crow influence that's crept into that coop). Any
        side without player-controlled birds available to choose (or where
        the player skips/runs out of time) falls back to a random pairing,
        same as the Crow Hive's own side always does.
        """
        self.phase_message = "Breeding phase: choose two of your birds in the same coop to breed..."
        self.draw()

        for side in (True, False):
            group = [s for s in self.sprites if s.bird.side == side]
            if len(group) < 2:
                continue

            chosen_pair = None
            # Only offer player choice for a side that actually has at
            # least 2 player-controlled (Hen-species) birds standing on it.
            hen_controlled = [s for s in group if s.bird.species is True]
            if len(hen_controlled) >= 2:
                chosen_pair = self.prompt_breeding_choice(group, side)

            parents = chosen_pair if chosen_pair is not None else sample(group, 2)
            chick_bird = parents[0].bird.breed(parents[1].bird)
            chick_sprite = BirdSprite(chick_bird, pos=parents[0].pos)
            self.sprites.append(chick_sprite)

        self.relayout()
        self.animate_until_settled()

    def prompt_breeding_choice(self, group, side):
        """
        Lets the player click two birds (within `group`, all on the same
        coop side) to choose breeding parents. Returns the chosen pair of
        sprites, or None if the player presses SPACE to skip and let the
        game pick randomly instead. A short on-screen prompt explains
        what's happening; this does not use the tutorial overlay since
        it's a real input-gathering step, not an explanation.
        """
        coop_name = "Hen-coop" if side else "Crow-coop"
        self.phase_message = f"Click two birds in the {coop_name} to breed them (SPACE to skip / random)."
        picked = []
        self.draw()

        while len(picked) < 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for sprite in group:
                        if sprite in picked:
                            continue
                        if dist(sprite.pos, event.pos) < BIRD_RADIUS + 6:
                            picked.append(sprite)
                            break
            self.draw_breeding_prompt(picked, group)
            self.clock.tick(TICK_RATE)

        return picked

    def draw_breeding_prompt(self, picked, group):
        """Extra highlight ring around already-picked breeding candidates,
        drawn on top of the normal frame so the player can see their
        in-progress selection."""
        self.draw()
        for sprite in picked:
            pygame.draw.circle(self.screen, (127, 232, 255), sprite.pos, BIRD_RADIUS + 6, 4)
        pygame.display.flip()

    def molt_phase(self):
        """
        Retire one aging bird from EACH COOP SIDE (not each species),
        weighted by age. This keeps population pressure tied to physical
        location on the field, matching how breed_phase now works.
        """
        self.phase_message = "Molt phase: the oldest birds on each side may retire from the flock..."
        self.draw()
        time.sleep(0.6)

        for side in (True, False):
            group = [s for s in self.sprites if s.bird.side == side]
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
        """
        Runs the Crow Hive's full turn. Each stage of the real pipeline
        (encode -> reduce -> build circuit -> entangle -> anneal -> measure
        -> decide) is paired with its matching tutorial corner-overlay step
        IF full_tutorial is on. Because the overlay is non-blocking, the
        graph panel and entanglement-pulse animation for that exact stage
        keep rendering live underneath the explanation text.
        """
        crow_birds = [s.bird for s in self.sprites if s.bird.species is False]
        all_birds = [s.bird for s in self.sprites]

        def show_step(key, hold_seconds=1.1):
            if self.full_tutorial:
                self.popup.queue_sequence([key], blocking=False)
            self._pump_and_render(hold_seconds)

        # STEP 1+2: encoding & reduction (no graph yet, just narrate)
        self.phase_message = "Encoding the flock as logic clauses..."
        show_step("encoding")
        self.phase_message = "Reducing to a Max-Cut graph..."
        show_step("reduction")

        mind = QuantumFlockMind(all_birds, time_steps=self.time_steps)
        self.current_graph = mind.graph
        self.current_node_index = mind.node_index
        self.current_bits = None
        self.current_top_results = None
        self.pulse_edges = []

        # STEP 3: superposition -- graph is now visible, uncolored (no
        # measurement yet so nothing to highlight)
        self.phase_message = "Superposition: every qubit is every answer at once..."
        show_step("superposition")

        # STEP 4: entanglement -- pulse every edge in the graph briefly to
        # visualize RZZ gates "acting" on connected qubits
        self.phase_message = "Entangling connected qubits (RZZ gates)..."
        self.pulse_edges = list(self.current_graph.edges())
        show_step("entanglement", hold_seconds=1.6)
        self.pulse_edges = []

        # STEP 5: annealing
        self.phase_message = f"Annealing over {self.time_steps} time-steps..."
        show_step("annealing", hold_seconds=1.4)

        # STEP 6: measurement -- run the real circuit now, then show the
        # probability bar chart alongside the "measurement" explanation
        self.phase_message = "Running the circuit on Qiskit's Aer simulator..."
        self._pump_and_render(0.3)
        solution = mind.think(shots=2000)
        self.current_bits = solution
        self.current_top_results = mind.top_results
        show_step("measurement", hold_seconds=2.2)

        # Decision
        self.phase_message = "The Hive is deciding its move..."
        show_step("decision")

        movable = [b for b in crow_birds]
        chosen = mind.pick_best_move(movable)
        if chosen is not None:
            chosen.move()
        self.relayout()
        self.animate_until_settled()
        self.phase_message = "The Hive has moved. Your turn!"

    def _pump_and_render(self, seconds):
        """Run the event loop for roughly `seconds`, allowing SPACE to skip
        the current tutorial step early, while continuing to draw every
        frame (so animations underneath the overlay keep playing)."""
        elapsed = 0.0
        while elapsed < seconds:
            dt = 1.0 / TICK_RATE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.popup.handle_continue()
                    elapsed = seconds  # skip the rest of this hold
            self.popup.tick(dt)
            self.draw()
            self.clock.tick(TICK_RATE)
            elapsed += dt

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
    flock_size = run_flock_size_menu(screen)
    time_steps = run_difficulty_menu(screen)
    return flock_size, time_steps


def run_flock_size_menu(screen):
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


def run_difficulty_menu(screen):
    """
    Lets the player choose the Hive's annealing schedule length
    (time_steps) before play starts -- the "how smart is the Hive" dial.
    Fewer steps means the cost Hamiltonian never gets to dominate, so the
    Hive's measured answer stays closer to a noisy coin-flip; more steps
    means the annealing schedule has time to sharpen the distribution
    around the truly best split, producing a more consistently optimal
    (and harder to beat) opponent.
    """
    font_title = pygame.font.SysFont("consolas", 36, bold=True)
    font_btn = pygame.font.SysFont("consolas", 22)
    font_small = pygame.font.SysFont("consolas", 16)
    clock = pygame.time.Clock()

    title_surf = font_title.render("Hive Intelligence", True, FONT_COLOR)

    options = [
        ("Erratic   (2 anneal steps)", 2, "Mostly random exploration -- very beatable."),
        ("Balanced  (4 anneal steps)", 4, "Some convergence toward the best split."),
        ("Sharp     (8 anneal steps)", 8, "Strong convergence -- a tough opponent."),
        ("Ruthless  (14 anneal steps)", 14, "Near-optimal play almost every turn."),
    ]
    buttons = []
    for i, (label, n, desc) in enumerate(options):
        surf = font_btn.render(label, True, FONT_COLOR)
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, 330 + i * 80))
        desc_surf = font_small.render(desc, True, (210, 210, 200))
        buttons.append((surf, rect, n, desc_surf))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                for surf, rect, n, desc_surf in buttons:
                    if rect.collidepoint(event.pos):
                        return n

        screen.fill(COOP_BG)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150)))
        hint = font_small.render("This sets how many quantum annealing steps the Hive gets each turn.",
                                  True, (230, 230, 220))
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 200)))

        for surf, rect, n, desc_surf in buttons:
            pygame.draw.rect(screen, BUTTON_BG, rect.inflate(40, 36), border_radius=10)
            screen.blit(surf, rect)
            screen.blit(desc_surf, desc_surf.get_rect(center=(rect.centerx, rect.bottom + 18)))
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

    flock_size, time_steps = run_menu(screen)

    manager = GameManager(screen, full_tutorial=True, time_steps=time_steps)

    starter_genes_hen = [(True, True, True), (True, True, None), (True, None, None), (True, None, None), (True, True, None)]
    starter_genes_crow = [(False, False, False), (False, False, None), (False, None, None), (False, None, None), (False, False, None)]
    for i in range(flock_size):
        manager.add_bird(True, starter_genes_hen[i % len(starter_genes_hen)])
        manager.add_bird(False, starter_genes_crow[i % len(starter_genes_crow)])
    manager.relayout(animate=False)
    manager.age_all()

    manager.popup.queue_sequence(["intro"], blocking=True)
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
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    manager.time_steps = min(manager.time_steps + 1, 20)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    manager.time_steps = max(manager.time_steps - 1, 1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                manager.handle_click(event.pos)

        manager.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
