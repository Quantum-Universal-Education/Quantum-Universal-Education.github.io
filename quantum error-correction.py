import pygame
import random
import sys

pygame.init()

# --------------------
# Settings
# --------------------
WIDTH, HEIGHT = 1000, 600
FPS = 60

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
RED = (220, 50, 50)
GREEN = (50, 180, 80)
BLUE = (70, 120, 255)
PURPLE = (180, 80, 220)
GRAY = (180, 180, 180)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Error Correction Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

# --------------------
# Qubits
# --------------------
N_QUBITS = 7
qubits = []

spacing = WIDTH // (N_QUBITS + 1)

for i in range(N_QUBITS):
    qubits.append({
        "x": spacing * (i + 1),
        "y": HEIGHT // 2,
        "error": None,
        "timer": 0
    })

score = 0
lives = 5

# --------------------
# Buttons
# --------------------
buttons = {
    "X": pygame.Rect(250, 500, 120, 60),
    "Y": pygame.Rect(440, 500, 120, 60),
    "Z": pygame.Rect(630, 500, 120, 60)
}

selected_gate = "X"

spawn_timer = 0
SPAWN_INTERVAL = 120

running = True

while running:
    clock.tick(FPS)

    # --------------------
    # Events
    # --------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Select correction gate
            for gate, rect in buttons.items():
                if rect.collidepoint(mx, my):
                    selected_gate = gate

            # Click qubit
            for q in qubits:
                dx = mx - q["x"]
                dy = my - q["y"]

                if dx * dx + dy * dy < 35 * 35:
                    if q["error"] == selected_gate:
                        score += 10
                        q["error"] = None
                        q["timer"] = 0
                    elif q["error"] is not None:
                        score = max(0, score - 5)

    # --------------------
    # Spawn random errors
    # --------------------
    spawn_timer += 1

    if spawn_timer >= SPAWN_INTERVAL:
        spawn_timer = 0

        available = [q for q in qubits if q["error"] is None]

        if available:
            q = random.choice(available)
            q["error"] = random.choice(["X", "Y", "Z"])
            q["timer"] = 300

    # --------------------
    # Update timers
    # --------------------
    for q in qubits:
        if q["error"] is not None:
            q["timer"] -= 1

            if q["timer"] <= 0:
                q["error"] = None
                lives -= 1

    if lives <= 0:
        screen.fill(BLACK)

        txt = big_font.render(
            f"Game Over! Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            txt,
            (WIDTH // 2 - txt.get_width() // 2,
             HEIGHT // 2)
        )

        pygame.display.flip()
        pygame.time.wait(3000)
        break

    # --------------------
    # Draw
    # --------------------
    screen.fill(WHITE)

    title = big_font.render(
        "Quantum Error Correction",
        True,
        BLACK
    )
    screen.blit(title, (20, 20))

    score_text = font.render(
        f"Score: {score}",
        True,
        BLACK
    )
    screen.blit(score_text, (20, 80))

    lives_text = font.render(
        f"Lives: {lives}",
        True,
        BLACK
    )
    screen.blit(lives_text, (20, 120))

    instruction = font.render(
        f"Selected Correction: {selected_gate}",
        True,
        BLUE
    )
    screen.blit(instruction, (20, 160))

    # Connections
    for i in range(N_QUBITS - 1):
        pygame.draw.line(
            screen,
            GRAY,
            (qubits[i]["x"], qubits[i]["y"]),
            (qubits[i + 1]["x"], qubits[i + 1]["y"]),
            3
        )

    # Qubits
    for q in qubits:
        color = BLUE

        if q["error"] == "X":
            color = RED
        elif q["error"] == "Y":
            color = PURPLE
        elif q["error"] == "Z":
            color = GREEN

        pygame.draw.circle(
            screen,
            color,
            (q["x"], q["y"]),
            35
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (q["x"], q["y"]),
            35,
            2
        )

        label = "Q"

        if q["error"]:
            label = q["error"]

        text = font.render(label, True, BLACK)

        screen.blit(
            text,
            (
                q["x"] - text.get_width() // 2,
                q["y"] - text.get_height() // 2
            )
        )

    # Buttons
    for gate, rect in buttons.items():
        color = GRAY

        if gate == selected_gate:
            color = BLUE

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=10
        )

        txt = font.render(gate, True, BLACK)

        screen.blit(
            txt,
            (
                rect.centerx - txt.get_width() // 2,
                rect.centery - txt.get_height() // 2
            )
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
