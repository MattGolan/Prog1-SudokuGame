import pygame
from cell import Cell
from sudoku_generator import generate_sudoku
import copy

# Initializes pygame for use within class.
pygame.init()


class Board:
    def __init__(self, width, height, screen, difficulty):

        # Initializes object attributes.
        self.width = width
        self.height = height
        self.screen = screen
        # Determines difficulty based on what text is passed in as a string.
        if difficulty == "EASY":
            self.difficulty = 30
        elif difficulty == "MEDIUM":
            self.difficulty = 40
        else:
            self.difficulty = 50
        # Generates the sudoku board by calling generate_sudoku.
        self.board = generate_sudoku(9, self.difficulty)
        # Creates an empty list.
        self.cells = []
        # Appends Cell objects to the empty list in a 2D format.
        for row_index, row_value in enumerate(self.board):
            current_row = []
            for col_index, col_value in enumerate(row_value):
                current_row.append(Cell(col_value, row_index, col_index, self.screen))
            self.cells.append(current_row)
        # Creates a copy of original cells that will not be altered.
        self.original_cells = []
        for row_index, row_value in enumerate(self.board):
            current_row = []
            for col_index, col_value in enumerate(row_value):
                current_row.append(Cell(col_value, row_index, col_index, self.screen))
            self.original_cells.append(current_row)
        # Originally not assigned a value.
        self.selected_cell = None
        # Creates a deep copy
        self.test_board = copy.deepcopy(self.board)

    def draw(self):

        # draws the vertical lines every 3rd bolded
        for index in range(0, 10):
            if index % 3 == 0:
                pygame.draw.line(self.screen, (0, 0, 0), (index * (600 / 9), 0), (index * (600 / 9), 600), 10)
            else:
                pygame.draw.line(self.screen, (0, 0, 0), (index * (600 / 9), 0), (index * (600 / 9), 600), 5)

        # draws the horizontal lines every 3rd bolded
        for index in range(0, 10):
            if index % 3 == 0:
                pygame.draw.line(self.screen, (0, 0, 0), (0, index * (600 / 9)), (600, index * (600 / 9)), 10)
            else:
                pygame.draw.line(self.screen, (0, 0, 0), (0, index * (600 / 9)), (600, index * (600 / 9)), 5)

        # draws the cells
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):

        # drawing the left red border around the cell.
        pygame.draw.line(self.screen, (255, 0, 0), (row * 67, col * 67),
                         (row * 67, (col + 1) * 67), 10)

        # drawing the bottom red border around the cell
        pygame.draw.line(self.screen, (255, 0, 0), (row * 67, (col + 1) * 67),
                         ((row + 1) * 67, (col + 1) * 67), 10)

        # drawing the right red border around the cell
        pygame.draw.line(self.screen, (255, 0, 0), ((row + 1) * 67, col * 67),
                         ((row + 1) * 67, (col + 1) * 67), 10)

        # drawing the top red border around the cell
        pygame.draw.line(self.screen, (255, 0, 0), (row * 67, col * 67),
                         ((row + 1) * 67, col * 67), 10)

        # Assigns selected_cell
        self.selected_cell = self.cells[row][col]

    def click(self, x, y):

        if (0 <= x <= 600) and (0 <= y <= 600):
            row = int(x // (600 / 9))
            col = int(y // (600 / 9))

            coordinates = (row, col)
            return coordinates

        else:
            return None

    def clear(self):
        # if the cell can be cleared, then the value of the cell is set to 0
        if self.selected_cell.can_be_cleared == True:
            self.selected_cell.value = 0

    def sketch(self, value):
        try:
            # basically by making a try loop we can avoid crashes and we need to verify if its an original cell
            if self.selected_cell.can_be_cleared:
                self.selected_cell.set_sketched_value(value)
        except:
            pass

    def place_number(self, value):
        try:
            # same concept with sketch function we need to verify if the cell can be changed
            if self.selected_cell.can_be_cleared:
                self.selected_cell.set_cell_value(value)
        except:
            pass

    def reset_to_original(self):
        # redefines the cells list by the original board provided by the self.board 2d list
        self.cells = self.original_cells

    def is_full(self):
        # initializing the boolean variable full as true
        full = True
        # looping though the 2d list of self.cells, if there is any cells that aren't filled, the full becomes False
        for row in range(0, 9):
            for col in range(0, 9):
                if self.cells[row][col].value == 0:
                    full = False
        return full

    def update_board(self):
        # looping through the board and the cells 2d array and adjusting the values
        for row in range(0, 9):
            for col in range(0, 9):
                self.board[row][col] = self.cells[row][col].value

    def find_empty(self):
        # boolean for if an empty cell exists
        exists = False
        x = 0
        y = 0
        # loops through the cells 2d list finding the empty cell
        for row in range(0, 9):
            for col in range(0, 9):
                if self.cells[row][col].value == 0:
                    x = self.cells[row][col].row
                    y = self.cells[row][col].col
                    exists = True
        if exists == True:
            return x, y
        else:
            return None

    def check_board(self):
        # Checks to make sure row contains all single digit ints.
        for row in self.board:
            for num in range(1, 10):
                if num not in row:
                    return False
        # Checks to make sure every col contains all single digit ints.
        for index in range(0, 9):
            counter = 0
            # Makes a temporary list for all ints in each col.
            temp_col = []
            while counter < 9:
                temp_col.append(self.board[counter][index])
                counter += 1
            # Checks temp_col for each single digit int.
            for num in range(1, 10):
                if num not in temp_col:
                    return False
        for row in range(0, 9, 3):
            # by using increments of 3 we can evaluate the boxes as boxes!
            for col in range(0, 9, 3):
                # turning it into a matter of boxes we can check the final win condition all at once!
                box = (self.board[row][col:col + 3] + self.board[row + 1][col:col + 3] + self.board[row + 2][
                                                                                         col:col + 3])
                if len(set(box)) != 9:
                    return False
        return True
