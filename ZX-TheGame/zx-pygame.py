import pygame
import pyzx as zx
import numpy as np
import math
import sys

# --- Pygame Initialization and Constants ---
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ZX-Simplifier: The Diagram Builder (Pygame)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
BLUE = (60, 60, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
INPUT_BOX_COLOR_ACTIVE = (150, 150, 255)
INPUT_BOX_COLOR_INACTIVE = (180, 180, 180)

# Fonts
FONT_SIZE_TITLE = 48
FONT_SIZE_HEADER = 28
FONT_SIZE_NORMAL = 20
FONT_SIZE_SMALL = 16

try:
    # Try loading a common system font, or fall back to default
    FONT_TITLE = pygame.font.Font(None, FONT_SIZE_TITLE)
    FONT_HEADER = pygame.font.Font(None, FONT_SIZE_HEADER)
    FONT_NORMAL = pygame.font.Font(None, FONT_SIZE_NORMAL)
    FONT_SMALL = pygame.font.Font(None, FONT_SIZE_SMALL)
except:
    FONT_TITLE = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
    FONT_HEADER = pygame.font.SysFont("Arial", FONT_SIZE_HEADER)
    FONT_NORMAL = pygame.font.SysFont("Arial", FONT_SIZE_NORMAL)
    FONT_SMALL = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)

# --- UI Components ---

class InputBox:
    """
    A simple text input box for Pygame.
    """
    def __init__(self, x, y, w, h, text='', multiline=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = INPUT_BOX_COLOR_INACTIVE
        self.text = text
        self.font = FONT_NORMAL
        self.active = False
        self.multiline = multiline
        self.lines = [text] if multiline else [text]
        self.cursor_pos = len(text) # For single line
        self.scroll_offset_y = 0 # For multiline scrolling
        self.max_lines_display = h // self.font.get_linesize() # How many lines fit

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = INPUT_BOX_COLOR_ACTIVE if self.active else INPUT_BOX_COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.multiline:
                        self.lines.append('')
                        self.cursor_pos = 0 # Cursor at start of new line
                        # Auto-scroll down if past visible area
                        if len(self.lines) > self.max_lines_display:
                            self.scroll_offset_y = max(0, len(self.lines) - self.max_lines_display)
                    else:
                        # For single line, return might trigger submission
                        pass 
                elif event.key == pygame.K_BACKSPACE:
                    if self.multiline:
                        if self.cursor_pos > 0:
                            self.lines[-1] = self.lines[-1][:-1]
                            self.cursor_pos -= 1
                        elif len(self.lines) > 1: # If at start of a line and not first line
                            self.lines.pop()
                            self.cursor_pos = len(self.lines[-1]) # Move cursor to end of previous line
                            if len(self.lines) <= self.max_lines_display:
                                self.scroll_offset_y = 0 # Scroll back up if fits
                            else:
                                self.scroll_offset_y = max(0, len(self.lines) - self.max_lines_display)
                    else:
                        self.text = self.text[:-1]
                        self.cursor_pos = len(self.text)
                else:
                    if self.multiline:
                        self.lines[-1] += event.unicode
                        self.cursor_pos = len(self.lines[-1])
                        # If the last line exceeds box width, don't auto-wrap but allow input.
                        # For simplicity, we won't implement auto-wrap here but could be added.
                    else:
                        self.text += event.unicode
                        self.cursor_pos = len(self.text)
    
    def get_text(self):
        return "\n".join(self.lines) if self.multiline else self.text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, BLACK, self.rect, 2) # Border

        if self.multiline:
            # Display visible lines
            y_offset = self.rect.y
            for i in range(self.scroll_offset_y, len(self.lines)):
                if (y_offset - self.rect.y) + self.font.get_linesize() > self.rect.h:
                    break # Stop if beyond visible height
                line_surface = self.font.render(self.lines[i], True, BLACK)
                screen.blit(line_surface, (self.rect.x + 5, y_offset))
                y_offset += self.font.get_linesize()
            
            # Draw cursor (simple blinking cursor for active multiline box)
            if self.active:
                current_line_text = self.lines[-1]
                cursor_x = self.rect.x + 5 + self.font.size(current_line_text[:self.cursor_pos])[0]
                cursor_y = self.rect.y + 5 + (len(self.lines) - 1 - self.scroll_offset_y) * self.font.get_linesize()
                
                # Only draw if cursor is within visible bounds of the input box
                if self.rect.collidepoint(cursor_x, cursor_y) and self.rect.collidepoint(cursor_x, cursor_y + self.font.get_height()):
                    pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + self.font.get_height()), 2)

        else:
            txt_surface = self.font.render(self.text, True, BLACK)
            screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.h - txt_surface.get_height()) // 2))
            if self.active:
                # Draw cursor for single line
                cursor_x = self.rect.x + 5 + self.font.size(self.text)[0]
                cursor_y = self.rect.y + (self.rect.h - txt_surface.get_height()) // 2
                pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + self.font.get_height()), 2)


class Button:
    """
    A clickable button for Pygame.
    """
    def __init__(self, x, y, w, h, text, font, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.action = action

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    return self.action()
        return None

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2) # Border

        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

# --- Game Logic ---

class QuantumGame:
    """
    Manages the game flow for the "Build the Diagram Challenge" using pyzx,
    with a Pygame graphical interface.
    """
    def __init__(self):
        self.total_score = 0
        self.levels = [
            {
                "name": "Level 1: Build the Identity Gate (1 Qubit)",
                "target_sqasm": "qreg q[1];",
                "description": "Your goal is to write an SQASM string that simplifies to the identity gate on one qubit. (Example: 'qreg q[1];' or 'qreg q[1];z q[0];z q[0];')",
                "base_score": 100,
                "max_attempts": 3,
                "target_matrix": np.array([[1.+0.j]])
            },
            {
                "name": "Level 2: Build a Pauli-X Gate (1 Qubit)",
                "target_sqasm": "qreg q[1];x q[0];",
                "description": "Your goal is to write an SQASM string that simplifies to a Pauli-X gate on one qubit. (Example: 'qreg q[1];x q[0];')",
                "base_score": 150,
                "max_attempts": 4,
                "target_matrix": np.array([[0.+0.j, 1.+0.j], [1.+0.j, 0.+0.j]])
            },
            {
                "name": "Level 3: Build a Hadamard Gate (1 Qubit)",
                "target_sqasm": "qreg q[1];h q[0];",
                "description": "Your goal is to write an SQASM string that simplifies to a Hadamard gate on one qubit. (Example: 'qreg q[1];h q[0];')",
                "base_score": 200,
                "max_attempts": 5,
                "target_matrix": (1/np.sqrt(2)) * np.array([[1.+0.j, 1.+0.j], [1.+0.j, -1.+0.j]])
            },
            {
                "name": "Level 4: Build a CNOT Gate (2 Qubits)",
                "target_sqasm": "qreg q[2];cx q[0],q[1];",
                "description": "Your goal is to write an SQASM string that simplifies to a CNOT gate with q[0] as control and q[1] as target. (Example: 'qreg q[2];cx q[0],q[1];')",
                "base_score": 250,
                "max_attempts": 6,
                "target_matrix": np.array([
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0]
                ])
            },
            {
                "name": "Level 5: Build a Z-Spider (Phase pi/2)",
                "target_sqasm": "qreg q[1]; s q[0];",
                "description": "Your goal is to write an SQASM string that creates a Z-spider with a phase of pi/2 (e.g., an S gate) on one qubit. (Example: 'qreg q[1];s q[0];')",
                "base_score": 300,
                "max_attempts": 7,
                "target_matrix": np.array([[1.+0.j, 0.+0.j], [0.+0.j, 0.+1.j]])
            }
        ]
        self.current_level_idx = 0
        self.current_level_attempts = 0
        self.user_sqasm_input = InputBox(50, 400, 600, 200, multiline=True)
        self.submit_button = Button(50, 620, 150, 50, "Submit SQASM", FONT_NORMAL, GREEN, (0, 255, 0), self.submit_sqasm)
        self.next_level_button = Button(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 70, 150, 50, "Next Level", FONT_NORMAL, BLUE, (100, 100, 255), self.go_to_next_level)
        
        self.feedback_message = ""
        self.user_matrix_display = None
        self.level_won = False
        self.game_over = False

    def _get_diagram_matrix(self, sqasm_string):
        """
        Helper to convert an SQASM string into a pyzx Graph and get its matrix representation.
        Includes simplification.
        """
        try:
            g = zx.sqasm(sqasm_string)
            zx.full_reduce(g)
            return g.to_matrix(preserve_scalar=False)
        except Exception as e:
            self.feedback_message = f"Error: Invalid SQASM syntax or diagram issue: {e}"
            return None

    def _check_equivalence(self, user_matrix, target_matrix, tolerance=1e-9):
        """
        Checks if two complex matrices are equivalent, considering a global scalar factor.
        """
        if user_matrix is None or target_matrix is None:
            return False

        if user_matrix.shape != target_matrix.shape:
            self.feedback_message = f"Incorrect! Matrix shape mismatch. Expected {target_matrix.shape}, got {user_matrix.shape}."
            return False

        if np.allclose(target_matrix, 0, atol=tolerance):
            return np.allclose(user_matrix, 0, atol=tolerance)

        target_flat = target_matrix.flatten()
        user_flat = user_matrix.flatten()

        non_zero_idx = -1
        for i, val in enumerate(target_flat):
            if not np.isclose(val, 0, atol=tolerance):
                non_zero_idx = i
                break

        if non_zero_idx == -1: # Target matrix is all zeros, but user matrix might not be
            return np.allclose(user_matrix, 0, atol=tolerance)

        target_ref = target_flat[non_zero_idx]
        user_ref = user_flat[non_zero_idx]
        
        if np.isclose(target_ref, 0, atol=tolerance): # Should not happen if non_zero_idx is correct
            return False 
        
        scalar_factor = user_ref / target_ref
        
        is_equivalent = np.allclose(user_matrix, scalar_factor * target_matrix, atol=tolerance)
        if not is_equivalent:
            self.feedback_message = "Incorrect! Your diagram's operation does not match the target."
        return is_equivalent


    def submit_sqasm(self):
        if self.level_won or self.game_over:
            return # Don't submit if level already won or game over

        self.current_level_attempts += 1
        sqasm_string = self.user_sqasm_input.get_text()
        
        user_matrix = self._get_diagram_matrix(sqasm_string)
        self.user_matrix_display = user_matrix # Store for display

        current_level_info = self.levels[self.current_level_idx]
        target_matrix = current_level_info["target_matrix"]

        if user_matrix is None:
            # Error message already set by _get_diagram_matrix
            pass 
        elif self._check_equivalence(user_matrix, target_matrix):
            self.feedback_message = "Correct! Your diagram is equivalent to the target!"
            self.level_won = True
            self.total_score += current_level_info["base_score"]
        else:
            # Feedback message set by _check_equivalence
            pass

        if not self.level_won and self.current_level_attempts >= current_level_info["max_attempts"]:
            self.feedback_message = f"Attempts exhausted for {current_level_info['name']}! Game Over."
            self.game_over = True

    def go_to_next_level(self):
        if not self.level_won and not self.game_over:
            return # Can't go to next level if current not won or game not over

        self.current_level_idx += 1
        if self.current_level_idx < len(self.levels):
            self.current_level_attempts = 0
            self.user_sqasm_input = InputBox(50, 400, 600, 200, multiline=True) # Reset input box
            self.feedback_message = ""
            self.user_matrix_display = None
            self.level_won = False
            self.game_over = False # Reset game over state for new level
        else:
            self.feedback_message = "Congratulations! You completed all levels!"
            self.game_over = True

    def draw_text(self, text, font, color, x, y, align="left"):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "center":
            text_rect.center = (x, y)
        elif align == "right":
            text_rect.right = x
        else: # left
            text_rect.topleft = (x, y)
        SCREEN.blit(text_surface, text_rect)

    def draw_matrix(self, matrix, x, y, title, max_width, max_height):
        # Format matrix for display, handling complex numbers
        # Removed 'suppress=True' from np.array2string
        matrix_str = np.array2string(matrix, precision=2)
        lines = matrix_str.splitlines()

        # Render title
        self.draw_text(title, FONT_HEADER, BLACK, x, y)
        current_y = y + FONT_HEADER.get_height() + 10

        # Calculate dimensions for the background rectangle
        # This will need to be re-calculated after getting line sizes
        max_line_width = 0
        for line in lines:
            line_width = FONT_SMALL.size(line)[0]
            if line_width > max_line_width:
                max_line_width = line_width
        
        matrix_display_width = max_line_width + 20 # 10 padding each side
        matrix_display_height = len(lines) * FONT_SMALL.get_height() + FONT_HEADER.get_height() + 20 # 10 padding top/bottom

        # Ensure the background rectangle fits within the overall designated area
        rect_width = min(matrix_display_width, max_width)
        rect_height = min(matrix_display_height, max_height)

        # Draw a translucent background behind the text
        bg_rect = pygame.Rect(x, y, rect_width, rect_height)
        s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        s.fill((LIGHT_GRAY[0], LIGHT_GRAY[1], LIGHT_GRAY[2], 180)) # 180 alpha
        SCREEN.blit(s, (bg_rect.x, bg_rect.y))

        # Redraw text on top of the background
        self.draw_text(title, FONT_HEADER, BLACK, x, y)
        current_y = y + FONT_HEADER.get_height() + 10
        for line in lines:
            self.draw_text(line, FONT_SMALL, BLACK, x + 10, current_y)
            current_y += FONT_SMALL.get_height()


    def run_game_loop(self):
        """
        The main Pygame event loop.
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle input for the SQASM input box
                self.user_sqasm_input.handle_event(event)
                
                # Handle button clicks
                if self.submit_button.handle_event(event) and self.level_won:
                    # If submit leads to a win, set focus on next_level_button for a moment.
                    # Or just wait for the next event loop cycle.
                    pass 
                
                if self.next_level_button.handle_event(event) and not self.game_over:
                    # After clicking next level, the current level state is reset.
                    pass

            # --- Drawing ---
            SCREEN.fill(WHITE) # Clear screen

            # Game Title
            self.draw_text("ZX-Simplifier: The Diagram Builder", FONT_TITLE, BLACK, SCREEN_WIDTH // 2, 30, align="center")

            # Current Level Info
            current_level_info = self.levels[self.current_level_idx]
            self.draw_text(f"Level: {current_level_info['name']}", FONT_HEADER, BLUE, 50, 90)
            self.draw_text(current_level_info['description'], FONT_NORMAL, BLACK, 50, 130)
            self.draw_text(f"Attempts: {self.current_level_attempts} / {current_level_info['max_attempts']}", FONT_NORMAL, BLACK, 50, 170)
            self.draw_text(f"Total Score: {self.total_score}", FONT_HEADER, BLACK, SCREEN_WIDTH - 50, 90, align="right")

            # Target Matrix Display
            self.draw_matrix(current_level_info["target_matrix"], 700, 130, "Target Matrix:", 450, 200)

            # User Input Area
            self.draw_text("Your SQASM Input:", FONT_HEADER, BLACK, 50, 360)
            self.user_sqasm_input.draw(SCREEN)

            # Submit Button
            self.submit_button.draw(SCREEN)

            # User's Matrix Display
            if self.user_matrix_display is not None:
                self.draw_matrix(self.user_matrix_display, 700, 380, "Your Diagram's Matrix:", 450, 200)
            
            # Feedback Message
            feedback_color = GREEN if "Correct!" in self.feedback_message else RED
            self.draw_text(self.feedback_message, FONT_HEADER, feedback_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, align="center")

            # Next Level Button (only shown if level won and not game over)
            if self.level_won and not self.game_over:
                self.next_level_button.draw(SCREEN)
            elif self.game_over:
                self.draw_text("Game Over!", FONT_TITLE, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, align="center")
                self.draw_text("Restart? (Quit and Rerun)", FONT_NORMAL, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, align="center")


            pygame.display.flip() # Update the full display Surface to the screen
            clock.tick(60) # Limit frame rate to 60 FPS

        pygame.quit()
        sys.exit()

    def start_game(self):
        self.run_game_loop()

# This block allows you to run the game directly by executing this file
if __name__ == "__main__":
    game = QuantumGame()
    game.start_game()
