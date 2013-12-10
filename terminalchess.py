#-*- coding: utf-8 -*-
def init_bricks():
    h_brikker = {"A1":"Tårn", "B1":"Hest", "C1":"Løper","D1":"Dronning","E1":"Konge","F1":"Løper","G1":"Hest","H1":"Tårn",
                "A2":"Bonde", "B2":"Bonde", "C2":"Bonde", "D2":"Bonde", "E2":"Bonde", "F2":"Bonde", "G2":"Bonde", "H2":"Bonde"}
    s_brikker= {"A8":"Tårn", "B8":"Hest", "C8":"Løper","D8":"Dronning","E8":"Konge","F8":"Løper","G8":"Hest","H8":"Tårn",
                "A7":"Bonde", "B7":"Bonde", "C7":"Bonde", "D7":"Bonde", "E7":"Bonde", "F7":"Bonde", "G7":"Bonde", "H7":"Bonde"}
    return h_brikker, s_brikker

def chess_board(alle_brikker):
    board = [["0" for x in range(8)] for y in range(8)]
    for x in alle_brikker:
        matrix_x, matrix_y = brick_to_index(x)
        board[matrix_x][matrix_y] = alle_brikker[x][0]
    return board

def brick_to_index(brick):
    return (int(brick[1])-((int(brick[1])-4)*2), ord(brick[0])-65)

def index_to_brick(index):   
    return chr(index[1]+65)+str(8-index[0])

def get_straight(brick):
    x_pos, y_pos = brick_to_index(brick)
    upper = [(x, y_pos) for x in range(x_pos,-1,-1) if x < x_pos]
    lower = [(x, y_pos) for x in range(x_pos,8) if x > x_pos]
    left =  [(x_pos, y) for y in range(y_pos, -1, -1) if y < y_pos]
    right = [(x_pos, y) for y in range(y_pos, 8) if y > y_pos]
    return [upper, lower, left, right]

def get_adjacent(brick):
    x_pos, y_pos = brick_to_index(brick)
    upper_r = [(x_pos+c, y_pos-c) for c in range(-1, y_pos-8, -1) if 0 <= x_pos+c <= 7 and 0 <= y_pos-c <= 7]
    upper_l = [(x_pos-c, y_pos-c) for c in range(1, 8) if 0 <= y_pos-c <= 7 and 0 <= x_pos-c <= 7]
    lower_r = [(x_pos+c, y_pos+c) for c in range(1, 8) if 0 <= x_pos+c <= 7 and 0 <= y_pos+c <= 7]
    lower_l = [(x_pos+c, y_pos-c) for c in range(1, 8) if 0 <= x_pos+c <= 7 and 0 <= y_pos-c <= 7]
    return [upper_r, upper_l, lower_r, lower_l]

def legal_moves(brick, player_bricks, opponent_bricks):
    kind = player_bricks.get(brick, "z")[0]
    index = brick_to_index(brick)
    legal_moves = []
    if kind == "L":
        moves = get_adjacent(brick)
    elif kind == "D":
        moves = get_adjacent(brick)+get_straight(brick)
    elif kind == "T":
        moves = get_straight(brick)
    elif kind == "H":
        delta = [(-2, 1), (-2,-1), (2, 1), (2,-1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        moves =[[(x+index[0], y+index[1])] for x,y in delta if 0 <= x+index[0] <= 7 and 0 <= y+index[1] <= 7]
    elif kind == "K":
        delta = [(-1, 0),(1, 0),(1, 1),(0, 1),(-1, 1),(1, -1),(0, -1),(-1,-1)]
        moves =[[(x+index[0], y+index[1])] for x,y in delta if 0 <= x+index[0] <= 7 and 0 <= y+index[1] <= 7]
    elif kind == "B":
        #denne koden er alt for stygg
        moves = []
        if brick in hvite_brikker:
            attack = [(-1+index[0], -1+index[1]), (-1+index[0], 1+index[1])]
            move =   [(-1+index[0], index[1]), (-2+index[0], index[1])]
            if brick[1] != "2": del move[-1]
        else: 
            attack = [(1+index[0], -1+index[1]), (1+index[0], 1+index[1])]
            move = [(1+index[0], index[1]), (2+index[0], index[1])]
            if brick[1] != "7": del move[-1]
        for x in attack:
            this_brick = index_to_brick(x)
            if this_brick in opponent_bricks:
                legal_moves.append(this_brick)
        for x in move:
            this_brick = index_to_brick(x)
            if this_brick in player_bricks or this_brick in opponent_bricks:
                break
            else:
                legal_moves.append(this_brick)

        return legal_moves
    else:
        return []

    for direction in moves:
        for move in direction:
            this_brick = index_to_brick(move)
            if this_brick in player_bricks:
                break
            else:
                if this_brick in opponent_bricks:
                    legal_moves.append(this_brick)
                    break
                legal_moves.append(this_brick)

    return legal_moves
    
def print_board(board, hvite_brikker, svarte_brikker):
    white_symbols = {"K":"\u2654", "D":"\u2655", "T":"\u2656", "L":"\u2657", "H":"\u2658", "B":"\u2659"}
    black_symbols = {"K":"\u265A", "D":"\u265B", "T":"\u265C", "L":"\u265D", "H":"\u265E", "B":"\u265F"}
    white, black, red = "\033[38;05;15m", "\033[38;05;16m", "\033[38;05;196m"
    c, cc = 8, 0
    print(red+"\033[2J\033[H")
    print("     A B C D E F G H   "+"\n    "+"-"*17)
    for indexx, row in enumerate(board):
        cc += 1
        print(c, " | ", end='')
        for indexy, brick in enumerate(row):
            if index_to_brick((indexx, indexy)) in svarte_brikker.keys():
                print(black+black_symbols[brick]+red+" ", end='')
            elif index_to_brick((indexx, indexy)) in hvite_brikker.keys():
                print(white+white_symbols[brick]+red+" ", end='')
            else:
                if cc % 2 == 0: print(black+"■"+red+" ", end='')
                else: print(white+"■"+red+" ", end='')
            cc += 1
        print(" | ", c)
        c -= 1
    print("    "+"-"*17+"\n     A B C D E F G H   "+"\033[0m")

def make_new(start, end):
    if start in hvite_brikker:
        player_bricks = hvite_brikker.copy()
        opponent_bricks = svarte_brikker.copy()
    elif start in svarte_brikker:
        player_bricks = svarte_brikker.copy()
        opponent_bricks = hvite_brikker.copy()
    player_bricks[end] = player_bricks[start]
    del player_bricks[start]
    try: del opponent_bricks[end]
    except: pass
    return player_bricks, opponent_bricks

def check(player_bricks, opponent_bricks):
    king = [x[0] for x in player_bricks.items() if x[1]=="Konge"][0]
    for key in opponent_bricks.keys():
        moves = legal_moves(key, opponent_bricks, player_bricks)
        for move in moves:
            if move == king:
                return True
    return False

def checkmate(player_bricks, opponent_bricks):
    king = [x[0] for x in player_bricks.items() if x[1]=="Konge"][0]
    for key in player_bricks.keys():
        moves = legal_moves(key, player_bricks, opponent_bricks)
        for move in moves:
            a, b = make_new(key, move)
            if not check(a, b):
                return False
    return True

def move(player_bricks, opponent_bricks):
    while True:
        sjakk = check(player_bricks, opponent_bricks)
        if sjakk: print("Obs du er i sjakk")
        start = input("Fra:")
        end = input("Til:")
        if start not in player_bricks:
            continue
        if end not in legal_moves(start, player_bricks, opponent_bricks):
            continue
        a, b = make_new(start, end)
        if not check(a, b):
            player_bricks, opponent_bricks = make_new(start, end)
            if end[1] == ("1" or "8") and player_bricks[end][0] == "B":
                print("Du har muilighet til å forfremme bonden")
                print("D = Dronning\nT = Tårn\nL = Løper\nH = Hest\nB = Bonde")
                choice = ""
                while choice not in ["D", "T", "L", "H", "B"]:
                    choice = input("Velg en:")
                player_bricks[end] = choice
            break
    return player_bricks, opponent_bricks

def update():
    alle_brikker = dict(list(svarte_brikker.items()) + list(hvite_brikker.items()))
    board = chess_board(alle_brikker)
    print_board(board, hvite_brikker, svarte_brikker)

hvite_brikker, svarte_brikker = init_bricks()
alle_brikker = dict(list(svarte_brikker.items()) + list(hvite_brikker.items()))

def main():
    global alle_brikker, hvite_brikker, svarte_brikker
    board = chess_board(alle_brikker)
    print_board(board, hvite_brikker, svarte_brikker)
    while True:
        if checkmate(hvite_brikker, svarte_brikker):
            if check(hvite_brikker, svarte_brikker):
                print("Hvit er i sjakkmatt, svart vant")
            else:
                print("Svart spiller er i sjakkpatt...")
            break
        print("\033[38;05;15m", end="")
        hvite_brikker, svarte_brikker = move(hvite_brikker, svarte_brikker)
        update()
        print("\033[38;05;16m")
        if checkmate(svarte_brikker, hvite_brikker):
            if check(svarte_brikker, hvite_brikker):
                print("Svart er i sjakkmatt, hvit vant")
            else:
                print("Svart spiller er i sjakkpatt...")
            break
        svarte_brikker, hvite_brikker = move(svarte_brikker, hvite_brikker)
        update()
main()