import random

board_size = 3
board = [[[i * 9 + j * 3 + k + 1 for k in range(3)] for j in range(3)] for i in range(3)]

MODE_HUMAN_VS_HUMAN = '1'
MODE_HUMAN_VS_AI = '2'


def draw_board(board):
    ''' Display the 3D game board '''
    board_size = len(board)

    def draw_layer(layer):
        # Draw the horizontal separator
        print('_' * 4 * board_size)

        for i in range(board_size):
            # Draw empty row
            print((' ' * 4 + '|') * board_size)

            # Draw the row with board values
            row_values = ' | '.join(str(layer[i][j] or i * 9 + j * 3 + k + 1).rjust(2) for k, j in enumerate(range(board_size)))
            print('', row_values, ' |')

            # Draw separator
            print(('_' * 4 + '|') * board_size)

    # Loop through each layer and draw it
    for z in range(board_size):
        print("\nLayer", z + 1)
        draw_layer(board[z])
        print()


def computer_move(char):
    valid_moves = [i for i in range(1, 28) if board[(i - 1) // 9][(i - 1) % 9 // 3][(i - 1) % 9 % 3] not in ('X', 'O')]
    return random.choice(valid_moves) if valid_moves else None


def check_win(board):
    # Checking within layers
    for layer in board:
        for row in layer:
            if row.count(row[0]) == len(row) and row[0] != "":
                return True
        for col in range(3):
            if all(layer[i][col] == layer[0][col] and layer[0][col] != "" for i in range(3)):
                return True
        if check_diagonal_win(layer):
            return True

    # Checking across layers
    for i in range(3):
        for j in range(3):
            if all(board[k][i][j] == board[0][i][j] and board[0][i][j] != "" for k in range(3)):
                return True

    # Checking 3D diagonals
    diagonals = [
        [(0, 0, 0), (1, 1, 1), (2, 2, 2)],
        [(0, 0, 2), (1, 1, 1), (2, 2, 0)],
        [(0, 2, 0), (1, 1, 1), (2, 0, 2)],
        [(0, 2, 2), (1, 1, 1), (2, 0, 0)]
    ]

    for diagonal in diagonals:
        if all(board[z][y][x] == board[diagonal[0][2]][diagonal[0][1]][diagonal[0][0]] and board[diagonal[0][2]][diagonal[0][1]][diagonal[0][0]] != "" for x, y, z in diagonal):
            return True

    return False

def check_diagonal_win(layer):
    # Check main diagonal (from top-left to bottom-right)
    if all(layer[i][i] == layer[0][0] for i in range(board_size)) and layer[0][0] != "":
        return True

    # Check secondary diagonal (from top-right to bottom-left)
    if all(layer[i][board_size - 1 - i] == layer[0][board_size - 1] for i in range(board_size)) and layer[0][board_size - 1] != "":
        return True

    return False


def game_step(x, y, z, char):
    if board[z][y][x] in ('X', 'O'):
        return False
    board[z][y][x] = char
    return True


def next_player(current_player):
    return 'O' if current_player == 'X' else 'X'


def start_game(mode):
    player_X_name = input("Enter the name for player X: ")
    player_O_name = "Computer" if mode == MODE_HUMAN_VS_AI else input("Enter the name for player O: ")
    
    current_player = 'X'
    step = 1
    draw_board(board)

    while (step < 28) and (not check_win(board)):
        current_name = player_X_name if current_player == 'X' else player_O_name

        if current_name == "Computer":
            index = computer_move(current_player)
            print(f"Computer's turn. Computer chose {index}.")
        else:
            try:
                index = int(input(f"{current_name}'s turn. Enter a number between 1-27 (0 to exit):"))
                if index == 0:
                    return
            except ValueError:
                print("Please enter a number between 1-27.")
                continue

        x, y, z = convert_to_coordinates(index)

        if game_step(x, y, z, current_player):
            current_player = next_player(current_player)
            step += 1
            draw_board(board)
        else:
            print("Invalid coordinates! Please repeat!")

    if step >= 28:
        print('The game is over. It\'s a draw!')
    elif check_win(board):
        winner_name = player_O_name if current_player == 'X' else player_X_name
        print(f"{winner_name} ({next_player(current_player)}) won!")


def convert_to_coordinates(num):
    z = (num - 1) // 9
    y = (num - 1 - z * 9) // 3
    x = (num - 1 - z * 9) % 3
    return x, y, z


print('Welcome to the game!')
mode = input("Game Mode:\n1 - Human vs Human\n2 - Human vs Computer\nChoose a game mode:")

if mode in [MODE_HUMAN_VS_HUMAN, MODE_HUMAN_VS_AI]:
    start_game(mode)
else:
    print("Invalid choice!")
