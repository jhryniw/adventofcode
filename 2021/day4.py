with open('day4_input.txt', 'r') as f:
    moves = list(map(int, next(f).split(',')))
    print(moves)
    boards = []

    while True:
        if next(f, None) is None:
            break
        
        board = []
        for i in range(5):
            line = filter(lambda s: s != '', next(f).split(' '))
            board.append(list(map(lambda s: int(s.strip()), line)))
        boards.append(board)

move_lookup = dict([(m, i) for i, m in enumerate(moves)])
max_index = len(moves)

def board_completion_move(board):
    completion_move = max_index
    index_board = list([0, 0, 0, 0, 0] for i in range(5))
    for i in range(5):
        for j in range(5):
            index_board[i][j] = move_lookup[board[i][j]]

    # Check rows
    for i in range(5):
        row_index = 0
        for j in range(5):
            row_index = max(row_index, index_board[i][j])
        completion_move = min(completion_move, row_index)

    # Check columns
    for j in range(5):
        col_index = 0
        for i in range(5):
            col_index = max(col_index, index_board[i][j])
        completion_move = min(completion_move, col_index)

    # Check diag
    # main_diag_index = 0
    # off_diag_index = 0
    # for i in range(5):
    #     main_diag_index = max(index_board[i][i], main_diag_index)
    #     off_diag_index = max(index_board[4-i][i], off_diag_index)
    
    # completion_move = min(completion_move, main_diag_index)
    # completion_move = min(completion_move, off_diag_index)

    return completion_move

def sum_unmarked(board, num_moves):
    total = 0
    for i in range(5):
        for j in range(5):
            if move_lookup[board[i][j]] > num_moves:
                total += board[i][j]
    return total

min_move = max_index
board_index = 0
for i, board in enumerate(boards):
    board_move = board_completion_move(board)
    if board_move < min_move:
        min_move = board_move
        board_index = i

unmarked = sum_unmarked(boards[board_index], min_move)
print(unmarked * moves[min_move])


print("#########")

# Part 2

max_move = 0
board_index = 0
for i, board in enumerate(boards):
    board_move = board_completion_move(board)
    if board_move > max_move:
        max_move = board_move
        board_index = i

unmarked = sum_unmarked(boards[board_index], max_move)
print(unmarked * moves[max_move])
