import random


def print_field(matrix):
    print('-' * 9)
    for row in matrix:
        print('|', end=' ')
        for elem in row:
            print(' ' if elem == '_' else elem, end=' ')
        print('|')
    print('-' * 9)


def enter_coord():
    while True:
        coord = input('Enter the coordinates: ')
        try:
            x, y = map(int, coord.split())
        except ValueError:
            print("You should enter numbers!")
        else:
            if not 1 <= x <= 3 or not 1 <= y <= 3:
                print("Coordinates should be from 1 to 3!")
            else:
                break
    return x, y


def is_game_finished(matrix):
    return not any(elem == '_' for row in matrix for elem in row)


def is_coord_valid(matrix, x, y):
    if matrix[x-1][y-1] == '_':
        return True
    return False


def count_elem(matrix, symbol):
    counter = 0
    for row in matrix:
        for elem in row:
            if elem == symbol:
                counter += 1
    return counter


def make_move(matrix, player, sign):
    if player == 'user':
        return user_move(matrix, sign)
    elif player == 'easy':
        print('Making move level "easy"')
        return computer_move_easy(matrix, sign)
    elif player == 'medium':
        print('Making move level "medium"')
        return computer_move_medium(matrix, sign)
    elif player == 'hard':
        print('Making move level "hard"')
        return computer_move_hard(matrix, sign)


def user_move(matrix, sign):
    x, y = enter_coord()
    while not is_coord_valid(field, x, y):
        print('This cell is occupied! Choose another one!')
        x, y = enter_coord()
    matrix[x-1][y-1] = sign
    return matrix


def computer_move_easy(matrix, sign):
    coord = [(i, j) for i in range(3) for j in range(3) if field[i][j] == '_']
    x, y = random.choice(coord)
    matrix[x][y] = sign
    return matrix


def is_almost_win_line(lst, sign_1, sign_2):
    if lst.count(sign_1) == 2 and sign_2 not in lst:
        return True
    return False


def check_win_line(matrix, sign_1, sign_2):
    # whether one of the rows is almost winning
    for i in range(3):
        if is_almost_win_line(matrix[i], sign_1, sign_2):
            return i, matrix[i].index('_')
    # whether one of the columns is almost winning
    for i in range(3):
        lst = []
        for j in range(3):
            lst.append(matrix[j][i])
        if is_almost_win_line(lst, sign_1, sign_2):
            return lst.index('_'), i
    # whether the main diagonal is almost winning
    lst = []
    for i in range(3):
        lst.append(matrix[i][i])
    if is_almost_win_line(lst, sign_1, sign_2):
        return lst.index('_'), lst.index('_')
    lst.clear()
    # whether the secondary diagonal is almost winning
    for i in range(3):
        lst.append(matrix[i][2 - i])
    if is_almost_win_line(lst, sign_1, sign_2):
        return lst.index('_'), 2 - lst.index('_')
    return None


def computer_move_medium(matrix, sign):
    player_sign = sign
    opponent_sign = 'O' if sign == 'X' else 'X'
    # whether computer could win
    coord = check_win_line(matrix, player_sign, opponent_sign)
    if coord:
        x, y = coord
        matrix[x][y] = player_sign
        return matrix
    # whether opponent could win
    coord = check_win_line(matrix, opponent_sign, player_sign)
    if coord:
        x, y = coord
        matrix[x][y] = player_sign
        return matrix
    # otherwise, computer makes the random move
    return computer_move_easy(matrix, player_sign)


def computer_move_hard(matrix, sign):
    lst = from_matrix_to_line(matrix)
    best_move = min_max(lst, 'player_ai', sign)
    lst[best_move] = sign
    matrix = from_line_to_matrix(lst)
    return matrix


def from_line_to_matrix(line):
    matrix = []
    k = 0
    for i in range(3):
        matrix.append([])
        for j in range(3):
            matrix[i].append(line[j + k])
        k += 3
    return matrix


def from_matrix_to_line(matrix):
    line = [matrix[i][j] for i in range(3) for j in range(3)]
    return line


def min_max(lst, player, sign):
    ai_sign = opponent_sign = ''
    if player == 'player_ai':
        ai_sign = sign
        opponent_sign = 'O' if sign == 'X' else 'X'
    elif player == 'opponent':
        opponent_sign = sign
        ai_sign = 'O' if sign == 'X' else 'X'
    # print(player, ai_sign, opponent_sign)
    # check for the terminal states such as win, lose and draw
    matrix = from_line_to_matrix(lst)
    if is_winning_game(matrix, ai_sign):
        return 10
    elif is_winning_game(matrix, opponent_sign):
        return -10
    elif is_game_finished(matrix):
        return 0
    # available states
    empty_cells = [i for i in range(9) if lst[i] == '_']
    moves = []
    for cell in empty_cells:
        move = dict()
        move['index'] = cell
        lst[cell] = sign
        if player == 'player_ai':
            # print('Test ai', ai_sign, opponent_sign)
            move['score'] = min_max(lst, 'opponent', opponent_sign)
        elif player == 'opponent':
            # print('Test opponent', ai_sign, opponent_sign)
            move['score'] = min_max(lst, 'player_ai', ai_sign)
        lst[cell] = move['index']
        moves.append(move)
    # find best move
    best_move = None
    if player == 'player_ai':
        best_score = -100000
        for move in moves:
            if move['score'] > best_score:
                best_score = move['score']
                best_move = move['index']
    else:
        best_score = 100000
        for move in moves:
            if move['score'] < best_score:
                best_score = move['score']
                best_move = move['index']
    return best_move


def is_win_line(lst, sign):
    if lst.count(sign) == 3:
        return True
    return False


def is_winning_game(matrix, sign):
    # whether one of the rows is winning
    for row in matrix:
        if is_win_line(row, sign):
            return True
    # whether one of the columns is winning
    for i in range(3):
        lst = []
        for j in range(3):
            lst.append(matrix[j][i])
        if is_win_line(lst, sign):
            return True
    # whether the main diagonal is winning
    lst = []
    for i in range(3):
        lst.append(matrix[i][i])
    if is_win_line(lst, sign):
        return True
    lst.clear()
    # whether the secondary diagonal is winning
    for i in range(3):
        lst.append(matrix[i][2 - i])
    if is_win_line(lst, sign):
        return True
    return False


def input_command():
    while True:
        command = input("Input command: ")
        if command.startswith('start') and len(command.split()) == 3:
            return command
        elif command == 'exit':
            return command
        else:
            print('Bad parameters!')


if __name__ == '__main__':
    while True:
        user_command = input_command()
        if user_command == 'exit':
            break
        command_list = user_command.split()
        field = [['_' for i in range(3)] for j in range(3)]
        print_field(field)
        move_counter = 0
        while not is_game_finished(field):
            move_counter += 1
            if move_counter % 2:
                player_sign = 'X'
                player = command_list[1]
            else:
                player_sign = 'O'
                player = command_list[2]
            field = make_move(field, player, player_sign)
            print_field(field)
            if is_winning_game(field, player_sign):
                print(f'{player_sign} wins')
                break
        else:
            print('Draw')
