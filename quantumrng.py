import pygame
import random

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Random Number Explorer")

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

clock = pygame.time.Clock()

bits = []
measurements = {"0": 0, "1": 0}

running = True

while running:
    screen.fill((20, 20, 30))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                # Simulated quantum measurement
                bit = random.choice([0, 1])

                bits.append(bit)

                measurements[str(bit)] += 1

                if len(bits) > 8:
                    bits.pop(0)

    title = big_font.render(
        "Quantum Random Number Explorer",
        True,
        (255, 255, 255),
    )
    screen.blit(title, (120, 30))

    instructions = font.render(
        "Press SPACE to measure a qubit",
        True,
        (200, 200, 255),
    )
    screen.blit(instructions, (250, 110))

    binary_string = "".join(map(str, bits))

    if binary_string:
        decimal_value = int(binary_string, 2)
    else:
        decimal_value = 0

    pygame.draw.rect(screen, (40, 40, 60), (150, 180, 600, 100))

    binary_text = font.render(
        f"Random Bits: {binary_string}",
        True,
        (255, 255, 100),
    )
    screen.blit(binary_text, (180, 210))

    decimal_text = font.render(
        f"Decimal Value: {decimal_value}",
        True,
        (100, 255, 100),
    )
    screen.blit(decimal_text, (180, 250))

    zero_count = measurements["0"]
    one_count = measurements["1"]

    total = max(zero_count + one_count, 1)

    bar_height_0 = int((zero_count / total) * 250)
    bar_height_1 = int((one_count / total) * 250)

    pygame.draw.rect(
        screen,
        (100, 180, 255),
        (250, 520 - bar_height_0, 100, bar_height_0),
    )

    pygame.draw.rect(
        screen,
        (255, 100, 100),
        (500, 520 - bar_height_1, 100, bar_height_1),
    )

    label0 = font.render(f"0 : {zero_count}", True, (255, 255, 255))
    screen.blit(label0, (250, 530))

    label1 = font.render(f"1 : {one_count}", True, (255, 255, 255))
    screen.blit(label1, (500, 530))

    theory = [
        "Quantum Idea:",
        "A qubit can exist in a superposition of 0 and 1.",
        "When measured, it collapses randomly.",
        "Repeated measurements create random bits.",
    ]

    y = 170
    for line in theory:
        text = font.render(line, True, (220, 220, 220))
        screen.blit(text, (20, y))
        y += 35

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
