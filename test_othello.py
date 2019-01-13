'''
This is a test module for the Othello program. It removes the automatic graphic
components so unit testing is more easily accomplished.

I recommend commenting out the global window and othello variables
in othello.py before running tests in order to prevent a graphics window 
from popping up.

Author: Evan Douglass
'''
import pytest as pt
import othello as o

#### Module constants and global variables ####
SQUARE = 50             # pixels
RADIUS = SQUARE - 10    # pixels

class GameBoardTest(o.GameBoard):
    '''Same as GameBoard but does not draw graphics when initialized.'''

    def __init__(self, n):
        '''
        Sets up gameplay. The exact same implementation as the GameBoard class __init__
        but without the graphic components.
        int n -- The number of squares on one side of the board (it's length
        in squares).
        '''
        assert type(n) == int, "n must be an integer."
        assert n >= 4, "n must be greater than or equal to 4."
        assert n % 2 != 1, "n must be even."
        self.n = n

        self.size = SQUARE * n
        self.turn = "black"         # The user will go first and is assigned the black pieces

        # Game state tracking attributes
        self.pieces = [None for location in range(n*n)]
        self.black = 0
        self.white = 0
        start = -n * SQUARE // 2     # The x & y coordinate of the first square
        self.squares = self.init_squares(start)
        self.valid_moves = self.find_valid_moves()

        # Graphic components start here and are omitted

########## GameBoard Class Tests ##########

def test_invalid_inits():
    # Start by testing invalid inputs. These will raise AttributeErrors. See 
    # assertions for specific text the exception will display.
    # See https://docs.pytest.org/en/latest/assert.html for info on testing 
    # exception handling.

    # Test non-integer inputs
    with pt.raises(AssertionError) as string:
        GameBoardTest("hello")
    with pt.raises(AssertionError) as lst:
        GameBoardTest([1, 2, 3, 4])
    with pt.raises(AssertionError) as floating:
        GameBoardTest(9.5)

    assert "n must be an integer." in str(string.value)
    assert "n must be an integer." in str(lst.value)
    assert "n must be an integer." in str(floating.value)

    # Test integers less than 4
    with pt.raises(AssertionError) as one:
        # Odd
        GameBoardTest(1)
    with pt.raises(AssertionError) as negative:
        # Negative
        GameBoardTest(-45)
    with pt.raises(AssertionError) as two:
        # Even
        GameBoardTest(2)

    assert "n must be greater than or equal to 4." in str(one.value)
    assert "n must be greater than or equal to 4." in str(negative.value)
    assert "n must be greater than or equal to 4." in str(two.value)

    # Test odd integers greater than 4
    with pt.raises(AssertionError) as odd_9:
        GameBoardTest(9)
    with pt.raises(AssertionError) as odd_23:
        GameBoardTest(23)

    assert "n must be even." in str(odd_9.value)
    assert "n must be even." in str(odd_23.value)


# Valid inits
four = GameBoardTest(4)
six = GameBoardTest(6)
eight = GameBoardTest(8)


def test_init():
    # Test for correct attribute assignments
    # Note that squares list tests are in test_init_squares

    # Tests for 4x4 board
    assert four.n == 4
    assert four.size == 200
    assert four.turn == "black"
    assert four.black == 0
    assert four.white == 0
    assert len(four.pieces) == 16
    assert all(four.pieces) == False  # Every value is None
    
    # Tests for 6x6 board
    assert six.n == 6
    assert six.size == 300
    assert six.turn == "black"
    assert six.black == 0
    assert six.white == 0
    assert len(six.pieces) == 36
    assert all(six.pieces) == False  # Every value is None

    # Tests for 8x8 board
    assert eight.n == 8
    assert eight.size == 400
    assert eight.turn == "black"
    assert eight.black == 0
    assert eight.white == 0
    assert len(eight.pieces) == 64
    assert all(eight.pieces) == False  # Every value is None


def test_init_squares():
    # This function also indirectly tests the Squares.__init__ method

    # Test invalid values first
    with pt.raises(AssertionError) as string:
        four.init_squares("Hello")
    with pt.raises(AssertionError) as lst:
        four.init_squares(["h", 3, 6.8])
    with pt.raises(AssertionError) as flt:
        four.init_squares(4.5)
    assert "corner must be an integer" in str(string.value)
    assert "corner must be an integer" in str(lst.value)
    assert "corner must be an integer" in str(flt.value)

    # Function for testing squares' index values
    def squares_are_correct_index_values(board_object):
        # Squares have location value according to their place on the board,
        # which is assigned by list index
        for index, square in enumerate(board_object.squares):
            if square.location != index:
                return False
        return True

    # Function for testing correct x increments (50)
    def squares_increment_x_correctly(board_object):
        x = y = (-board_object.n * SQUARE) // 2         # Same definition as is in the class for the start (x, y)
        # Checks the first row of the board to make
        # sure x increments by 50
        for index in range(board_object.n):
            square = board_object.squares[index]
            if square.x != x or square.y != y:          # y remains constant
                return False
            x += 50
        return True
    
    # Function for testing correct y increments (50)
    def squares_increment_y_correctly(board_object):
        y = x = (-board_object.n * SQUARE) // 2                 # Same definition as is in the class for the start (x, y)
        # Checks the first row of the board to make sure
        # x increments by 50
        for index in range(0, board_object.n, board_object.n):  # Increment by n to get 1st column
            square = board_object.squares[index]
            if square.y != y or square.x != x:                  # x remains constant
                return False
            y += 50
        return True
    
    # Test Square.location values
    assert squares_are_correct_index_values(four)
    assert squares_are_correct_index_values(six)
    assert squares_are_correct_index_values(eight)

    # Test starting square location
    assert four.squares[0].x == -100 and four.squares[0].y == -100
    assert six.squares[0].x == -150 and six.squares[0].y == -150
    assert eight.squares[0].x == -200 and eight.squares[0].y == -200

    # Test last square location
    assert four.squares[-1].x == 50 and four.squares[-1].y == 50
    assert six.squares[-1].x == 100 and six.squares[-1].y == 100
    assert eight.squares[-1].x == 150 and eight.squares[-1].y == 150

    # Test x value increments
    assert squares_increment_x_correctly(four)
    assert squares_increment_x_correctly(six)
    assert squares_increment_x_correctly(eight)

    # Test y value increments
    assert squares_increment_y_correctly(four)
    assert squares_increment_y_correctly(six)
    assert squares_increment_y_correctly(eight)


def test_switch_turns():
    # turn starts with black
    four.switch_turns()
    assert four.turn == "white"
    four.switch_turns()
    assert four.turn == "black"


def test_find_center_squares():
    # This functions uses self.n to calculate the center squares.
    # It only works when self.n is an even number.
    # As shown above, the GameBoard class can only be initialized with
    # a positive even integer greater than 3. Therefore, only the valid
    # test objects defined earlier are used as tests here.
    # Note: the order that the squares are returned is clockwise from
    # top left.

    assert four.find_center_squares() == (9, 10, 6, 5)
    assert six.find_center_squares() == (20, 21, 15, 14)
    assert eight.find_center_squares() == (35, 36, 28, 27)


def test_place_argument_validity():
    # place only calls other functions, so it's validity is best tested
    # by testing those other functions. However, it takes one argument
    # that must be a positive integer between -1 and n**2 exclusive, which can be
    # tested.

    with pt.raises(AssertionError) as string:
        four.place("Hello")
    with pt.raises(AssertionError) as lst:
        four.place(["h", 3, 6.8])
    with pt.raises(AssertionError) as negative:
        four.place(-1)
    with pt.raises(AssertionError) as too_big:
        four.place(16)  # Last index should be one less than n**2
    
    assert "location must be an integer" in str(string.value)
    assert "location must be an integer" in str(lst.value)
    assert "location must be within the size of the board" in str(negative.value)
    assert "location must be within the size of the board" in str(too_big.value)


def test_is_full():
    # Operates on GameBoard.pieces list. is_full does not test if there are
    # values in GameBoard.pieces that are not GamePiece objects. Thus, a list
    # of integers could potentially evaluate to True. This is a short coming,
    # but I also do not expect anything other than GamePieces to be added to
    # the list since game-play is only accomplished via clicks on a GUI.

    # Only the starting tiles are on the board currently
    assert four.is_full() == False

    # Test Squares
    one = o.Square(0, 25, 25)
    two = o.Square(1, 75, 75)
    three = o.Square(2, 25, 75)
    _four = o.Square(3, 75, 25)     # underscore is due to the GameBoard four
    full = [one, two, three, _four]

    four.pieces = full
    assert four.is_full() == True

    # Delete one, test again
    not_full = [one, two, three, None]
    four.pieces = not_full
    assert four.is_full() == False


def test_find_winner():

    # Tie
    four.black = 5
    four.white = 5
    message, score = four.find_winner()
    assert message == "You tied!"
    assert score == "black: 5, white: 5"

    # Black wins
    four.black = 6
    four.white = 3
    message, score = four.find_winner()
    assert message == "Black wins!"
    assert score == "black: 6, white: 3"

    # White wins
    four.black = 2
    four.white = 10
    message, score = four.find_winner()
    assert message == "White wins!"
    assert score == "black: 2, white: 10"


def test_set_increment():
    # Takes a string in (n, ne, e, se, s, sw, w, nw) and returns a specific
    # increment value for traversing the board by index in that direction.

    # Test invalid input
    with pt.raises(AssertionError) as not_valid:
        four.set_increment("Northeast")
    assert "direction must be one of n, ne, e, se, s, sw, w, nw" in str(not_valid.value)

    # Test valid inputs
    assert four.set_increment("n") == 4
    assert six.set_increment("n") == 6
    assert eight.set_increment("n") == 8

    assert four.set_increment("ne") == 5
    assert six.set_increment("ne") == 7
    assert eight.set_increment("ne") == 9

    assert four.set_increment("e") == 1
    assert six.set_increment("e") == 1
    assert eight.set_increment("e") == 1

    assert four.set_increment("se") == -3
    assert six.set_increment("se") == -5
    assert eight.set_increment("se") == -7

    assert four.set_increment("s") == -4
    assert six.set_increment("s") == -6
    assert eight.set_increment("s") == -8

    assert four.set_increment("sw") == -5
    assert six.set_increment("sw") == -7
    assert eight.set_increment("sw") == -9

    assert four.set_increment("w") == -1
    assert six.set_increment("w") == -1
    assert eight.set_increment("w") == -1

    assert four.set_increment("nw") == 3
    assert six.set_increment("nw") == 5
    assert eight.set_increment("nw") == 7


def test_set_max_min():
    ### Test invalid input
    with pt.raises(AssertionError) as direction_not_valid:
        four.set_max_min(0, "Northeast")
    with pt.raises(AssertionError) as location_not_int:
        four.set_max_min("hello", "n")
    with pt.raises(AssertionError) as location_negative:
        four.set_max_min(-3, "n")
    with pt.raises(AssertionError) as location_too_big:
        four.set_max_min(16, "n")
    
    assert "direction must be one of n, ne, e, se, s, sw, w, nw" in str(direction_not_valid.value)
    assert "location must be a valid board index" in str(location_not_int.value)
    assert "location must be a valid board index" in str(location_negative.value)
    assert "location must be a valid board index" in str(location_too_big.value)

    ### Test valid inputs. Note that the board is a 2D n by n grid.
    ### The first test include the whole board as this is an important
    ### function. For larger boards, only a few indexes are tested
    ### to verify it still works with larger boards.
    ## 4x4 board
    # North
    assert four.set_max_min(0, "n") == 15
    assert four.set_max_min(1, "n") == 15
    assert four.set_max_min(2, "n") == 15
    assert four.set_max_min(3, "n") == 15
    assert four.set_max_min(4, "n") == 15
    assert four.set_max_min(5, "n") == 15
    assert four.set_max_min(6, "n") == 15
    assert four.set_max_min(7, "n") == 15
    assert four.set_max_min(8, "n") == 15
    assert four.set_max_min(9, "n") == 15
    assert four.set_max_min(10, "n") == 15
    assert four.set_max_min(11, "n") == 15
    assert four.set_max_min(12, "n") == 15
    assert four.set_max_min(13, "n") == 15
    assert four.set_max_min(14, "n") == 15
    assert four.set_max_min(15, "n") == 15

    # South
    assert four.set_max_min(0, "s") == 0
    assert four.set_max_min(1, "s") == 0
    assert four.set_max_min(2, "s") == 0
    assert four.set_max_min(3, "s") == 0
    assert four.set_max_min(4, "s") == 0
    assert four.set_max_min(5, "s") == 0
    assert four.set_max_min(6, "s") == 0
    assert four.set_max_min(7, "s") == 0
    assert four.set_max_min(8, "s") == 0
    assert four.set_max_min(9, "s") == 0
    assert four.set_max_min(10, "s") == 0
    assert four.set_max_min(11, "s") == 0
    assert four.set_max_min(12, "s") == 0
    assert four.set_max_min(13, "s") == 0
    assert four.set_max_min(14, "s") == 0
    assert four.set_max_min(15, "s") == 0

    # East
    assert four.set_max_min(0, "e") == 3
    assert four.set_max_min(1, "e") == 3
    assert four.set_max_min(2, "e") == 3
    assert four.set_max_min(3, "e") == 3
    assert four.set_max_min(4, "e") == 7
    assert four.set_max_min(5, "e") == 7
    assert four.set_max_min(6, "e") == 7
    assert four.set_max_min(7, "e") == 7
    assert four.set_max_min(8, "e") == 11
    assert four.set_max_min(9, "e") == 11
    assert four.set_max_min(10, "e") == 11
    assert four.set_max_min(11, "e") == 11
    assert four.set_max_min(12, "e") == 15
    assert four.set_max_min(13, "e") == 15
    assert four.set_max_min(14, "e") == 15
    assert four.set_max_min(15, "e") == 15

    # West
    assert four.set_max_min(0, "w") == 0
    assert four.set_max_min(1, "w") == 0
    assert four.set_max_min(2, "w") == 0
    assert four.set_max_min(3, "w") == 0
    assert four.set_max_min(4, "w") == 4
    assert four.set_max_min(5, "w") == 4
    assert four.set_max_min(6, "w") == 4
    assert four.set_max_min(7, "w") == 4
    assert four.set_max_min(8, "w") == 8
    assert four.set_max_min(9, "w") == 8
    assert four.set_max_min(10, "w") == 8
    assert four.set_max_min(11, "w") == 8
    assert four.set_max_min(12, "w") == 12
    assert four.set_max_min(13, "w") == 12
    assert four.set_max_min(14, "w") == 12
    assert four.set_max_min(15, "w") == 12

    # Northeast
    assert four.set_max_min(0, "ne") == 15
    assert four.set_max_min(1, "ne") == 11
    assert four.set_max_min(2, "ne") == 7
    assert four.set_max_min(3, "ne") == 3
    assert four.set_max_min(4, "ne") == 15
    assert four.set_max_min(5, "ne") == 15
    assert four.set_max_min(6, "ne") == 11
    assert four.set_max_min(7, "ne") == 7
    assert four.set_max_min(8, "ne") == 15
    assert four.set_max_min(9, "ne") == 15
    assert four.set_max_min(10, "ne") == 15
    assert four.set_max_min(11, "ne") == 11
    assert four.set_max_min(12, "ne") == 15
    assert four.set_max_min(13, "ne") == 15
    assert four.set_max_min(14, "ne") == 15
    assert four.set_max_min(15, "ne") == 15

    # Southeast
    assert four.set_max_min(0, "se") == 0
    assert four.set_max_min(1, "se") == 0
    assert four.set_max_min(2, "se") == 0
    assert four.set_max_min(3, "se") == 3
    assert four.set_max_min(4, "se") == 0
    assert four.set_max_min(5, "se") == 0
    assert four.set_max_min(6, "se") == 3
    assert four.set_max_min(7, "se") == 7
    assert four.set_max_min(8, "se") == 0
    assert four.set_max_min(9, "se") == 3
    assert four.set_max_min(10, "se") == 7
    assert four.set_max_min(11, "se") == 11
    assert four.set_max_min(12, "se") == 3
    assert four.set_max_min(13, "se") == 7
    assert four.set_max_min(14, "se") == 11
    assert four.set_max_min(15, "se") == 15

    # Northwest
    assert four.set_max_min(0, "nw") == 0
    assert four.set_max_min(1, "nw") == 4
    assert four.set_max_min(2, "nw") == 8
    assert four.set_max_min(3, "nw") == 12
    assert four.set_max_min(4, "nw") == 4
    assert four.set_max_min(5, "nw") == 8
    assert four.set_max_min(6, "nw") == 12
    assert four.set_max_min(7, "nw") == 15
    assert four.set_max_min(8, "nw") == 8
    assert four.set_max_min(9, "nw") == 12
    assert four.set_max_min(10, "nw") == 15
    assert four.set_max_min(11, "nw") == 15
    assert four.set_max_min(12, "nw") == 12
    assert four.set_max_min(13, "nw") == 15
    assert four.set_max_min(14, "nw") == 15
    assert four.set_max_min(15, "nw") == 15

    # Southwest
    assert four.set_max_min(0, "sw") == 0
    assert four.set_max_min(1, "sw") == 0
    assert four.set_max_min(2, "sw") == 0
    assert four.set_max_min(3, "sw") == 0
    assert four.set_max_min(4, "sw") == 4
    assert four.set_max_min(5, "sw") == 0
    assert four.set_max_min(6, "sw") == 0
    assert four.set_max_min(7, "sw") == 0
    assert four.set_max_min(8, "sw") == 8
    assert four.set_max_min(9, "sw") == 4
    assert four.set_max_min(10, "sw") == 0
    assert four.set_max_min(11, "sw") == 0
    assert four.set_max_min(12, "sw") == 12
    assert four.set_max_min(13, "sw") == 8
    assert four.set_max_min(14, "sw") == 4
    assert four.set_max_min(15, "sw") == 0

    ## 8x8 board
    # North
    assert eight.set_max_min(24, "n") == 63
    assert eight.set_max_min(27, "n") == 63
    assert eight.set_max_min(31, "n") == 63

    # South
    assert eight.set_max_min(24, "s") == 0
    assert eight.set_max_min(27, "s") == 0
    assert eight.set_max_min(31, "s") == 0

    # East
    assert eight.set_max_min(24, "e") == 31
    assert eight.set_max_min(27, "e") == 31
    assert eight.set_max_min(31, "e") == 31

    # West
    assert eight.set_max_min(24, "w") == 24
    assert eight.set_max_min(27, "w") == 24
    assert eight.set_max_min(31, "w") == 24

    # Northeast
    assert eight.set_max_min(24, "ne") == 63
    assert eight.set_max_min(27, "ne") == 63
    assert eight.set_max_min(31, "ne") == 31

    # Southeast
    assert eight.set_max_min(24, "se") == 0
    assert eight.set_max_min(27, "se") == 0
    assert eight.set_max_min(31, "se") == 31

    # Northwest
    assert eight.set_max_min(24, "nw") == 24
    assert eight.set_max_min(27, "nw") == 48
    assert eight.set_max_min(31, "nw") == 63

    # Southwest
    assert eight.set_max_min(24, "sw") == 24
    assert eight.set_max_min(27, "sw") == 0
    assert eight.set_max_min(31, "sw") == 0


# These GamePiece objects will be needed for the next tests
p_0 = o.GamePiece(0, "white", 25, 25)
p_1 = o.GamePiece(1, "white", 75, 25)
p_2 = o.GamePiece(2, "white", 125, 25)
p_3 = o.GamePiece(3, "white", 175, 25)
p_4 = o.GamePiece(4, "white", 25, 75)
p_5 = o.GamePiece(5, "white", 75, 75)
p_6 = o.GamePiece(6, "white", 125, 75)
p_7 = o.GamePiece(7, "white", 175, 75)
p_8 = o.GamePiece(8, "white", 25, 125)
p_9 = o.GamePiece(9, "white", 75, 125)
p_10 = o.GamePiece(10, "white", 125, 125)
p_11 = o.GamePiece(11, "white", 175, 125)
p_12 = o.GamePiece(12, "white", 25, 175)
p_13 = o.GamePiece(13, "white", 75, 175)
p_14 = o.GamePiece(14, "white", 125, 175)
p_15 = o.GamePiece(15, "white", 175, 175)


def test_can_capture_in_direction():
    ### Test invalid input
    with pt.raises(AssertionError) as direction_not_valid:
        four.can_capture_in_direction(0, "Northeast")
    with pt.raises(AssertionError) as location_not_int:
        four.can_capture_in_direction("hello", "n")
    with pt.raises(AssertionError) as location_negative:
        four.can_capture_in_direction(-3, "n")
    with pt.raises(AssertionError) as location_too_big:
        four.can_capture_in_direction(16, "n")
    
    assert "direction must be one of n, ne, e, se, s, sw, w, nw" in str(direction_not_valid.value)
    assert "location must be a valid board index" in str(location_not_int.value)
    assert "location must be a valid board index" in str(location_negative.value)
    assert "location must be a valid board index" in str(location_too_big.value)

    ### Test valid input
    ## These tests will alter the GameBoard.pieces list for the sake of simplicity
    ## East ##
    four.turn == "black"

    # All opponent tiles
    four.pieces = [None, p_1, p_2, p_3]
    assert four.can_capture_in_direction(0, "e") == []

    # Capture two
    p_3.change_color()
    assert four.can_capture_in_direction(0, "e") == [p_1, p_2]

    # Capture one
    p_2.change_color()
    assert four.can_capture_in_direction(0, "e") == [p_1]

    # Capture none
    p_1.change_color()
    assert four.can_capture_in_direction(0, "e") == []

    four.pieces = [None, None, None, None]
    assert four.can_capture_in_direction(0, "e") == []

    # Reset colors
    p_0.color = "white"
    p_1.color = "white"
    p_2.color = "white"
    p_3.color = "white"

    ## West ##
    ## Further tests will use the same basic sequence as above
    four.pieces = [p_0, p_1, p_2, None]
    assert four.can_capture_in_direction(3, "w") == []
    p_0.change_color() # black
    assert four.can_capture_in_direction(3, "w") == [p_2, p_1]
    p_1.change_color() # black
    assert four.can_capture_in_direction(3, "w") == [p_2]
    p_2.change_color() # black
    assert four.can_capture_in_direction(3, "w") == []
    four.pieces = [None, None, None, None]
    assert four.can_capture_in_direction(3, "w") == []

    # Reset colors
    p_0.color = "white"
    p_1.color = "white"
    p_2.color = "white"
    p_3.color = "white"

    ## North ##
    # Note that this board is inverted so 0 is top left, not bottom left
    four.pieces = [
        None, None, None, None,
        p_4, None, None, None,
        p_8, None, None, None,
        p_12, None, None, None,
    ]
    assert four.can_capture_in_direction(0, "n") == []
    p_12.change_color()  # black
    assert four.can_capture_in_direction(0, "n") == [p_4, p_8]
    p_8.change_color()   # black
    assert four.can_capture_in_direction(0, "n") == [p_4]
    p_4.change_color()   # black
    assert four.can_capture_in_direction(0, "n") == []
    four.pieces = [
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
    ]
    assert four.can_capture_in_direction(0, "n") == []

    # Reset colors
    p_0.color = "white"
    p_4.color = "white"
    p_8.color = "white"
    p_12.color = "white"

    ## South ##
    # Note that this board is inverted so 0 is top left, not bottom left
    four.pieces = [
        p_0, None, None, None,
        p_4, None, None, None,
        p_8, None, None, None,
        None, None, None, None,
    ]
    assert four.can_capture_in_direction(12, "s") == []
    p_0.change_color()  # black
    assert four.can_capture_in_direction(12, "s") == [p_8, p_4]
    p_4.change_color()   # black
    assert four.can_capture_in_direction(12, "s") == [p_8]
    p_8.change_color()   # black
    assert four.can_capture_in_direction(12, "s") == []
    four.pieces = [
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
    ]
    assert four.can_capture_in_direction(12, "s") == []

    # Reset colors
    p_0.color = "white"
    p_4.color = "white"
    p_8.color = "white"
    p_12.color = "white"

    ## Northeast ##
    # Note that this board is inverted so 0 is top left, not bottom left
    four.pieces = [
        None, None, None, None,
        None, p_5, None, None,
        None, None, p_10, None,
        None, None, None, p_15,
    ]
    assert four.can_capture_in_direction(0, "ne") == []
    p_15.change_color()  # black
    assert four.can_capture_in_direction(0, "ne") == [p_5, p_10]
    p_10.change_color()  # black
    assert four.can_capture_in_direction(0, "ne") == [p_5]
    p_5.change_color()   # black
    assert four.can_capture_in_direction(0, "ne") == []
    four.pieces = [
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
    ]
    assert four.can_capture_in_direction(0, "ne") == []

    # Reset colors
    p_0.color = "white"
    p_5.color = "white"
    p_10.color = "white"
    p_15.color = "white"

    ## Southeast ##
    four.pieces = [
        None, None, None, p_3,
        None, None, p_6, None,
        None, p_9, None, None,
        None, None, None, None,
    ]
    assert four.can_capture_in_direction(12, "se") == []
    p_3.change_color()
    assert four.can_capture_in_direction(12, "se") == [p_9, p_6]
    p_6.change_color()
    assert four.can_capture_in_direction(12, "se") == [p_9]
    p_9.change_color()
    assert four.can_capture_in_direction(12, "se") == []
    four.pieces = [
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
    ]
    assert four.can_capture_in_direction(12, "se") == []

    # Reset colors
    p_3.color = "white"
    p_6.color = "white"
    p_9.color = "white"
    p_12.color = "white"

    ## Northwest ##
    # Note that this board is inverted so 0 is top left, not bottom left
    four.pieces = [
        None, None, None, None,
        None, None, p_6, None,
        None, p_9, None, None,
        p_12, None, None, None,
    ]
    assert four.can_capture_in_direction(3, "nw") == []
    p_12.change_color()
    assert four.can_capture_in_direction(3, "nw") == [p_6, p_9]
    p_9.change_color()
    assert four.can_capture_in_direction(3, "nw") == [p_6]
    p_6.change_color()
    assert four.can_capture_in_direction(3, "nw") == []
    four.pieces = [
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
    ]
    assert four.can_capture_in_direction(3, "nw") == []

    # Reset colors
    p_3.color = "white"
    p_6.color = "white"
    p_9.color = "white"
    p_12.color = "white"

    ## Southwest ##
    # Note that this board is inverted so 0 is top left, not bottom left
    four.pieces = [
        p_0, None, None, None,
        None, p_5, None, None,
        None, None, p_10, None,
        None, None, None, None,
    ]
    assert four.can_capture_in_direction(15, "sw") == []
    p_0.color = "black"
    assert four.can_capture_in_direction(15, "sw") == [p_10, p_5]
    p_5.color = "black"
    assert four.can_capture_in_direction(15, "sw") == [p_10]
    p_10.color = "black"
    assert four.can_capture_in_direction(15, "sw") == []
    four.pieces = [
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
    ]
    assert four.can_capture_in_direction(15, "sw") == []

    # Reset colors
    p_0.color = "white"
    p_5.color = "white"
    p_10.color = "white"
    p_15.color = "white"


def test_all_can_capture():
    # Invalid entries
    with pt.raises(AssertionError) as location_not_int:
        four.all_can_capture("hello")
    with pt.raises(AssertionError) as location_negative:
        four.all_can_capture(-3)
    with pt.raises(AssertionError) as location_too_big:
        four.all_can_capture(16)

    assert "location must be a valid board index" in str(location_not_int.value)
    assert "location must be a valid board index" in str(location_negative.value)
    assert "location must be a valid board index" in str(location_too_big.value)

    # Valid entries

    four.turn = "black"
    # Empty board
    four.pieces = [
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
        None, None, None, None,
    ]
    for index in range(0, 16):
        assert four.all_can_capture(index) == []

    # Maximum Captured
    four.pieces = [
        None, p_1, p_2, p_3,
        p_4, p_5, None, None,
        p_8, None, p_10, None,
        p_12, None, None, p_15,
    ]
    p_12.color = "black"
    p_15.color = "black"
    p_3.color = "black"
    assert four.all_can_capture(0) == [p_4, p_8, p_5, p_10, p_1, p_2]

    p_3.color = "white"
    assert four.all_can_capture(0) == [p_4, p_8, p_5, p_10]

    p_2.color = "black"
    assert four.all_can_capture(0) == [p_4, p_8, p_5, p_10, p_1]

    p_2.color = "white"
    p_12.color = "white"
    p_15.color = "white"

    # The following board layout is 6x6
    six.pieces = [None for i in range(six.n**2)]

    for i in [0, 2, 4, 12, 17, 24, 32, 35]:
        six.pieces[i] = o.GamePiece(i, "black", 0, 0)  # x & y do not matter here
    
    for i in [7, 8, 9, 13, 15, 16, 19, 20, 21, 26, 28]:
        six.pieces[i] = o.GamePiece(i, "white", 0, 0)

    p = six.pieces
    assert six.all_can_capture(14) == [p[20], p[26], p[21], p[28], p[15], p[16], p[9], p[8], p[7], p[13], p[19]]

    p[35].color = "white"
    assert six.all_can_capture(14) == [p[20], p[26], p[15], p[16], p[9], p[8], p[7], p[13], p[19]]


def test_find_valid_moves():
    # This section sets up the board
    six.pieces = [None for i in range(six.n**2)]

    for i in [0, 2, 4, 12, 17, 24, 32, 35]:
        six.pieces[i] = o.GamePiece(i, "black", 0, 0)  # x & y do not matter here
    for i in [7, 8, 9, 13, 15, 16, 19, 20, 21, 26, 28]:
        six.pieces[i] = o.GamePiece(i, "white", 0, 0)

    assert six.find_valid_moves() == {
        14: six.all_can_capture(14),
        23: six.all_can_capture(23),
        33: six.all_can_capture(33)
    }


def test_choose_move():
    six.valid_moves = {
        1: [1],
        2: [1, 2],
        3: [1, 2, 3],
        4: [1, 2, 3, 4],
        5: [1]
    }
    assert six.choose_move() == 4

    six.valid_moves = {}
    assert six.choose_move() == -1

########## /GameBoard Class Tests ##########

########## Square Class Tests ##########

def test_invalid_Square_init():
    # First check for invalid inputs

    # Testing location attribute
    with pt.raises(AssertionError) as string:
        o.Square("hello", 25, 25)
    with pt.raises(AssertionError) as lst:
        o.Square([1, 2, 3, 4], 25, 25)
    with pt.raises(AssertionError) as floating:
        o.Square(9.5, 25, 25)
    with pt.raises(AssertionError) as negative:
        o.Square(-1, 25, 25)
    
    assert "location must be a non-negative integer" in str(string.value)
    assert "location must be a non-negative integer" in str(lst.value)
    assert "location must be a non-negative integer" in str(floating.value)
    assert "location must be a non-negative integer" in str(negative.value)

    # Testing x & y values
    with pt.raises(AssertionError) as x_string:
        o.Square(0, "hello", 25)
    with pt.raises(AssertionError) as y_string:
        o.Square(1, 25, "hello")
    with pt.raises(AssertionError) as x_floating:
        o.Square(2, 25.5, 25)
    with pt.raises(AssertionError) as y_floating:
        o.Square(3, 25, 25.5)
    with pt.raises(AssertionError) as x_lst:
        o.Square(4, [2, 5], 25)
    with pt.raises(AssertionError) as y_lst:
        o.Square(4, 25, [2, 5])

    assert "x & y must be integers" in str(x_string.value)
    assert "x & y must be integers" in str(y_string.value)
    assert "x & y must be integers" in str(x_floating.value)
    assert "x & y must be integers" in str(y_floating.value)
    assert "x & y must be integers" in str(x_lst.value)
    assert "x & y must be integers" in str(y_lst.value)


### Now test valid inputs
# Make squares
# x & y coordinates for each quadrant
neg_neg = o.Square(0, -50, -50)
pos_neg = o.Square(1, 50, -50)
origin = o.Square(2, 0, 0)
neg_pos = o.Square(3, -50, 50)
pos_pos = o.Square(4, 50, 50)


def test_valid_init():

    assert pos_pos.location == 4
    assert pos_pos.x == 50
    assert pos_pos.y == 50
    assert pos_pos.size == 50
    assert pos_pos.center == (75, 75)

    assert pos_neg.location == 1
    assert pos_neg.x == 50
    assert pos_neg.y == -50
    assert pos_neg.size == 50
    assert pos_neg.center == (75, -25)

    assert neg_neg.location == 0
    assert neg_neg.x == -50
    assert neg_neg.y == -50
    assert neg_neg.size == 50
    assert neg_neg.center == (-25, -25)

    assert neg_pos.location == 3
    assert neg_pos.x == -50
    assert neg_pos.y == 50
    assert neg_pos.size == 50
    assert neg_pos.center == (-25, 75)

    assert origin.location == 2
    assert origin.x == 0
    assert origin.y == 0
    assert origin.size == 50
    assert origin.center == (25, 25)


def test_calc_center():
    # calc_center uses Square.x and Square.y, which are validated upon
    # initialization as integers. This method is indirectly tested
    # above, but is again here for the sake of completeness.

    assert pos_pos.calc_center() == (75, 75)
    assert pos_neg.calc_center() == (75, -25)
    assert neg_neg.calc_center() == (-25, -25)
    assert neg_pos.calc_center() == (-25, 75)
    assert origin.calc_center() == (25, 25)
    assert o.Square(5, 2, 54).calc_center() == (27, 79)


def test_was_clicked():
    # For these tests, note that all squares are 50x50 pixels and
    # clicks on the line is considered a False value.

    # Clicks inside
    assert origin.was_clicked(25, 25) == True   # middle
    assert origin.was_clicked(1, 1) == True     # lower left
    assert origin.was_clicked(49, 49) == True   # upper right
    assert origin.was_clicked(1, 49) == True    # upper left
    assert origin.was_clicked(49, 1) == True    # lower right

    # Clicks outside
    assert origin.was_clicked(0, 0) == False
    assert origin.was_clicked(50, 50) == False
    assert origin.was_clicked(0, 50) == False
    assert origin.was_clicked(50, 0) == False
    assert origin.was_clicked(25, 0) == False
    assert origin.was_clicked(0, 25) == False
    assert origin.was_clicked(50, 25) == False
    assert origin.was_clicked(25, 50) == False
    assert origin.was_clicked(-3, 54) == False
    assert origin.was_clicked(75, 90) == False


def test_is_empty():
    # Note that the GamePiece objects in the state list must have the same
    # index as their location attribute and they must have center coordinates
    # that are the same as the square that they are in (at least for the 
    # game to be played correctly). Also, method can be given any list and
    # still give an answer, it only tests for a None value in the location
    # of the square. This is a weakness, but normal game-play would never
    # cause a list of non-GamePiece objects to be tested.

    # Set up test gameboard
    test1 = o.GamePiece(0, "white", -25, -25)
    test2 = o.GamePiece(2, "black", 25, 25)
    board = [test1, None, test2, None, None]

    # Test Square objects
    assert neg_neg.is_empty(board) == False
    assert neg_pos.is_empty(board) == True
    assert origin.is_empty(board) == False
    assert pos_neg.is_empty(board) == True
    assert pos_pos.is_empty(board) == True

########## /Square Class Tests ##########

########## GamePiece Class Tests ##########

def test_invalid_GamePiece_init():
    # First check for invalid inputs

    # Testing location attribute
    with pt.raises(AssertionError) as string:
        o.GamePiece("hello", "white", 25, 25)
    with pt.raises(AssertionError) as lst:
        o.GamePiece([1, 2, 3, 4], "black", 25, 25)
    with pt.raises(AssertionError) as floating:
        o.GamePiece(9.5, "white", 25, 25)
    with pt.raises(AssertionError) as negative:
        o.GamePiece(-1, "black", 25, 25)
    
    assert "location must be a non-negative integer" in str(string.value)
    assert "location must be a non-negative integer" in str(lst.value)
    assert "location must be a non-negative integer" in str(floating.value)
    assert "location must be a non-negative integer" in str(negative.value)

    # Testing color values
    with pt.raises(AssertionError) as wrong_color:
        o.GamePiece(0, "Hello", 0, 0)
    with pt.raises(AssertionError) as wrong_color2:
        o.GamePiece(0, 0, 0, 0)

    assert "color must be 'black' or 'white'" in str(wrong_color.value)
    assert "color must be 'black' or 'white'" in str(wrong_color2.value)

    # Testing x & y values
    with pt.raises(AssertionError) as x_string:
        o.GamePiece(0, "black", "hello", 25)
    with pt.raises(AssertionError) as y_string:
        o.GamePiece(1, "black", 25, "hello")
    with pt.raises(AssertionError) as x_floating:
        o.GamePiece(2, "black", 25.5, 25)
    with pt.raises(AssertionError) as y_floating:
        o.GamePiece(3, "black", 25, 25.5)
    with pt.raises(AssertionError) as x_lst:
        o.GamePiece(4, "black", [2, 5], 25)
    with pt.raises(AssertionError) as y_lst:
        o.GamePiece(4, "black", 25, [2, 5])

    assert "x & y values must be integers" in str(x_string.value)
    assert "x & y values must be integers" in str(y_string.value)
    assert "x & y values must be integers" in str(x_floating.value)
    assert "x & y values must be integers" in str(y_floating.value)
    assert "x & y values must be integers" in str(x_lst.value)
    assert "x & y values must be integers" in str(y_lst.value)


# Valid objects
def test_change_color():
    # change_color is the only method in GamePiece that does not require drawing
    # anything in the window.
    test = o.GamePiece(0, "white", 0, 0)
    assert test.color == "white"
    test.change_color()
    assert test.color == "black"
    test.change_color()
    assert test.color == "white"


def test_peek():
    pass

########## /GamePiece Class Tests ##########
