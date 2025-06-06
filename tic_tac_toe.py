import tkinter as tk
from tkinter import messagebox
import copy

# Main window setup
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("350x480")
root.resizable(False, False)

# Game variables
current_player = "X"
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
game_mode = None
x_wins = 0
o_wins = 0
draws = 0

# Check winner
def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != "":
            return b[i][0]
        if b[0][i] == b[1][i] == b[2][i] != "":
            return b[0][i]
    if b[0][0] == b[1][1] == b[2][2] != "":
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != "":
        return b[0][2]
    if all(cell != "" for row in b for cell in row):
        return "Draw"
    return None

# Minimax Algorithm
def minimax(b, depth, is_max):
    result = check_winner(b)
    if result == "O":
        return 1
    elif result == "X":
        return -1
    elif result == "Draw":
        return 0

    if is_max:
        best = -float("inf")
        for i in range(3):
            for j in range(3):
                if b[i][j] == "":
                    b[i][j] = "O"
                    best = max(best, minimax(b, depth+1, False))
                    b[i][j] = ""
        return best
    else:
        best = float("inf")
        for i in range(3):
            for j in range(3):
                if b[i][j] == "":
                    b[i][j] = "X"
                    best = min(best, minimax(b, depth+1, True))
                    b[i][j] = ""
        return best

# Best move for computer
def best_move():
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Handle cell click
def on_click(r, c):
    global current_player
    if board[r][c] == "":
        board[r][c] = current_player
        buttons[r][c].config(text=current_player, state="disabled")
        winner = check_winner(board)
        if winner:
            end_game(winner)
        else:
            current_player = "O" if current_player == "X" else "X"
            status_label.config(text=f"{current_player}'s Turn")
            if game_mode == "Single Player" and current_player == "O":
                root.after(500, computer_move)

# Computer makes move
def computer_move():
    global current_player
    r, c = best_move()
    if r is not None:
        board[r][c] = "O"
        buttons[r][c].config(text="O", state="disabled")
        winner = check_winner(board)
        if winner:
            end_game(winner)
        else:
            current_player = "X"
            status_label.config(text="X's Turn")

# Game over handler
def end_game(winner):
    global x_wins, o_wins, draws
    if winner == "Draw":
        messagebox.showinfo("Game Over", "It's a draw!")
        draws += 1
    else:
        messagebox.showinfo("Game Over", f"Player {winner} wins!")
        if winner == "X":
            x_wins += 1
        else:
            o_wins += 1
    update_scoreboard()
    reset_board()

# Scoreboard update
def update_scoreboard():
    x_score_label.config(text=f"X Wins: {x_wins}")
    o_score_label.config(text=f"O Wins: {o_wins}")
    draw_score_label.config(text=f"Draws: {draws}")

# Reset game board
def reset_board():
    global board, current_player
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    status_label.config(text="X's Turn")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")

# Reset to mode selection
def reset_game_to_mode_select():
    global x_wins, o_wins, draws, game_mode
    x_wins = o_wins = draws = 0
    game_mode = None
    hide_game_screen()
    show_mode_select()

# Screen controls
def show_mode_select():
    mode_select_frame.pack(pady=100)

def hide_mode_select():
    mode_select_frame.pack_forget()

def show_game_screen():
    game_frame.pack()
    scoreboard_frame.pack()
    status_label.pack(pady=10)
    board_frame.pack()
    reset_button.pack(pady=10)

def hide_game_screen():
    game_frame.pack_forget()
    scoreboard_frame.pack_forget()
    status_label.pack_forget()
    board_frame.pack_forget()
    reset_button.pack_forget()

def set_mode(mode):
    global game_mode
    game_mode = mode
    hide_mode_select()
    reset_board()
    update_scoreboard()
    show_game_screen()

# Mode selection UI
mode_select_frame = tk.Frame(root)
tk.Label(mode_select_frame, text="Choose Game Mode", font=('Arial', 16, 'bold')).pack(pady=10)
tk.Button(mode_select_frame, text="Single Player", font=('Arial', 14), width=20, command=lambda: set_mode("Single Player")).pack(pady=5)
tk.Button(mode_select_frame, text="Two Player", font=('Arial', 14), width=20, command=lambda: set_mode("Two Player")).pack(pady=5)

# Game screen UI
game_frame = tk.Frame(root)
status_label = tk.Label(root, text="X's Turn", font=('Arial', 14))

scoreboard_frame = tk.Frame(root)
x_score_label = tk.Label(scoreboard_frame, text="X Wins: 0", font=('Arial', 11))
x_score_label.grid(row=0, column=0, padx=10)
o_score_label = tk.Label(scoreboard_frame, text="O Wins: 0", font=('Arial', 11))
o_score_label.grid(row=0, column=1, padx=10)
draw_score_label = tk.Label(scoreboard_frame, text="Draws: 0", font=('Arial', 11))
draw_score_label.grid(row=0, column=2, padx=10)

board_frame = tk.Frame(root)
for i in range(3):
    for j in range(3):
        btn = tk.Button(board_frame, text="", font=('Arial', 18), width=5, height=2,
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j)
        buttons[i][j] = btn

reset_button = tk.Button(root, text="Reset to Mode Selection", font=('Arial', 12), command=reset_game_to_mode_select)

# Start game
show_mode_select()
root.mainloop()
