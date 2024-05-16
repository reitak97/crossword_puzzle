""" Source header """

import csv

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class Clue:
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return f"{self.indices} {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}"

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) + other.indices)


class Crossword:
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'], row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-"*(6*CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)

    def change_guess(self,cl,g): # fill out the parameters
        """
        Allows updating the user's guess for a given clue.
        If the guess is valid, the board will be updated
        cl: Clue object
        g: string, the user's guess for the clue
        Returns: None
        """
        if len(g) == len(cl.answer) and all([c in GUESS_CHARS for c in g]):
            if cl.down_across == 'A':
                for i in range(len(g)):
                    self.board[cl.indices[0]][cl.indices[1] + i] = g[i]
            else:
                for i in range(len(g)):
                    self.board[cl.indices[0] + i][cl.indices[1]] = g[i]
                    
        elif len(g) != len(cl.answer):
            raise RuntimeError ("Guess length does not match the length of the clue.\n")
        else:
            raise RuntimeError ("Guess contains invalid characters.\n")
        
    def reveal_answer(self,cl): # fill out the parameters
        '''
        Reveals the answer to a clue on the board
        cl: Clue object
        Return: None
        '''
        if cl.down_across == 'A':
            for i in range(len(cl.answer)):
                self.board[cl.indices[0]][cl.indices[1] + i] = cl.answer[i]
        else:
            for i in range(len(cl.answer)):
                self.board[cl.indices[0] + i][cl.indices[1]] = cl.answer[i]
    def find_wrong_letter(self,cl):  # fill out the parameters
        """
        Identifies the first incorrect letter in a user's guess for a clue 
        cl: Clue object
        Returns: integer, the index of the first incorrect letter in the user's guess
        """

        if cl.down_across == 'A':
            for i in range(len(cl.answer)):
                if self.board[cl.indices[0]][cl.indices[1] + i] != cl.answer[i]:
                    return i
               
        elif cl.down_across == 'D':
            for i in range(len(cl.answer)):
                if self.board[cl.indices[0] + i][cl.indices[1]] != cl.answer[i]:
                    return i 
        return -1

    def is_solved(self):  # fill out the parameters
        """
        Determines if the crossword puzzle has been solved
        Returns: boolean, True if the puzzle has been solved, False otherwise
        """
        for key in self.clues:
            cl = self.clues[key]
            if cl.down_across == 'A':
                for i in range(len(cl.answer)):
                    if self.board[cl.indices[0]][cl.indices[1] + i] != cl.answer[i]:
                        return False
            else:
                for i in range(len(cl.answer)):
                    if self.board[cl.indices[0] + i][cl.indices[1]] != cl.answer[i]:
                        return False
        return True
