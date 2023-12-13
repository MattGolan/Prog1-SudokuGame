import math, random

# Group 24 - Matthew Golan, Caleb Jackson, Kevin Zheng, Melissa Mankewich.

"""Originally, we forked the repository and coded in REPLIT. However, in response to instructions provided by Armin 
Da Silvia Anton in the projects slack channel, we used our forked repository as a template to create a new private 
repository. We then pushed our preexisting code to our new private github repository."""

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length, removed_cells):
        # Initializes object by assigning passed in parameters.
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = []
        row_count, col_count = row_length, row_length
        # Creates a 2D list using assigned counting variables to conform with the row length.
        while row_count > 0:
            new_row = []
            while col_count > 0:
                # Appends nine zeros in the row.
                new_row.append(0)
                col_count -= 1
            # Appends nine rows into list.
            self.board.append(new_row)
            col_count = row_length
            row_count -= 1
        # Uses the imported math module to calculate the square root of the length.
        self.box_length = int(math.sqrt(row_length))

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''

    def get_board(self):
        # Returns current board.
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''

    def print_board(self):
        # Prints each row of the 2D list individually to conform with visual expectations.
        for index, item in enumerate(self.board):
            print(self.board[index])

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row

	Return: boolean
    '''

    def valid_in_row(self, row, num):
        # Uses a for loop to compare num with other integers in the list.
        for i in self.board[row]:
            if i == num:
                # Returns False if a match is found.
                return False
        return True

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column

	Return: boolean
    '''

    def valid_in_col(self, col, num):
        # Assigns a counter to ensure nine loops occur.
        counter = 0
        while counter < 9:
            # Compares passed in number to each element of the list.
            if self.board[counter][col] == num:
                return False
            counter += 1
        # Returns true if number is unique.
        return True

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        # Searches for num in subsections of rows and columns that correspond with each box.
        for r in self.board[int(row_start):int(row_start) + 3]:
            if num in r[int(col_start):int(col_start) + 3]:
                return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''

    def is_valid(self, row, col, num):
        # Returns False if not valid in row.
        if not self.valid_in_row(row, num):
            return False
        # Returns False if not valid in col.
        if not self.valid_in_col(col, num):
            return False
        # Assigns row_ind and col_ind based on which box the cell is located in.
        # Credit to A.Sarmiento for explaining that I needed to convert row and col to starting box indices.
        if 0 <= row <= 2:
            if 0 <= col <= 2:
                # Top left.
                row_ind = 0
                col_ind = 0
            elif 3 <= col <= 5:
                # Top middle.
                row_ind = 0
                col_ind = 3
            else:
                # Top right.
                row_ind = 0
                col_ind = 6
        elif 3 <= row <= 5:
            if 0 <= col <= 2:
                # Middle left.
                row_ind = 3
                col_ind = 0
            elif 3 <= col <= 5:
                # Middle middle.
                row_ind = 3
                col_ind = 3
            else:
                # middle right.
                row_ind = 3
                col_ind = 6
        else:
            # Bottom left.
            if 0 <= col <= 2:
                row_ind = 6
                col_ind = 0
            # Bottom middle.
            elif 3 <= col <= 5:
                row_ind = 6
                col_ind = 3
            # Bottom right.
            else:
                row_ind = 6
                col_ind = 6
        if not self.valid_in_box(row_ind, col_ind, num):
            return False
        # Returns True if all tests pass.
        else:
            return True

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        self.row_start = row_start
        self.col_start = col_start
        # Assigns variable with list of single-digit integers.
        unused_in_box = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # Assigns counter variable to restrict method to first three rows.
        row_counter = 3
        # Loop assess and modifies three by three square.
        while row_counter > 0:
            # Assigns counter variable to restrict method to first three columns.
            col_counter = 3
            while col_counter > 0:
                # strategy for randomly ordering list taken from https://note.nkmk.me/en/python-random-shuffle/.
                random.shuffle(unused_in_box)
                # Variable is assigned the new first element in the int list. Element is then removed.
                random_num = unused_in_box.pop()
                # Element is replaced with the random element.
                self.board[int(self.row_start)][int(self.col_start)] = random_num
                self.col_start += 1
                col_counter -= 1
            self.row_start += 1
            self.col_start = col_start
            row_counter -= 1

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        # Calls fill_box method and passes in the starting index for each diagonal box.
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''

    def fill_values(self):
        # Calls methods to replace placeholder elements.
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called

    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''

    def remove_cells(self):
        # Assigns temp_counter with number of cells to be removed.
        temp_counter = self.removed_cells
        while temp_counter >= 1:
            # Randomly selects an element of the 2D list.
            removal_row = random.randint(0, 8)
            removal_col = random.randint(0, 8)
            # Checks to make sure the selected element is not already zero.
            if self.board[removal_row][removal_col] != 0:
                self.board[removal_row][removal_col] = 0
                temp_counter -= 1
            else:
                pass


'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board
