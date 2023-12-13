import pygame


# Modified grid size to conform with smaller specifications.
class Cell:
    def __init__(self, value, row, col, screen):
        # Initializes attributes.
        self.value = value
        self.initial_value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketch = False

        # determines which cells are preset and which are empty which can be readjusted
        if self.initial_value > 0:
            self.can_be_cleared = False
        else:
            self.can_be_cleared = True

    def set_cell_value(self, value):
        # Setter updates cell value.
        self.value = value

    def set_sketched_value(self, value):
        # Setter updates cell value and defines sketch attribute as true.
        self.value = value
        self.sketch = True

    # Completed after watching Module 9 videos. Credit to L.Zhou for overall approach.
    def draw(self):

        font = pygame.font.Font(None, 50)

        # if there is a nonzero value, and it is not a sketch, then the color will be black
        if self.value != 0 and not self.sketch:
            surface = font.render(str(self.value), 0, (0, 0, 0))
            rectangle = surface.get_rect(center=((self.row * (600 / 9) + 33.333), (self.col * (600 / 9) + 33.333)))
            self.screen.blit(surface, rectangle)

        # if there is a nonzero value, and it is a sketch, then the color will be grey
        if self.value != 0 and self.sketch:
            surface = font.render(str(self.value), 0, (128, 128, 128))
            rectangle = surface.get_rect(center=((self.row * (600 / 9) + 25), (self.col * (600 / 9) + 25)))
            self.screen.blit(surface, rectangle)

        # if the value is equal to 0, nothing is displayed
        if self.value == 0:
            surface = font.render(" ", 0, (255, 255, 255))
            rectangle = surface.get_rect(center=((self.row * (600 / 9) + 33.333), (self.col * (600 / 9) + 33.333)))
            self.screen.blit(surface, rectangle)
