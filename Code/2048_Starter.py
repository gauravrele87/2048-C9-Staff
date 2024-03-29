"""
Project: "2048 in Python!"

Developed by: Kunal Mishra

Developed for: beginning students in Computer Science

Dependencies: 'getch' module, installed via the terminal command 'python3 -m pip install getch'
              'termcolor' module, installed via the terminal command 'python3 -m pip install termcolor'

To run: python3 2048_Starter.py

Student Learning Outcomes:
    Various levels of comfort with:
        large projects and abstraction
        understanding and modeling off existing code
        variables
        functional programming
        loops and conditionals
        multidimensional arrays
        CLI programming and terminal GUIs

Skill Level:
    precedes Hog and succeeds Rock, Paper, Scissors (bridges the two in terms of complexity and difficulty)
    assumed knowledge of language and concepts, but without mastery or even comfortability with them
    ~10 hours of experience/class/lecture coming into this project

Usage:
    Uses a terminal GUI and arrow keys for control and the key element of this project is that it will
    be much more interactive than any of the projects previously used in the workshop. Kids will be able to look
    at the elements of a large project and understand how each function comes together to create a game

Abstraction Reference Guide:

    Main            - responsible for starting the game and directing control to each function, the tests, or quitting
        board       - a variable within main that contains the current board and is passed to most functions as an argument

    System Functions:
        get_key_press   - returns the user's key_press input as an ascii value
        clear           - clears the screen (should be called before each print_board call)
        pause           - a function used by the GUI to allow for a slight delay that is more visually appealing in placing the new piece


    Board Functions:
        make_board      - creates a new, empty square board of N x N dimension
        print_board     - prints out the state of the argument board
        board_full      - returns True if the board is full and False otherwise


    Logic:
        swipe_right     - simulates a right swipe on the argument board
        swipe_left      - simulates a left swipe on the argument board
        swipe_up        - simulates a upward swipe on the argument board
        swipe_down      - simulates a downward swipe on the argument board
        swap            - occurs when the spacebar is pressed and randomly switches two different numbers on the board (1 use/game only)
        swap_possible   - a helper function that returns True if a swap is possible and False otherwise


    Useful Helper Functions:
        get_piece       - gets the piece from the given board at the given (x,y) coordinates or returns None if the position is invalid
        place_piece     - places the given piece on the given board at the given (x,y) coordinates and returns True or returns False if the position is invalid
        place_random    - user implemented function which places a random 2 OR 4 OR 8 in an empty part of the board
        have_lost       - responsible for determining if the game has been lost yet (no moves remain)
        move_possible   - responsible for determining if a move is possible from a single position
        move            - responsible for moving a piece, at the given (x,y) coordinates in the given direction on the given board

"""

#Installed via 'python3 -m pip install getch'
import getch
#Installed via 'python3 -m pip install termcolor'
import termcolor
import random
import os
import time

def get_key_press():
    #Utility function that gets which key was pressed and translates it into its character ascii value
    return ord(getch.getch());


def clear():
    #Utility function that clears the terminal GUI's screen - takes no arguments
    try:
        #For Macs and Linux
        os.system('clear');
    except:
        #For Windows
        os.system('cls');


def pause(seconds):
    #Utility function that pauses for the given amount of time
    #Arg seconds: a float or integer - number of seconds to pause for

    time.sleep(seconds);


def make_board(N):
    #Utility function that returns a new N x N empty board (empty spaces represented by '*')
    #Arg N: integer - board dimensions - must be greater than or equal to 1

    assert N >= 1, "Invalid board dimension";
    assert type(N) == int, "N must be an integer";
    return [["*" for x in range(N)] for x in range(N)];


def print_board(board):
    #Utility function that prints out the state of the board
    #Arg board: board - the board you want to print
    colors = {
        '*': None,
        '2': 'red',
        '4': 'green',
        '8': 'yellow',
        '16': 'blue',
        '32': 'magenta',
        '64': 'cyan',
        '128': 'grey',
        '256': 'white',
        '512': 'green',
        '1024': 'red',
        '2048': 'blue',
        '4096': 'magenta'
    };
    header = "Use the arrows keys to play 2048! -- Press t to test -- Press q to quit";
    print(header);
    N = len(board);
    vertical_edge = "";
    for i in range(N+2):
        vertical_edge += "-\t";
    print(vertical_edge);
    for y in range(N):
        row = "";
        for x in board[y]:
            row += termcolor.colored(x, colors[x]);
            row += "\t";
        print("|\t" + row + "|");
        if y is not N-1: print("")
    print(vertical_edge);


def board_full(board):
    #Utility function that returns True if the given board is full and False otherwise
    #Arg board: board - the board you want to check


    for row in board:
        for piece in row:
            if piece == '*':  return False;

    return True;


def move_possible(x, y, board):
    #Utility function that, given a position, will return True if a move is possible at that (x,y) position and False otherwise
    #Arg x: integer - x coordinate
    #Arg y: integer - y coordinate
    #Arg board: board - the board you wish to check if a move is possible on

    piece_at_xy = get_piece(x, y, board);
    if piece_at_xy == None:
        return False;
    elif piece_at_xy == '*':    #An empty space means a move is always possible
        return True;

    return (
           piece_at_xy == get_piece(x+1, y, board) or
           piece_at_xy == get_piece(x-1, y, board) or
           piece_at_xy == get_piece(x, y+1, board) or
           piece_at_xy == get_piece(x, y-1, board)
           );


def move(x, y, direction, board):
    #Utility function that moves the piece at the position (x,y) on the given board the given direction
    #Returns whether an action was actually executed or not
    #Arg x: integer - x coordinate
    #Arg y: integer - y coordinate
    #Arg direction: string - "left", "right", "up", "down"
    #Arg board: board - the board you wish to make a move on


    piece_at_xy = get_piece(x, y, board);                   #Getting necessary pieces

    assert piece_at_xy != '*', "Error in swipe logic";      #Logical debug case
    valid_direction = (direction == "left"  or
                       direction == "right" or
                       direction == "up"    or
                       direction == "down");
    assert valid_direction, "Invalid direction passed in";  #Logical debug case

    #The new x and y for the current piece (adjacent's current position) are stored alongside adjacent (fewer ifs + redundant code)
    if   direction == "left":   adjacent = (get_piece(x-1, y, board), x-1, y);
    elif direction == "right":  adjacent = (get_piece(x+1, y, board), x+1, y);
    elif direction == "up":     adjacent = (get_piece(x, y-1, board), x, y-1);
    elif direction == "down":   adjacent = (get_piece(x, y+1, board), x, y+1);

    if adjacent[0] == None:                                             #Edge of the board case (no action taken)
        return False;

    elif piece_at_xy != adjacent[0] and adjacent[0] != '*':             #Can't combine two numbers case (no action taken)
        return False;

    elif adjacent[0] == '*':                                            #Empty spot adjacent case (recursive movement in direction)
        place_piece('*', x, y, board);
        place_piece(piece_at_xy, adjacent[1], adjacent[2], board);
        move(adjacent[1], adjacent[2], direction, board);
        return True;

    elif piece_at_xy == adjacent[0]:                                    #Adjacent same numbers case (combine them)
        place_piece('*', x, y, board);
        place_piece(str(int(adjacent[0]) * 2), adjacent[1], adjacent[2], board);
        move(adjacent[1], adjacent[2], direction, board);
        return True;

    else:
        #Logical debug case
        assert False, "No way you should be in here. Error in move logic";

    return False;


#End of first section
############################################################################################################
################################## DO NOT CHANGE ANYTHING ABOVE THIS LINE ##################################    - Section 2 -
############################################################################################################


#Start of Step 0 ###########################################################################################

def main():
    #Only want to see the game board at the top
    clear();

    #Creating my new 4x4 board
    board = ">>>>>>>>>>YOUR CODE HERE 1<<<<<<<<<<"

    #Getting the game started with a single piece on the board
    place_random(board);
    print_board(board);

    #Runs the game loop until the user quits or the game is lost
    while True:

        #Gets the key pressed and stores it in the key variable
        key = ">>>>>>>>>>YOUR CODE HERE 2<<<<<<<<<<"

        #Quit case ('q')
        if ">>>>>>>>>>YOUR CODE HERE 3<<<<<<<<<<":
            #Quits the program
            break;

        #Up arrow
        elif ">>>>>>>>>>YOUR CODE HERE 3<<<<<<<<<<":
            #YOUR CODE HERE (1 line) <<<<<

        #Down arrow
        elif ">>>>>>>>>>YOUR CODE HERE 3<<<<<<<<<<":
            #YOUR CODE HERE (1 line) <<<<<

        #Right arrow
        elif ">>>>>>>>>>YOUR CODE HERE 3<<<<<<<<<<":
            #YOUR CODE HERE (1 line) <<<<<

        #Left arrow
        elif ">>>>>>>>>>YOUR CODE HERE 3<<<<<<<<<<":
            #YOUR CODE HERE (1 line) <<<<<

        #Space bar
        elif ">>>>>>>>>>YOUR CODE HERE 3<<<<<<<<<<":
            swap(board);

        #Special testing case: Runs test suite ('t')
        elif ">>>>>>>>>>YOUR CODE HERE 3<<<<<<<<<<":
            clear();
            tests();

        #Check to see if I've lost at the end of the game or not
        if ">>>>>>>>>>YOUR CODE HERE 4<<<<<<<<<<":

            print("You lost! Would you like to play again? (y/n)");
            if (input() == 'y'):
                main();
            return;

    print("Game Finished!");

#End of Step 0 #############################################################################################



#Start of Step 1 ###########################################################################################

def get_piece(x, y, board):
    #Utility function that gets the piece at a given (x,y) coordinate on the given board
    #Returns the piece if the request was valid and None if the request was not valid
    #Arg x: integer - x coordinate
    #Arg y: integer - y coordinate
    #Arg board: board - the board you wish to get the piece from

    #Ensure that x and y are both integers (use assert)
    ">>>>>>>>>>YOUR CODE HERE 5<<<<<<<<<<"

    #What does this do?
    N = len(board);

    #Checking that the (x,y) coordinates given are valid for the N x N board
    ">>>>>>>>>>YOUR CODE HERE 6<<<<<<<<<<"

    #Getting the piece on the board
    return board[y][x];


def place_piece(piece, x, y, board):
    #Utility function that places the piece at a given (x,y) coordinate on the given board if possible
    #Will overwrite the current value at (x,y), no matter what that piece is
    #Returns True if the piece is placed successfully and False otherwise
    #Arg piece: string - represents a piece on the board ('*' is an empty piece, '2' '8' etc. represent filled spots)
    #Arg x: integer - x coordinate
    #Arg y: integer - y coordinate
    #Arg board: board - the board you wish to place the piece on

    #Ensure that x and y are both integers (use assert)
    ">>>>>>>>>>YOUR CODE HERE 7<<<<<<<<<<"

    #What are the dimensions of the board?
    ">>>>>>>>>>YOUR CODE HERE 8<<<<<<<<<<"

    #Checking that the (x,y) coordinates given are valid for the board
    ">>>>>>>>>>YOUR CODE HERE 9<<<<<<<<<<"

    #Placing the piece on the board
    board[y][x] = piece;
    return True;

#End of Step 1 #############################################################################################


#Start of Step 2 ###########################################################################################

def place_random(board):
    #Helper function which is necessary for the game to continue playing
    #Returns True if a piece is placed and False if the board is full
    #Places a 2 (60%) or 4 (37%) or 8 (3%) randomly on the board in an empty space
    #Arg board: board - the board you wish to place the piece on

    #Delete this return statement AND comment before beginning Step 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    return;

    #Check if the board is full and return False if it is
    ">>>>>>>>>>YOUR CODE HERE 10<<<<<<<<<<"

    #random.random() generates a random decimal between [0, 1) ... Multiplying by 100 generates a number between [0, 100)
    generated = random.random() * 100;

    #Assign to_place according to my generated random number

    if generated < -1:                              #YOUR CODE HERE (replace -1) <<<<<
        to_place = "2";

    elif generated < -1 and generated >= -1:        #YOUR CODE HERE (replace -1) <<<<<
        to_place = "4";

    else:
        #What should to_place be if it's not a 2 or 4?
        to_place = ">>>>>>>>>>YOUR CODE HERE 11<<<<<<<<<<"


    #Variable keeps track of whether a randomly generated empty spot has been found yet
    found = False;
    N = len(board);

    while not found:
        #Generate a random (x,y) coordinate that we can try to put our new value in at
        #How did we "generate" a random number earlier? (hint: x and y should be between [0, N) )
        random_y = ">>>>>>>>>>YOUR CODE HERE 12<<<<<<<<<<"
        random_x = ">>>>>>>>>>YOUR CODE HERE 13<<<<<<<<<<"

        #Think about why this is necessary (hint: changes 3.4 (float) -> 3 (int))
        random_y = int(random_y);
        random_x = int(random_x);

        #If the randomly generated coordinates are empty, we have found a spot to place our random piece
        found = get_piece(random_x, random_y, board) == '*';

    #Place the piece at the randomly generated (x,y) coordinate
    ">>>>>>>>>>YOUR CODE HERE 14<<<<<<<<<<"

    return True;

#End of Step 2 #############################################################################################


#Start of Step 3 ###########################################################################################

def have_lost(board):
    #Helper function which checks at the end of each turn if the game has been lost
    #Returns True if the board is full and no possible turns exist and False otherwise


    #Delete this return statement AND comment before beginning Step 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    return False;


    N = len(board);

    #Check every (x,y) position on the board to see if a move is possible
    for y in range(N):
        for x in range(N):
            ">>>>>>>>>>YOUR CODE HERE 15<<<<<<<<<< (1 or 2 lines)"

    return True;

#End of Step 3 #############################################################################################


#Start of Step 4 ###########################################################################################

def end_move(board):
    #Prints the board after a swipe, pauses for .2 seconds, places a new random piece and prints the new state of the board
    #Arg board: board - the board you're finishing a move on

    #Print the board
    ">>>>>>>>>>YOUR CODE HERE 16<<<<<<<<<< (2 lines)"

    #Pause for .2 seconds
    ">>>>>>>>>>YOUR CODE HERE 17<<<<<<<<<<"

    #Place a random piece on the board at a random (x,y) position
    ">>>>>>>>>>YOUR CODE HERE 18<<<<<<<<<<"

    #Print the board again
    ">>>>>>>>>>YOUR CODE HERE 19<<<<<<<<<< (2 lines)"

#End of Step 4 #############################################################################################



#Start of Step 5 ###########################################################################################

def swipe_left(board):
    #YOUR COMMENT HERE
    action_taken = False;

    #YOUR COMMENT HERE
    N = len(board);

    #YOUR COMMENT HERE
    for y in range(N):
        for x in range(N):
            #YOUR COMMENT HERE
            piece_at_xy = get_piece(x, y, board);
            left_adjacent = get_piece(x-1, y, board);

            #YOUR COMMENT HERE
            if piece_at_xy == '*':
                continue;

            #YOUR COMMENT HERE
            if left_adjacent == None:
                continue;

            #YOUR COMMENT HERE
            action_taken = move(x, y, "left", board) or action_taken;


    #YOUR COMMENT HERE
    if action_taken:
        end_move(board);

def swipe_right(board):
    action_taken = False;

    N = len(board);

    for y in range(N):
        for x in range(N):
            #Don't worry about why this is done (is not needed for up or left)
            x = N-1-x;

            piece_at_xy = get_piece(x, y, board);
            right_adjacent = get_piece(x+1, y, board);

            if piece_at_xy == '*':
                continue;

            if right_adjacent == None:
                continue;

            action_taken = move(x, y, "right", board) or action_taken;


    if action_taken:
        end_move(board);

def swipe_up(board):
    action_taken = False;

    N = len(board);

    for y in range(N):
        for x in range(N):
            piece_at_xy = get_piece(x, y, board);
            up_adjacent = get_piece(x, y-1, board);

            if piece_at_xy == '*':
                continue;

            if up_adjacent == None:
                continue;

            action_taken = move(x, y, "up", board) or action_taken;


    if action_taken:
        end_move(board);

def swipe_down(board):
    action_taken = False;

    N = len(board);

    for y in range(N):
        #Don't worry about why this is done (is not needed for up or left)
        y = N-1-y;

        for x in range(N):

            piece_at_xy = get_piece(x, y, board);
            down_adjacent = get_piece(x, y+1, board);

            if piece_at_xy == '*':
                continue;

            if down_adjacent == None:
                continue;

            action_taken = move(x, y, "down", board) or action_taken;


    if action_taken:
        end_move(board);

#End of Step 5 #############################################################################################



#End of second section
############################################################################################################
######################## EXTRA FOR EXPERTS -- ATTEMPT AFTER FINISHING PROJECT ##############################    - Section 3 -
############################################################################################################

def swap(board):
    #Extra for Experts: an addition to our game that adds some randomness and chance!
    #Randomly swaps 2 different numbers on the board (only have one swap per game!)
    #Purpose: allows you to evade losing for a little while longer if the swap is useful
    #Key Concept: Can you explain why swapping two different numbers randomly might be useful?
    print("Not implemented yet!");
    return;

    #or (have not tested staff implementation)

    N = len(board);

    #Check that a swap can occur on the board (2 unique numbers/pieces)
    if not swap_possible(board):    return False;


    #Getting the first random piece to swap
    found = False;
    while not found:
        random_x1 = int(random.random() * N);
        random_y1 = int(random.random() * N);

        first_random_piece = get_piece(random_x1, random_y1, board);

        found = first_random_piece != '*';

    #Getting the second random piece to swap
    found = False;
    while not found:
        random_x2 = int(random.random() * N);
        random_y2 = int(random.random() * N);

        second_random_piece = get_piece(random_x2, random_y2, board);

        found = second_random_piece != '*' and second_random_piece != first_random_piece;


    #Swap the first and second pieces
    place_piece(second_random_piece, random_x1, random_y1, board);
    place_piece(first_random_piece, random_x2, random_y2, board);

    #An action was taken, so return true
    return True;

def swap_possible(board):
    #Extra for experts helper function for swap
    #Returns True if a swap is possible on the given board and False otherwise

    print("Not implemented yet!");
    return False;

    #or (have not tested staff implementation)

    container = set();
    for y in range(N):
        for x in range(N):
            piece_at_xy = get_piece(x, y, board);

            #Don't add empty spaces (they obviously can't be swapped...)
            if piece_at_xy != '*':  container.add(piece_at_xy);

    unique_pieces = len(container);

    if unique_pieces < 2:
        print("Cannot swap");
        return False;

    return True;






#End of third section
############################################################################################################
################################## DO NOT CHANGE ANYTHING BELOW THIS LINE ##################################   - Section 4 -
############################################################################################################

def tests():

    print("Testing...");

    msg = "Which option would you like to test?\n";
    msg += "0\t\tQuit\n";
    msg += "1\t\tget_piece and place_piece\n";
    msg += "2\t\tplace_random\n";
    msg += "3\t\thave_lost\n";
    msg += "4\t\tend_move"


    N = 4;
    board = make_board(N);

    #Runs suite of tests
    while True:

        print(msg);

        #Gets the key pressed
        key = get_key_press();


        ###########################################
        #Quit case ('0')
        if key == 48:
            quit();


        ###########################################
        #Test case: get_piece and place_piece ('1')
        elif key == 49:
            try:
                #Tests that they are returning None properly during an invalid (x,y) call
                result = (None == get_piece(-1, -1, board)          ==
                                  get_piece(N, N, board)
                         );
                assert result, "Not returning None properly during an invalid get or misunderstanding of spec w/ invalid inputs";

                result = (False == place_piece('*', -1, -1, board)  ==
                                   place_piece('*', N, N, board)
                         );
                assert result, "Not returning False properly during an invalid place or misunderstanding of spec w/ invalid inputs";


                #Tests that getting what was placed is possible
                to_place = '0';
                for y in range(N):
                    for x in range(N):
                        place_piece(to_place, x, y, board);
                        assert to_place == get_piece(x, y, board), ("Placed a piece at ", x, ", ", y, " but did not get same piece back");
                        to_place = chr(ord(to_place) + 1);

                assert board_full(board), "N by N Board needs to be full after N*N calls to place_piece at different (x,y) coordinates";

                #Checks against data abstraction violations
                temp_board = make_board(10);
                assert place_piece('7', 7, 7, temp_board) != False, "Abstraction violation. Hard-coded bounds in place_piece. Use the board's dimensions";
                assert get_piece(7, 7, temp_board) != None, "Abstraction violation. Hard-coded bounds in get_piece. Use the board's dimensions";


                print("Test passed.");
                board = make_board(N);      #Clears the board



            except IndexError:
                print("Test failed! Check bounds logic in place_piece and get_piece again. Quitting now...");
                quit();


        ##############################
        #Test case: place_random ('2')
        elif key == 50:
            for i in range(N):
                for j in range(N):  place_random(board);
                print_board(board);
                print("There should be ", (i+1)*(j+1), " spots filled. Pausing for 2 seconds...");
                pause(2);
            assert board_full(board), "N by N Board needs to be full after N*N calls to place_random";

            board = make_board(10);
            while not board_full(board):
                place_random(board);

            #Ensuring there are no asterisks, more 2's than 4's, and more 4's than 8's on the board
            empty, two, four, eight = 0, 0, 0, 0;
            for row in board:
                for piece in row:
                    if piece == '*':    empty += 1;
                    elif piece == '2':  two += 1;
                    elif piece == '4':  four += 1;
                    elif piece == '8':  eight += 1;
                    else:
                        print("Incorrect piece found: ", piece);
                        print("Examine to_place and place piece more carefully... Quitting now");

            assert empty == 0, "If board is full, there shouldn't be empty spaces";
            assert two > four > eight, "Test failed. Ratio is improbable";
            assert 75 >= two >= 45, "There don't seem to be enough 2's. Test failed.";
            assert 50 >= four >= 25, "There don't seem to be enough 4's. Test failed.";
            assert 10 >= eight >= 1, "There don't seem to be enough 8's. Test failed ... BUT retry 1 time";
            assert two + four + eight == 100, "There should only be 2s, 4s, and 8s placed by random";

            print("");
            print("Ensure the ratio is roughly 60/37/3: ");
            print("Twos: ", two);
            print("Fours:", four);
            print("Eights:", eight);
            print("");

            print("Test complete.");
            board = make_board(N);      #Clears the board


        ###########################
        #Test case: have_lost ('3')
        elif key == 51:
            assert not have_lost(board), "An empty board should not lose";
            place_piece('0', 0, 0, board);
            assert not have_lost(board), "A board with 1 piece should not lose";


            board = make_board(2);
            place_piece('0', 0, 0, board);
            place_piece('0', 1, 0, board);
            place_piece('0', 0, 1, board);
            place_piece('0', 1, 1, board);
            assert not have_lost(board), "A full board but with possible moves should not lose";

            board = make_board(2);
            place_piece('1', 0, 0, board);
            place_piece('0', 1, 0, board);
            place_piece('0', 0, 1, board);
            place_piece('1', 1, 1, board);
            assert have_lost(board), "A full board with no possible moves should lose";

            print("Test passed.");
            board = make_board(N);      #Clears the board

        ###########################
        #Test case: end_move ('4')
        elif key == 52:
            clear();
            print("If this msg does not get cleared, test failed. Ensure you always clear the screen before printing a board");
            pause(3.5);
            end_move(board);

            print("There should only be one board on the screen with 1 total piece at a random position");
            pause(3.5);

            end_move(board);
            print("There should only be one board on the screen with 2 total pieces at random positions");
            print("If two boards are on the screen, ensure you always clear the screen before printing a board");
            pause(4);


            now = time.time();
            end_move(board);
            after = time.time();

            assert after - now > .2, ("Not pausing correctly in end_move -- review instructions carefully -- execution took " + str(after - now) + " seconds");
            clear();
            print("Execution of single function should take between .2 and .25 seconds at most.\nYour execution took ", str(after-now));
            print("");

            print("Test complete");
            board = make_board(N);      #Clears the board

main();




#End of fourth section
