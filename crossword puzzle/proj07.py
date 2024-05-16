""" Source header """
from operator import itemgetter
from crossword import Crossword
import sys


HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
                "\nC n - Display n of the current puzzle's down and across clues" \
                "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
                "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
                "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at row i, column j" \
                "\nH - Display the menu" \
                "\nS - Restart the game" \
                "\nQ - Quit the program"


OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"
"\nAcross"
"\nDown"
"\nPuzzle solved! Congratulations!"
"Letter {} is wrong, it should be {}"
"Invalid option/arguments. Type 'H' for help."
"Enter your guess (use _ for blanks): "
"This clue is already correct!"

RuntimeError("Guess length does not match the length of the clue.\n")
RuntimeError("Guess contains invalid characters.\n")


'''def input( prompt=None ):
   if prompt != None:
       print( prompt, end="" )
   aaa_str = sys.stdin.readline()
   aaa_str = aaa_str.rstrip( "\n" )
   print( aaa_str )
   return aaa_str
'''
   


# DEFINE YOUR FUNCTIONS HERE

def open_puzzle_file():
    '''
    Asks user to enter the filename of the puzzle they want to play. 
    Returns a Crossword object
    '''
    valid = False
    while not valid:
        try:
            filename = input(PUZZLE_PROMPT)
            cw = Crossword(filename)
            valid = True
        except FileNotFoundError:
            print(PUZZLE_FILE_ERROR)
    return cw

def display_clues(cw, num=0):
    '''
    Displays the first num clues in the crossword puzzle
    cw: Crossword object
    num: int, number of clues to display
    Return: None
    '''
    if num == 0:
        num = len(cw.clues)
    cl = cw.clues
    
    # Sort the clues by down/across
    cl_keys = sorted(cl, key=itemgetter(2))
    across_lst = []
    down_lst = []
    for key in cl_keys:
        if key[2] == 'A':
            across_lst.append(key)
        else:
            down_lst.append(key)
    if num > len(across_lst):
        num = len(across_lst)
    if num > len(down_lst):
        num = len(down_lst)
    print("Across")
    for i in range(num):
        print(cl[across_lst[i]])
    print()
    print("Down")
    for i in range(num):
        print(cl[down_lst[i]])
    
def validate(cw,option):
    '''
    Validates the user's input
    cw: Crossword object
    option: string, user's input
    Return: True if valid, None if invalid
    '''
    option = option.split()
    if len(option) == 2:
        if option[0] == "C" and option[1].isdigit() and int(option[1]) > 0:
            return True
    elif len(option) == 4:
        if option[0] == "G" or option[0] == "R" or option[0] == "T":
            if (int(option[1]),int(option[2]),option[3]) in cw.clues:
                return True
    if option[0] == "H" or option[0] == "S" or option[0] == "Q":
        return True
    
    return None
      
    
def main():
    cw = open_puzzle_file()
    print()
    display_clues(cw)
    print(cw)
    print(HELP_MENU)
    while True:
        option = input(OPTION_PROMPT)
        option = option.split()
        
        if validate(cw," ".join(option)) == None:
            print("Invalid option/arguments. Type 'H' for help.")
        elif option[0] == "C":
            display_clues(cw,int(option[1]))
        elif option[0] == "G":
            curr_clue = cw.clues[(int(option[1]),int(option[2]),option[3])]
            guess = input("Enter your guess (use _ for blanks): ").upper()
            valid = False
            while valid == False:
                try:
                    cw.change_guess(curr_clue,guess)
                    valid = True
                except RuntimeError as e:
                    print(e)
                    guess = input("Enter your guess (use _ for blanks): ").upper()
            print(cw)
        elif option[0] == "R":
            curr_clue = cw.clues[(int(option[1]),int(option[2]),option[3])]
            cw.reveal_answer(curr_clue)
            print(cw)
        elif option[0] == "T":
            curr_clue = cw.clues[(int(option[1]),int(option[2]),option[3])]
            index = cw.find_wrong_letter(curr_clue)
            if index != -1:
                if curr_clue.down_across == 'A':
                    print("Letter {} is wrong, it should be {}".format(index+curr_clue.indices[1],curr_clue.answer[index]))
            
                elif curr_clue.down_across == 'D':
                    
                    print("Letter {} is wrong, it should be {}".format(index+curr_clue.indices[0],curr_clue.answer[index]))
            else:
                print("This clue is already correct!")
              
        elif option[0] == "H":
            print(HELP_MENU)
        elif option[0] == "S":
            cw = open_puzzle_file()
            print()
            display_clues(cw)
            print(cw)
            print(HELP_MENU)
        elif option[0] == "Q":
            break
        if cw.is_solved():
            print("Puzzle solved! Congratulations!")
            break






if __name__ == "__main__":
    main()
