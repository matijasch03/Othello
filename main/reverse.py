import copy

from exceptiongroup import catch

from board import Board

def ask_opponent_what_to_play(): # vraca bool vrednost postojanja poteza i broj mogucih poteza
    list_next_moves, list_crossed_way, move_existing = board.next_moves("B")

    if move_existing:
        unique_list = [list(t) for t in set(tuple(move) for move in list_next_moves)]
        print(unique_list)

        while True:
            position_string = input('Choose some of this positions (in format a, b): ')

            position = position_string.split(", ")

            try:
                x = int(position[0])
                y = int(position[1])
                chosen_pair = [x, y]

                if chosen_pair not in list_next_moves:
                    print('Non-existent position! Please choose one from the above.\n')
                    raise Exception

                board.play_a_move(chosen_pair, list_next_moves, list_crossed_way, 'B')
                board.draw_table()
                break

            except (ValueError, IndexError):
                print("You didn't input a correct format. Try again. e.g. 3, 5\n")
            except Exception:
                pass

    return move_existing, len(list_crossed_way)

def minimax(board, depth, maximizing_player, alpha, beta):
    list_next_moves, list_crossed_way, move_existing = board.next_moves('W')  # beli je maximizing igrac
    list_next_moves1, list_crossed_way1, move_existing1 = board.next_moves('B')  # crni je minimizing igrac
    move_dict = {} # (position, evaluation)

    if depth == 0 or not move_existing or not move_existing1:
        return board.evaluate_position(), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        old_board = copy.deepcopy(board)

        for position in list_next_moves:
            if position[0] != -1: # signal da je polje vec poseceno (u pitanju je duplikat)
                # 2. opcija: if position not in move_dict:
                chosen_pair = []
                chosen_pair.append(position[0])
                chosen_pair.append(position[1])
                board.play_a_move(chosen_pair, list_next_moves, list_crossed_way, 'W')
                eval_score, _ = minimax(board, depth - 1, False, alpha, beta)
                move_dict[board] = eval_score
                board = copy.deepcopy(old_board)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = chosen_pair

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

        return max_eval, best_move

    else:  # minimizing igrac
        min_eval = float('inf')
        best_move = None
        old_board = copy.deepcopy(board)

        for position in list_next_moves1:
            if position[0] != -1:
                chosen_pair = []
                chosen_pair.append(position[0])
                chosen_pair.append(position[1])
                board.play_a_move(chosen_pair, list_next_moves1, list_crossed_way1, 'B')
                eval_score, _ = minimax(board, depth - 1, True, alpha, beta)
                board = copy.deepcopy(old_board)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = chosen_pair

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

        return min_eval, best_move

def variable_depth(num_options):
    if num_options < 6: return 5
    else: return 4

board = Board()
board.draw_table()
black_move_existing = white_move_existing = True

while(black_move_existing and white_move_existing):
    black_move_existing, num_options = ask_opponent_what_to_play()
    old_board = copy.deepcopy(board)
    depth = variable_depth(num_options)
    _, my_position = minimax(board, depth, True, float('-inf'), float('inf'))
    board = copy.deepcopy(old_board)

    list_next_moves, list_crossed_way, white_move_existing = board.next_moves('W')
    if white_move_existing and black_move_existing and my_position:
        board.play_a_move(my_position, list_next_moves, list_crossed_way, 'W')
        board.draw_table()

print("\nGame over! There're no more moves you can play.")
board.winner()
