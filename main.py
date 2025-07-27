from sys import stdout
from time import sleep
from Game import Board, Size, Mode
from AI import Connect4AI
from TextFormatting import format_text, Colours, Styles

# Print the welcome message
stdout.write("\rWelcome ")
sleep(1)
stdout.write("to ")
stdout.flush()
sleep(1)
stdout.write(format_text("Connect ", colour=Colours.YELLOW, style=Styles.BOLD) + format_text("4\n", colour=Colours.RED,
                                                                                             style=Styles.BOLD))
stdout.flush()
sleep(1)
stdout.write("\rBy ")
sleep(1)
stdout.write(format_text(text='Sahand Nikoo', colour=Colours.RED, style=Styles.BOLD))
stdout.flush()
sleep(1)
inp = input("\nPress 1 for instructions or any other key to play! ").strip()
sleep(1)

# Print the instructions
if inp == '1':
    stdout.write(
        "\nThe objective of the game is to " + format_text("connect 4 of your pieces together", colour=Colours.RED,
                                                           style=Styles.BOLD) + ", whether it's diagonal, horizontal, or vertical.\n")
    sleep(6)
    stdout.write("\nTo drop a piece, input the desired column number.\n")
    sleep(4)
    stdout.write("\nYou will be playing against a computer who has the same objective.\n")
    sleep(4)
    stdout.write("\nYour pieces will be " + format_text("red", colour=Colours.RED,
                                                        style=Styles.BOLD) + " and the computer's will be " + format_text(
        "yellow", colour=Colours.YELLOW, style=Styles.BOLD) + ".\n")
    stdout.flush()
    sleep(3)

# Ask the user who should go first
turn = input("\nPress 1 for the AI to go first or any other key for you to go first ").strip()
first = turn != '1'

# Initialize the Connect 4 board and print it
board = Board(size=Size.S_7x6, mode=Mode.NORMAL, player_first=first)
stdout.write(str(board))

# Initialize variables used in the game loop
chars = (' 🔴  ', ' 🟡  ')
curr_char = chars[0] if board.player_first else chars[1]
column = 0

# Game loop
while True:
    # Check if it is the player's turn
    if curr_char == chars[0]:
        # Get the player's move
        try:
            column = int(input("→ ").strip()) - 1
        # Handle non-integer input
        except ValueError:
            stdout.write("Invalid column number. Please enter a valid column.\n")
            continue
        # Handle out-of-bounds input
        if column < 0 or column >= board.size[0]:
            stdout.write("Invalid column number. Please select a column on the board.\n")
            continue
    # Check if it is the computer's turn
    else:
        # Create a copy of the board and get the computer's move
        temp_board = board.copy()
        computer = Connect4AI(temp_board)
        column = computer.get_best_move()

    # Attempt to drop the piece in the column
    valid = board.drop(column, curr_char)
    # Handle an invalid drop
    if not valid:
        # Check if the board is full
        if ' ⚫  ' not in [item for sublist in board.data for item in sublist]:
            stdout.write("It's a tie!")
            break
        # Otherwise, ask the player again
        stdout.write("Column is full. Please select another column.\n")
        continue

    # Check if the player or computer has won
    won = board.check_connect(column, board.data[column].index(curr_char), curr_char)
    if won:
        stdout.write(str(board))
        if curr_char == chars[0]:
            sleep(1)
            stdout.write(format_text(text='\rCongratulations! ', colour=Colours.GREEN, style=Styles.BOLD))
            sleep(1)
            stdout.write(format_text(text='You are victorious!\n', colour=Colours.GREEN, style=Styles.BOLD))
            stdout.flush()
        else:
            sleep(1)
            stdout.write(format_text(text='\rGame Over! ', colour=Colours.RED, style=Styles.BOLD))
            sleep(1)
            stdout.write(format_text(text='The computer is victorious!\n', colour=Colours.RED, style=Styles.BOLD))
            stdout.flush()
        sleep(1)

        # Ask the user if they want to play again
        play_again = True if input("\nPress 1 to play again or any other key to quit: ").strip() == '1' else False
        if play_again:
            turn = input("\nPress 1 for the AI to go first or any other key for you to go first ").strip()
            first = turn != '1'
            board = Board(size=Size.S_7x6, mode=Mode.NORMAL, player_first=first)
            stdout.write(str(board))
            curr_char = chars[0] if board.player_first else chars[1]
            continue
        else:
            stdout.write("\nBye!")
            break

    # Print the string representation of the board and switch whose turn it is
    stdout.write(str(board))
    curr_char = chars[1] if curr_char == chars[0] else chars[0]
