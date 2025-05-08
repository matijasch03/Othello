import copy

class Board:

    def __init__(self):
        #                0    1    2    3    4    5    6    7
        self._board = [['-', '-', '-', '-', '-', '-', '-', '-'],  # 0
                       ['-', '-', '-', '-', '-', '-', '-', '-'],  # 1
                       ['-', '-', '-', '-', '-', '-', '-', '-'],  # 2
                       ['-', '-', '-', 'B', 'W', '-', '-', '-'],  # 3
                       ['-', '-', '-', 'W', 'B', '-', '-', '-'],  # 4
                       ['-', '-', '-', '-', '-', '-', '-', '-'],  # 5
                       ['-', '-', '-', '-', '-', '-', '-', '-'],  # 6
                       ['-', '-', '-', '-', '-', '-', '-', '-']]  # 7

    @property
    def board(self):
        return self._board

    @board.setter
    def age(self, board):
        self._board = board

    def evaluate_position(self) -> int:
        score = 0
        white_num = black_num = 0

        for row in range(8): # obilazak matrice (tabele) i racunanje njene heuristike stabilnosti
            for col in range(8):
                piece = self._board[row][col]
                if piece == 'B': black_num += 1 # heuristika brojnosti figura
                elif piece == 'W': white_num += 1

        if white_num + black_num != 0:
            score += 100 * (white_num - black_num) / (white_num + black_num) # heuristika brojnosti figura

        white_moves, _, _ = self.next_moves('W')
        num_white_moves = len(white_moves)
        black_moves, _, _ = self.next_moves('B')
        num_black_moves = len(black_moves)

        if num_white_moves + num_black_moves != 0:
            score += 100 * (num_white_moves - num_black_moves) / (num_white_moves + num_black_moves)  # heuristika mobilnosti figura

        white_corners = black_corners = 0
        white_stabile = black_stabile = 0

        if self._board[0][0] == 'B':
            black_corners += 1
            black_stabile += self.stable_coins('B', 0, 0, [[0, 1], [1, 0], [1, 1]])

        elif self._board[0][0] == 'W':
            white_corners += 1
            white_stabile += self.stable_coins('W', 0, 0, [[0, 1], [1, 0], [1, 1]])

        if self._board[0][7] == 'B':
            black_corners += 1
            black_stabile += self.stable_coins('B', 0, 7, [[0, -1], [1, 0], [1, -1]])

        elif self._board[0][7] == 'W':
            white_corners += 1
            white_stabile += self.stable_coins('W', 0, 7, [[0, -1], [1, 0], [1, -1]])

        if self._board[7][0] == 'B':
            black_corners += 1
            black_stabile += self.stable_coins('B', 7, 0, [[0, 1], [-1, 0], [-1, 1]])

        elif self._board[7][0] == 'W':
            white_corners += 1
            white_stabile += self.stable_coins('W', 7, 0, [[0, 1], [-1, 0], [-1, 1]])

        if self._board[7][7] == 'B':
            black_corners += 1
            black_stabile += self.stable_coins('B', 7, 7, [[0, -1], [-1, 0], [-1, -1]])

        elif self._board[7][7] == 'W':
            white_corners += 1
            white_stabile += self.stable_coins('W', 7, 7, [[0, -1], [-1, 0], [-1, -1]])

        if white_corners + black_corners != 0:
            score += 100 * (white_corners - black_corners) / (white_corners + black_corners)  # heuristika popunjenosti coskova

        white_unstabile = black_unstabile = 0

        for i in range(8):
            for j in range(8):
                if self._board[i][j] != "-":
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

                    for dx, dy in directions:
                        new_row = i + dx
                        new_col = j + dy

                        if (1 < new_row < 8) and (1 < new_col < 8) and self._board[new_row][new_col] == "-":
                            if self._board[i][j] == 'W': white_unstabile += 1
                            elif self._board[i][j] == 'B': black_unstabile += 1
                            break
        white_stability = white_stabile - white_unstabile
        black_stability = black_stabile - black_unstabile

        if white_stability + black_stability != 0:
            score += 100 * (white_stability - black_stability) / (white_stability + black_stability)  # heuristika stabilnosti
                        
        return score

    def next_moves(self, player): # vraca dve dole navedene liste i bool vrednost da li je kraj igre
        list_next_moves = []
        list_crossed_way = []

        expanded_board = [[''] * 10 for _ in range(10)]  # pomaze pri izlazenju van opsega iz matrice
        for i in range(1, 9):
            for j in range(1, 9):
                expanded_board[i][j] = self._board[i - 1][j - 1]

        if player == 'B':
            opponent = 'W'
        else: opponent = 'B'

        for i in range(1, 9):
            for j in range(1, 9):
                row = i
                col = j  # cuvaju koordinate
                if expanded_board[i][j] == player:
                    while (expanded_board[i - 1][j] == opponent):  # 1) gore
                        i -= 1
                    if i != row :
                        if i > 1 and expanded_board[i - 1][j] == '-':
                            list_next_moves.append([i - 1, j])
                            list_crossed_way.append([row - i, 0])
                        i = row

                    while (expanded_board[i + 1][j] == opponent):  # 2) dole
                        i += 1
                    if i != row:
                        if i < 8 and expanded_board[i + 1][j] == '-':
                            list_next_moves.append([i + 1, j])
                            list_crossed_way.append([row - i, 0])
                        i = row

                    while (expanded_board[i][j - 1] == opponent):  # 3) levo
                        j -= 1
                    if j != col:
                        if j > 1 and expanded_board[i][j - 1] == '-':
                            list_next_moves.append([i, j - 1])
                            list_crossed_way.append([0, col - j])
                        j = col

                    while (expanded_board[i][j + 1] == opponent):  # 4) desno
                        j += 1
                    if j != col:
                        if j < 8 and expanded_board[i][j + 1] == '-':
                            list_next_moves.append([i, j + 1])
                            list_crossed_way.append([0, col - j])
                        j = col

                    while (expanded_board[i - 1][j - 1] == opponent):  # 5) gore levo
                        i -= 1
                        j -= 1

                    if j != col:
                        if j > 1 and i > 1 and expanded_board[i - 1][j - 1] == '-':
                            list_next_moves.append([i - 1, j - 1])
                            delta = row - i
                            list_crossed_way.append([delta, delta])
                        i = row
                        j = col

                    while (expanded_board[i - 1][j + 1] == opponent):  # 6) gore desno
                        i -= 1
                        j += 1

                    if j != col:
                        if j > 1 and i < 8 and expanded_board[i - 1][j + 1] == '-':
                            list_next_moves.append([i - 1, j + 1])
                            delta = row - i
                            list_crossed_way.append([delta, -delta])
                        i = row
                        j = col

                    while (expanded_board[i + 1][j - 1] == opponent):  # 7) dole levo
                        i += 1
                        j -= 1

                    if j != col:
                        if j > 1 and i < 8 and expanded_board[i + 1][j - 1] == '-':
                            list_next_moves.append([i + 1, j - 1])
                            delta = row - i
                            list_crossed_way.append([delta, -delta])
                        i = row
                        j = col

                    while (expanded_board[i + 1][j + 1] == opponent):  # 8) dole desno
                        i += 1
                        j += 1

                    if j != col:
                        if j < 8 and i < 8 and expanded_board[i + 1][j + 1] == '-':
                            list_next_moves.append([i + 1, j + 1])
                            delta = row - i
                            list_crossed_way.append([delta, delta])
                        i = row
                        j = col

        move_existing = True # objasnjava postoji li mogucnost za sledeci potez, tj. da li je game over
        if not list_next_moves:
            move_existing = False

        return list_next_moves, list_crossed_way, move_existing

    def draw_table(self):
        print("\n  ", end=' ')
        for i in range(1, 9):
            print(i, end="  ")
        print()

        white_num = black_num = 0

        row = 1
        for i in self._board:
            print(row, end="  ")
            row += 1
            for j in i:
                print(j, end="  ")
                if j == 'B': black_num += 1
                elif j == 'W': white_num += 1
            print()
        print('Black disks:', black_num, '   White disks:', white_num, '\n')


    def play_a_move(self, chosen_pair, list_next_moves, list_crossed_way, player):
        x = chosen_pair[0] - 1
        y = chosen_pair[1] - 1

        indexes = []
        while chosen_pair in list_next_moves:
            indexes.append(list_next_moves.index(chosen_pair))
            list_next_moves[list_next_moves.index(chosen_pair)][0] = -1

        for index in indexes:

            delta_position = list_crossed_way[index]
            x_delta = delta_position[0]
            y_delta = delta_position[1]

            if y_delta == 0:  # promena samo po x
                x_new = x + x_delta
                x_min = min(x_new, x)
                x_max = max(x_new, x)
                for i in range(x_min, x_max + 1):
                    self._board[i][y] = player

            elif x_delta == 0:  # promena samo po y
                y_new = y + y_delta
                y_min = min(y_new, y)
                y_max = max(y_new, y)
                for i in range(y_min, y_max + 1):
                    self._board[x][i] = player

            elif x_delta + y_delta != 0:  # promena po obe ose u istom smeru
                j = 0
                for i in range(abs(x_delta) + 1):
                    self._board[x + j][y + j] = player
                    j += x_delta // abs(x_delta)

            else:  # promena po obe ose u razlicitim smerovima
                j = 0
                for i in range(abs(x_delta) + 1):
                    self._board[x + j][y - j] = player
                    j += x_delta // abs(x_delta)

    def winner(self):
        num_black = num_white = 0

        for i in range(8):
            for j in range(8):
                if self._board[i][j] == 'B':
                    num_black += 1
                elif self._board[i][j] == 'W':
                    num_white += 1

        if num_white > num_black:
            print('The winner is the white player.')
        elif num_black > num_white:
            print('The winner is the black player.')
        else:
            print('The result is a draw.')


    def stable_coins(self, player, x, y, directions): # lista pravaca u kojima se moguce kretati iz datog coska (x, y)
        stability_score = 1
        for dx, dy in directions: # racuna broj susednih figura u coskovima (stabilnih)
            while (0 < x + dx < 8) and (0 < y + dy < 8) and self._board[x + dx][y + dy] == player:
                stability_score += 1
                if dx != 0:
                    dx += dx // abs(dx)
                if dy != 0:
                    dy += dy // abs(dy)

        return stability_score
