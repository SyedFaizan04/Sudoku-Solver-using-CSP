import tkinter as tk
import numpy as np

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_cell(board):
    min_zeros = 10
    min_cell = None
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                row_zeros = np.count_nonzero(board[i, :] == 0)
                col_zeros = np.count_nonzero(board[:, j] == 0)
                start_row, start_col = 3 * (i // 3), 3 * (j // 3)
                subgrid_zeros = np.count_nonzero(board[start_row:start_row + 3, start_col:start_col + 3] == 0)
                min_local_zeros = min(row_zeros, col_zeros, subgrid_zeros)

                if min_local_zeros < min_zeros:
                    min_zeros = min_local_zeros
                    min_cell = (i, j)

    return min_cell

def check_row_constraint(board, row, num):
    return num not in board[row]

def check_column_constraint(board, col, num):
    return num not in board[:, col]

def check_subgrid_constraint(board, row, col, num):
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    subgrid = board[start_row:start_row + 3, start_col:start_col + 3]
    return num not in subgrid

def is_valid_move(board, row, col, num):
    return (
        check_row_constraint(board, row, num) and
        check_column_constraint(board, col, num) and
        check_subgrid_constraint(board, row, col, num)
    )

entries = []
display = []
values = np.zeros((9, 9), dtype=int)
main = tk.Tk()
main.title("Sudoku Puzzle Solver")

font_config = ("Calibri", 12, "bold")
font_config2 = ("Calibri", 14, "bold")
bg_color = "gray"  
entry_bg_color = "white"  
entry_fg_color = "black"  
readonly_bg_color = "#333333"  # Grey 
label_bg_color = "Navy blue"  
label_fg_color = "#FFFFFF"  # White
button_bg_color = "#00FF00"  # Green
button_fg_color = "#000000"  # Black

main.configure(bg=bg_color)

def Solve():
    for row in range(9):
        for col in range(9):
            try:
                value = int(entries[row][col].get())
                values[row][col] = value if value else 0
            except ValueError:
                values[row][col] = 0

    if solve_sudoku(values):
        for row in range(9):
            for col in range(9):
                display[row][col].config(state='normal')
                display[row][col].delete(0, tk.END)
                display[row][col].insert(0, str(values[row][col]))
                display[row][col].config(state='readonly')
    else:
        print("No solution exists.")

label = tk.Label(main, text="Enter Unsolved Puzzle", font=font_config, bg=label_bg_color, fg=label_fg_color)
label.grid(row=0, column=2, columnspan=5, pady=10)

for i in range(9):
    row = []
    for j in range(9):
        entry = tk.Entry(main, width=3, font=font_config, justify='center', bg=entry_bg_color, fg=entry_fg_color, relief='solid', borderwidth=1)
        entry.grid(row=i+1, column=j, padx=5, pady=5)
        row.append(entry)
    entries.append(row)

solve_btn = tk.Button(main, text="Solve Puzzle", font=font_config2, command=Solve, bg=button_bg_color, fg=button_fg_color, relief='raised', borderwidth=2)
solve_btn.grid(row=10, column=8, columnspan=5, padx=20, pady=20)

label2 = tk.Label(main, text="Solved Puzzle", font=font_config, bg=label_bg_color, fg=label_fg_color)
label2.grid(row=0, column=14, columnspan=5, pady=10)

for i in range(9):
    row = []
    for j in range(9):
        entry = tk.Entry(main, width=3, font=font_config, state='readonly', justify='center', bg=readonly_bg_color, fg=entry_fg_color, relief='solid', borderwidth=1)
        entry.grid(row=i+1, column=j+12, padx=5, pady=5)
        row.append(entry)
    display.append(row)

main.mainloop()

