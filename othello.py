'''
The othello module is used to play the board game Othello, also known as Reversi. 
It is the final project for CS5001 at Northeastern University. To play, simply run the 
file.

Author: Evan Douglass
'''
import turtle

#### Module constants and global variables ####
SQUARE = 50                 # pixels - The size of one square on the board.
DIAMETER = SQUARE - 10      # pixels - The diameter of a single tile.
SCORES = "./scores.txt"     # A file to track player scores.

window = turtle.Screen()    # Graphics window
othello = turtle.Turtle()   # A pen to draw in the window

#### Classes ####
class GameBoard:
    '''
    The GameBoard class represents a board for the game Othello. It also 
    contains the functionality and logic allowing for gameplay, including
    a simple computer player AI.
    '''
    ## SIGNATURE
    # __init__ :: (Object, Integer) => Void
    def __init__(self, n):
        '''
        Draws the starting board and sets up gameplay.
        int n -- The number of squares on one side of the board (it's length
            in squares).
        '''
        assert type(n) == int, "n must be an integer."
        assert n >= 4, "n must be greater than or equal to 4."
        assert n % 2 != 1, "n must be even."
        
        self.n = n
        self.size = SQUARE * n      # The size of one side of the board in pixels
        self.turn = "black"         # The user will go first and is assigned the black pieces

        # Game state tracking attributes
        self.pieces = [None for location in range(n*n)]
        self.black = 0
        self.white = 0
        start = -n * SQUARE // 2     # The x & y coordinate of the first square
        self.squares = self.init_squares(start)

        # Draw the empty board
        self.draw_board()

        # Draw the starting tiles 
        self.draw_start_tiles()

        # Display turn
        self.announce_turn()

        # Find first valid moves
        self.valid_moves = self.find_valid_moves()

        # Set up mouse click event listener
        window.onclick(self.play)

    ## SIGNATURE
    # play :: (Object, Integer, Integer) => Void
    def play(self, x, y):
        '''
        This method drives the game. It waits for a user's mouse click to occur and 
        if the click is in a valid location, it places a black tile in that square.
        Before terminating, it also drives the computer's turn and checks if the
        game is over.
        int x -- The mouse x position
        int y -- The mouse y position 
        '''
        # Temporarily disable further clicks
        window.onclick(None)

        # Execute move
        for square in self.squares:
            # Search each square on the board for a click and make a play
            # where there was one, or do nothing if no valid tile was clicked.
            if square.was_clicked(x, y) and (square.location in self.valid_moves):
                self.make_move(square.location)
                break
        
        # This test is used for games that end with a full board.
        if board.is_full():
            self.end_game()
            # change turn so below block will not execute
            self.turn = "black"
        
        # If the user made a valid move, it's the computer's turn.
        if self.turn == "white":
            
            # True if the computer made a move, False otherwise
            comp_moved = self.computer_move()

            # If the user has no moves after the computer goes,
            # the computer will recursively continue to play until
            # either the user has a move or neither have a move.
            # If the computer made all of the moves that it could 
            # (including none), and the user still cannot go, the 
            # game is over.
            if not comp_moved and len(self.valid_moves) == 0:
                self.end_game()
        
        # Reactivate clicks
        window.onclick(self.play)
    
    ## SIGNATURE
    # computer_move :: Object => Boolean
    def computer_move(self):
        '''
        Contains the logic for the computer player's move during a game.
        Returns True if a move was made, or False if there were no legal moves.
        '''
        # Choose a move if possible (-1 if not)
        choice = self.choose_move()

        # There was a move:
        if choice != -1:
            # Draw tile and update game state for user
            self.make_move(choice)

            num_possible_user_moves = len(self.valid_moves)

            # If board is full, end the game.
            if self.is_full():
                self.end_game()

            # If the board is not full, but the user has no moves, computer
            # goes again.
            elif num_possible_user_moves == 0:
                self.switch_turns()  # back to computer
                self.valid_moves = self.find_valid_moves()
                self.announce_turn()
                return self.computer_move()
            
            return True
        
        # If there are no valid moves, return to user's turn
        else:
            self.switch_turns()
            self.valid_moves = self.find_valid_moves()
            self.announce_turn()
            return False

    ## SIGNATURE
    # choose_move :: Object => Integer
    def choose_move(self):
        '''
        This function is used by the computer player to decide what move to 
        make. It searches for the valid move that will capture the most tiles.
        It returns an integer representing the location of a square, or -1 if
        no valid move exists.
        '''
        keys = self.valid_moves.keys()

        key = -1
        length = 0
        for k in keys:
            l = len(self.valid_moves[k])
            if l > length:
                length = l
                key = k
        return key

    ## SIGNATURE
    # make_move :: (Object, Integer) => Void
    def make_move(self, location):
        '''
        Executes the actions necessary to make a move after a choice of tile
        location has been made.
        int location -- The index location of the square where the tile 
            will go.
        '''
        assert type(location) == int and 0 <= location < self.n**2, \
            "location must be a valid board index"

        # Put a tile in the square
        self.place(location)

        # Flip captured tiles
        to_flip = self.valid_moves[location]
        self.flip_tiles(to_flip)

        # Determine valid moves for next player
        self.switch_turns()
        self.valid_moves = self.find_valid_moves()
        self.announce_turn()
    
    ## SIGNATURE
    # place :: (Object, Integer) => Void
    def place(self, location):
        '''
        Initializes and draws a Gamepiece object on the Othello board at the given 
        location and with the given color. Also updates the number of tiles
        on the board.
        int location -- An index representing a square on the board, 0 to (n*n)-1.
        '''
        assert type(location) == int, "location must be an integer"
        assert 0 <= location < self.n**2, \
            "location must be within the size of the board"

        # Get center coordinates of the square
        x, y = self.squares[location].calc_center()

        # Draw a new tile in the square
        piece = GamePiece(location, self.turn, x, y)
        piece.draw_tile()

        # Track the new tile
        self.pieces[location] = piece
        if self.turn == "white":
            self.white += 1
        elif self.turn == "black":
            self.black += 1

    ## SIGNATURE
    # find_valid_moves :: Object => {Integer: Integer[]}
    def find_valid_moves(self):
        '''
        Determines which squares are valid moves based on the current state of 
        the game and which tiles can be captured from each square.
        '''
        moves = {}
        for square in self.squares:
            # Find the tiles that could be flipped from there
            can_capture = self.all_can_capture(square.location)

            # The list is not empty:
            if can_capture:
                # Add list of tiles to dictionary
                moves[square.location] = can_capture

        return moves

    ## SIGNATURE
    # all_can_capture :: (Object, Integer) => Integer[]
    def all_can_capture(self, location):
        '''
        Finds all of the tiles that can be captured from the given location.
        int location -- An integer identifying a square on the board.
        Returns a list of integer index locations.
        '''
        assert type(location) == int and 0 <= location < self.n**2, \
            "location must be a valid board index"

        square = self.squares[location]

        # The square is not empty:
        if not square.is_empty(self.pieces):
            # Return an empty list, not a valid move.
            return []

        # The square is empty:
        else:
            captured = []

            # Check in each direction around the square
            for direction in ("n", "ne", "e", "se", "s", "sw", "w", "nw"):

                # Find the locations of tiles that can be captured
                captured_in_direction = self.can_capture_in_direction(location, direction)
                # Add them to the total captured
                captured += captured_in_direction
            
            return captured

    ## SIGNATURE
    # can_capture_in_direction :: (Object, Integer, String) => Integer[]
    def can_capture_in_direction(self, location, direction):
        '''
        Finds tiles that can be captured from the given location in the given direction.
        int location -- An integer identifying a square on the board.
        str direction -- The direction to look in. Can be one of:
            n, ne, e, se, s, sw, w, nw
        Returns a list of integer index locations.
        '''
        assert type(location) == int and 0 <= location < self.n**2,\
            "location must be a valid board index"
        assert direction in ("n", "ne", "e", "se", "s", "sw", "w", "nw"),\
            "direction must be one of n, ne, e, se, s, sw, w, nw"

        captured = []

        # Set an increment based on direction
        # inc can be negative or positive
        inc = self.set_increment(direction)

        # Set a max/min value to bound movement
        end = self.set_max_min(location, direction)

        # Ensure the stop in range includes end
        if inc <= 0:
            end -= 1
        else:
            end += 1

        # Get first potential opponent location
        start = location + inc

        # While the next location is not above/below max/min
        for loc in range(start, end, inc):
            piece = self.pieces[loc]

            # There isn't a piece there:
            if piece == None:
                # Return empty list because nothing can be captured 
                return []

            # The next location has an opponent's tile:
            elif piece.color != self.turn:
                captured.append(piece)

            # The next location has own tile:
            elif piece.color == self.turn:
                captured.append(piece)
                break

            loc += inc
        
        # The loop can append opponent tiles that can't be captured it it
        # reaches the end of the board and only encountered opponent tiles.
        # A final test is needed to ensure the last tile belongs to the 
        # current player
        if len(captured) > 0 and captured[-1].color == self.turn:
            # remove own tile as a captured tile before returning
            return captured[:-1]
        else:
            return []

    ## SIGNATURE
    # set_increment :: (Object, String) => Integer
    def set_increment(self, direction):
        '''
        Determines an appropriate increment for moving from one square 
        location to the next in the given direction.
        str direction -- The direction to look in. Can be one of:
            n, ne, e, se, s, sw, w, nw
        Returns an integer
        '''
        assert direction in ("n", "ne", "e", "se", "s", "sw", "w", "nw"), \
            "direction must be one of n, ne, e, se, s, sw, w, nw"

        # Sample board layout (self.n = 2):
        # +---+---+
        # | 2 | 3 |
        # +---+---+
        # | 0 | 1 |
        # +---+---+
        if direction == "n":
            inc = self.n
        elif direction == "s":
            inc = -self.n
        elif direction == "e":
            inc = 1
        elif direction == "w":
            inc = -1
        elif direction == "ne":
            inc = self.n + 1
        elif direction == "nw":
            inc = self.n - 1
        elif direction == "se":
            inc = -(self.n - 1)
        elif direction == "sw":
            inc = -(self.n + 1)

        return inc

    ## SIGNATURE
    # set_max_min :: (Object, Integer, String) => (String, Integer)
    def set_max_min(self, location, direction):
        '''
        For the given location, determines the maximum or minimum index 
        location along the given direction that is still on the board.       
        int location -- An integer identifying a square on the board.
        Returns the min or max square location along direction that is 
            still on the board.
        '''
        assert type(location) == int and 0 <= location < self.n**2,\
            "location must be a valid board index"
        assert direction in ("n", "ne", "e", "se", "s", "sw", "w", "nw"),\
            "direction must be one of n, ne, e, se, s, sw, w, nw"

        row_num = location // self.n    # from 0 to self.n-1
        row_start = row_num * self.n    # first index in row
        max_steps = self.n - 1          # squares from first-in-row to last-in-row
        row_end = row_start + max_steps # last index in row
        board_max = self.n**2 - 1       # maximum index on board
        board_min = 0                   # lowest index on board

        # Instead of using a single variable for all conditions I've 
        # used two, a max and min, because it helps make clear
        # which direction the iteration will have to go for each case.
        # A conditional statement determines which is returned.
        mx = None
        mn = None

        # Moving straight up
        if direction == "n":
            mx = board_max

        # Moving straight down
        elif direction == "s":
            mn = board_min

        # Moving right
        elif direction == "e":
            # max = max in row
            mx = row_end
        
        # Moving left
        elif direction == "w":
            # min = first in row
            mn = row_start

        # Moving up-right
        elif direction == "ne":
            # Viewed as a 2D grid, the number of steps to get to the right
            # edge is also the number of steps to take up from the edge.
            # For some squares, the limit needs to be before the last, 
            # upper-right square.
            steps = max_steps - (location % self.n)
            mx = row_end + (steps * self.n)

            # For others, this is over the max board index
            if mx > board_max:
                mx = board_max

        # Moving down-right
        elif direction == "se":
            # Same logic as northeast, but downwards
            steps = max_steps - (location % self.n)
            mn = row_end - (steps * self.n)
            if mn < board_min:
                mn = board_min
        
        # Moving up-left
        elif direction == "nw":
            # nw and sw use the same logic as last set, but backwards
            steps = location - row_start
            mx = row_start + (steps * self.n)
            if mx > board_max:
                mx = board_max
        
        # Moving down-left
        elif direction == "sw":
            steps = location - row_start
            mn = row_start - (steps * self.n)
            if mn < board_min:
                mn = board_min

        # Return max or min?
        if mx == None:
            return mn
        else:
            return mx

    ## SIGNATURE
    # flip_tiles :: (Object, Integer[]) => Void
    def flip_tiles(self, tile_list):
        '''
        Drives the flipping of opponent tiles after a move is made.
        int[] tile_list -- A list of all the locations of tiles to be flipped.
        '''
        for tile in tile_list:
            self.flip_tile(tile.location)

    ## SIGNATURE
    # flip_tile :: (Object, Integer) = > Void
    def flip_tile(self, location):
        '''
        Changes the color of a single tile on the board and redraws it. Also
        tracks resulting changes to the board state.
        int location -- The location of the tile to be flipped.
        '''
        assert type(location) == int and 0 <= location < self.n**2,\
            "location must be a valid board index"

        piece = self.pieces[location]
        square = self.squares[location]

        # The square in location is not empty:
        if not square.is_empty(self.pieces):
            # Change the color of the piece
            piece.flip()

        # Increment/decrement self.black & self.white as needed.
        color = piece.color
        if color == "white":
            self.white += 1
            self.black -= 1
        elif color == "black":
            self.black += 1
            self.white -= 1

    ## SIGNATURE
    # switch_turns :: Object => Void
    def switch_turns(self):
        '''
        Changes the turn from black to white or white to black.
        '''
        if self.turn == "white":
            self.turn = "black"
        elif self.turn == "black":
            self.turn = "white"
    
    ## SIGNATURE
    # is_full :: Object => Boolean
    def is_full(self):
        '''
        Tests whether the board is full of tiles or not.
        Returns a boolean value.
        '''
        full = True
        for tile in self.pieces:
            # If any tile is None, the board is not full
            if tile == None:
                full = False
                break
        return full
    
    ## SIGNATURE
    # find_winner :: Object => (String, String)
    def find_winner(self):
        '''
        Calculates the winner based on the number of black and white tiles
        on the board.
        Returns two strings, the first announces the winner, the second 
            gives the score.
        '''
        # Determine message to display
        if self.white > self.black:
            message = "White wins!"
        elif self.black > self.white:
            message = "Black wins!"
        else:
            message = "You tied!"
        
        score = "black: " + str(self.black) + ", white: " + str(self.white)

        return message, score

    ## SIGNATURE
    # end_game :: Object => Void
    def end_game(self):
        '''
        Announces a winner and saves user's name in a high scores file.
        '''
        self.announce_winner()

        # Make a pop up window to collect user's name
        name = window.textinput("Name", "Enter your name to save your score:")

        # Only save name if the user gives one:
        if name != "" and name != None:
            self.save_score(name, SCORES)
    
    ## SIGNATURE
    # save_score :: (Object, String, String) => Void
    def save_score(self, name, path):
        '''
        Save the user's score to a text file with the given path. The 
        highest score is saved at the top of the file; the rest is
        ordered as played.
        str name -- A name given by the user.
        str path -- A path to the scores file.
        '''
        assert type(name) == str, "name must be a string"
        assert type(path) == str, "path must be a string"

        try:
            scores = open(path, "r+")

            # Read first line and make a list of [<name>, <score>]
            # This will be the current high score
            high_score = scores.readline().strip().split()

            # Write any new high scores at the top of the file:
            if self.black > int(high_score[1]):

                # Reset position to beginning and read whole file.
                scores.seek(0, 0)
                rest = scores.read()

                # Reset position again and write scores
                scores.seek(0, 0)
                scores.write(name + " " + str(self.black) + "\n")
                scores.write(rest)

            # Not a new high score:
            else:
                scores.write(name + " " + str(self.black) + "\n")
            
            scores.close()
        
        # If the file doesn't exist, create a new one and make the first entry
        except FileNotFoundError:
            scores = open(path, "w")
            scores.write(name + " " + str(self.black) + "\n")
            scores.close()

    ## SIGNATURE
    # init_squares :: (Object, Integer) => Object
    def init_squares(self, corner):
        '''
        Populates the self.squares list.
        int corner -- A number representing the x & y coordinate of the 
            first square.
        Returns a list of Square objects
        '''
        assert type(corner) == int, "corner must be an integer"

        lst = []
        index = 0

        # y-coordinates can continuously increase
        y_corner = corner
        for row in range(self.n):

            # x-coordinate values need to start over on each row
            x_corner = corner
            for column in range(self.n):

                # Add a square to the tracker list and increment values
                lst.append(Square(index, x_corner, y_corner))
                index += 1
                x_corner += SQUARE

            y_corner += SQUARE
        
        return lst
    
    ## SIGNATURE
    # find_center_squares :: Object => Integer[]
    def find_center_squares(self):
        '''
        Finds the four center starting squares on the board.
        Returns a tuple of ints representing the indexes of the four center 
            squares on the draw_board.
        '''
        # If n is even and the board grid is indexed from 0 to n*n,
        # then the upper right center square can be found with the formula:
        # 0.5(n**2 + n)
        # The remaining squares can be found by subtracting from that result
        # 1, n, n+1 for upper left, lower right, and lower left respectively
        ur = int(0.5 * (self.n**2 + self.n))
        ul = ur - 1
        lr = ur - self.n
        ll = lr - 1
        # Positioned in an order to make drawing the start pieces simpler,
        # see draw_start_tiles.
        return (ul, ur, lr, ll)

    ## SIGNATURE
    # draw_board :: Object => Void
    def draw_board(self):
        '''
        Draws an Othello board with a green background.
        '''
        # Setup window
        window.setup(self.size + SQUARE, self.size + SQUARE)
        window.screensize(self.size, self.size)
        window.bgcolor("white")
        window.title("Othello")

        # Create turtle to draw the board
        othello.penup()
        othello.speed(0)
        othello.hideturtle()

        # Line color is black, fill color is green
        othello.color("black", "forest green")

        # Move the turtle to the lower left corner
        corner = -self.n * SQUARE // 2
        othello.setposition(corner, corner)

        # Draw the green background
        othello.begin_fill()
        for i in range(4):
            othello.pendown()
            othello.forward(SQUARE * self.n)
            othello.left(90)
        othello.end_fill()

        # Draw the horizontal lines
        for i in range(self.n + 1):
            othello.setposition(corner, SQUARE * i + corner)
            self.draw_line()

        # Draw the vertical lines
        othello.left(90)
        for i in range(self.n + 1):
            othello.setposition(SQUARE * i + corner, corner)
            self.draw_line()

    ## SIGNATURE
    # draw_line :: Object => Void
    def draw_line(self):
        '''
        Draws a line. this is a helper function for draw_board.
        '''
        othello.pendown()
        othello.forward(SQUARE * self.n)
        othello.penup()

    ## SIGNATURE
    # draw_start_tiles :: Object => Void
    def draw_start_tiles(self):
        '''
        Draws the four starting tiles on the board.
        '''
        start_tiles = self.find_center_squares()
        for location in start_tiles:
            self.place(location)
            self.switch_turns()

    ## SIGNATURE
    # draw_box :: Object => Void
    def draw_box(self):
        '''
        Draws a black box used to display the end-of-game text.
        '''
        # Box will cover the middle two rows across the whole window
        start_x = -self.size//2 - SQUARE//2
        start_y = -SQUARE
        width = self.size + SQUARE
        height = 2 * SQUARE

        # Set start
        othello.penup()
        othello.goto(start_x, start_y)
        othello.setheading(0)    # Move right first
        othello.pendown()

        # Draw
        othello.color("white", "#202020")    # Background is light black
        othello.begin_fill()
        for half in range(2):
            othello.forward(width)
            othello.left(90)
            othello.forward(height)
            othello.left(90)
        othello.end_fill()

    ## SIGNATURE
    # announce_winner :: Object => Void
    def announce_winner(self):
        '''
        Determines and announces the winner of the current game to the user.
        '''
        message, score = self.find_winner()

        # Display textbox
        self.draw_box()
        
        # Display message
        othello.penup()
        othello.home()
        othello.color("white")
        othello.pendown()
        othello.write(message, align="center", font=("Georgia", 25, "bold", "underline"))
        print(message)

        # Display score
        othello.penup()
        othello.goto(0, -SQUARE//2)
        othello.pendown()
        othello.write(score, align="center", font=("Georgia", 16, "bold"))
        print(score)

    ## SIGNATURE
    # announce_turn :: Object => Void
    def announce_turn(self):
        '''
        Displays whose turn it is at the top of the board.
        '''
        message = self.turn + "'s turn"

        ## Draw white box around old text
        # Setup
        othello.penup()
        othello.goto(-SQUARE, (self.size//2 + 1))  # +1 => avoids writing over board outline
        othello.pendown()
        othello.color("white", "white")
        othello.setheading(0)
        # Start drawing
        othello.begin_fill()
        for half in range(2):
            othello.forward(2 * SQUARE)
            othello.left(90)
            othello.forward(SQUARE//2 - 1)
            othello.left(90)
        othello.end_fill()

        ## Display the text
        othello.penup()
        othello.goto(0, self.size // 2)    # Middle-top of the board
        othello.color("black")
        othello.pendown()
        othello.write(message, align="center", font=("Georgia"))



class Square:
    '''
    Represents a single square on the Othello board.
    '''

    def __init__(self, location, x, y):
        '''
        int location -- An index representing the assigned number on the board
        of this square.
        int x -- The lower left x-coordinate of the square.
        int y -- The lower left y-coordinate of the square.
        Attributes representing the length of a side (size) and the center
            coordinates (center) of the square are also initialized.
        '''
        assert type(location) == int and location >= 0, \
            "location must be a non-negative integer"
        assert type(x) == int and type(y) == int, \
            "x & y must be integers"
        
        self.location = location
        self.x = x
        self.y = y
        self.size = SQUARE
        self.center = self.calc_center()

    ## SIGNATURE
    # calc_center :: Object => Integer[]
    def calc_center(self):
        '''
        Finds the coordinates of the square's center.
        Returns a tuple containing the coordinates.
        '''
        half = self.size // 2
        x = self.x + self.size - half
        y = self.y + self.size - half

        return (x, y)

    ## SIGNATURE
    # was_clicked :: (Object, Integer, Integer) => Boolean
    def was_clicked(self, x, y):
        '''
        Determines if this square was clicked on by the user.
        int x -- The x-coordinate of a mouse click.
        int y -- The y-coordinate of a mouse click.
        Returns a boolean value.
        '''
        inside = False
        if ((self.x < x < self.x + self.size)
                and (self.y < y < self.y + self.size)):
            inside = True

        return inside

    ## SIGNATURE
    # is_empty :: Object => Boolean
    def is_empty(self, state):
        '''
        Tests if the square contains a tile
        GamePiece[] state -- A list of GamePiece objects representing the 
            current board layout.
        Returns a boolean value.
        '''
        if state[self.location] == None:
            return True
        return False


class GamePiece:
    '''
    GamePiece represents a single piece, or tile, in Othello.
    '''

    def __init__(self, location, color, center_x, center_y):
        '''
        int location -- An index cooresponding to the square that this piece is placed in.
        str color -- The color of the piece. Either white or black.
        int center_x -- The x-coordinate of the piece's center.
        int center_y -- The y-coordinate of the piece's center.
        '''
        assert type(location) == int and location >= 0,\
            "location must be a non-negative integer"
        assert color == "black" or color == "white",\
            "color must be 'black' or 'white'"
        assert type(center_x) == int and type(center_y) == int,\
            "x & y values must be integers"

        self.location = location
        self.color = color
        self.x = center_x
        self.y = center_y

    ## SIGNATURE
    # draw_tile :: Object => Void
    def draw_tile(self):
        '''
        Draws an Othello piece on the game board using the global Turtle object.
        str color -- The color of the piece being placed.
        '''
        othello.penup()
        othello.goto(self.x, self.y)
        othello.pendown()
        othello.dot(DIAMETER, self.color)

    ## SIGNATURE
    # change_color :: Object => Void
    def change_color(self):
        '''
        Changes the object's color from black to white, or 
        from white to black.
        '''
        if self.color == "white": 
            self.color = "black"
        elif self.color == "black":
            self.color = "white"

    ## SIGNATURE
    # flip :: Object => Void
    # This method not used in part 1 and not in testing.txt
    def flip(self):
        '''
        Redraws a tile with a new color.
        '''
        self.change_color()
        self.draw_tile()

    ## SIGNATURE
    # __repr__ :: Object => String
    def __repr__(self):
        '''
        A string representation of this object. Made to help in debugging.
        '''
        return self.color + " @ " + str(self.location)


#### Start Game ####
if __name__ == "__main__":
    board = GameBoard(8)
    turtle.done()
