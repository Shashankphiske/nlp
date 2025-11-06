import math

# Initialize the board
board = [" " for _ in range(9)]

# Function to print the board
def print_board():
    for i in range(3):
        print(board[3*i], "|", board[3*i+1], "|", board[3*i+2])
        if i < 2:
            print("---------")

# Check for winner
def winner(b, player):
    win_states = [
        [0,1,2], [3,4,5], [6,7,8], # rows
        [0,3,6], [1,4,7], [2,5,8], # columns
        [0,4,8], [2,4,6]           # diagonals
    ]
    for state in win_states:
        if b[state[0]] == b[state[1]] == b[state[2]] == player:
            return True
    return False

# Check for draw
def draw(b):
    return " " not in b

# Minimax algorithm
def minimax(b, depth, is_maximizing):
    if winner(b, "O"):
        return 1
    elif winner(b, "X"):
        return -1
    elif draw(b):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                score = minimax(b, depth + 1, False)
                b[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                score = minimax(b, depth + 1, True)
                b[i] = " "
                best_score = min(score, best_score)
        return best_score

# AI move using Minimax
def ai_move():
    best_score = -math.inf
    move = 0
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"

# Main game loop
def play_game():
    print("Tic Tac Toe (You: X | AI: O)")
    print_board()

    while True:
        # Player move
        move = int(input("Enter your move (1-9): ")) - 1
        if board[move] != " ":
            print("Invalid move! Try again.")
            continue
        board[move] = "X"

        if winner(board, "X"):
            print_board()
            print("🎉 You win!")
            break
        elif draw(board):
            print_board()
            print("It's a draw!")
            break

        # AI move
        ai_move()

        print_board()

        if winner(board, "O"):
            print("💻 AI wins!")
            break
        elif draw(board):
            print("It's a draw!")
            break

# Run the game
play_game()
