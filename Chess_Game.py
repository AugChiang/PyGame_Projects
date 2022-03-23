import pygame

player_sign = " U "
pc_sign = " P "
blank = "   " # require 3 len(blank included)
class Board:
    # width = block width
    # size = ? * ? board
    def __init__(self, link_num = 3, width = 3):
        self.turn = 0
        self.board = []
        self.col = []
        self.row = []
        self.dia_posi = []
        self.dia_neg = []
        self.link_num = link_num
        self.width = width
        self.blank_cnt = self.width ** 2

    def generate_board(self):
        for i in range(self.width):
            self.board.append([])
            self.row.append({player_sign:0,pc_sign:0})
            self.col.append({player_sign:0,pc_sign:0})
            for j in range(self.width):
                self.board[i].append(blank)
            #print(self.board[i])
        for k in range((self.width - self.link_num)*2 + 1):
            self.dia_posi.append({player_sign:0, pc_sign:0})
            self.dia_neg.append({player_sign:0, pc_sign:0})
        #print(f"temp row: {self.row}")
        #print(f"temp col: {self.col}")
        #print(f"temp dia: {self.dia}")
        #print(len(self.dia_posi))
        #print(len(self.dia_neg))

    def draw_board(self):
        for i in range(self.width):
            for j in range(len(self.board[0])):
                if j < self.width - 1:
                    print(self.board[i][j] + "|", end="")
                else:
                    print(self.board[i][j], end="")
                if j == self.width - 1:
                    print(" " + str(self.width - i))
            if i < self.width -1:
                print("--- " * self.width)
        # print the column indices at the last line
        for k in range(self.width):
            print(" " + str(k+1) + " "*2, end="")
        print("")

        #print(f"temp row: {self.row}")
        #print(f"temp col: {self.col}")
        #print(f"temp dia: {self.dia}")
        return self.board

    def is_valid(self,row,col):
        # index of the board.
        if abs(row - (self.width - 1) // 2) <= (self.width // 2):
            if abs(col - (self.width - 1) // 2) <= (self.width // 2):
                if self.board[row][col] == blank:
                    return True
        return False


    def fill_in(self):
        while True:
            print("Your turn!")
            # de Cartesian Coordinates.
            try:
                fill_x = int(input(f"Place the x (1~{self.width}): "))
                fill_y = int(input(f"Place the y (1~{self.width}): "))
                if self.is_valid(self.width - fill_y, fill_x - 1): # convert to board index
                    print(f"You place at pos ({fill_x},{fill_y})")
                    self.board[self.width - fill_y][fill_x - 1] = player_sign
                    self.blank_cnt -= 1
                    self.update_board_state(self.board, fill_x, fill_y)
                    self.draw_board()
                    break
                print("Invalid input.")
            except Exception:
                print("Format error.")

    def is_full(self):
        if self.blank_cnt == 0:
            return True
        return False

    def is_sb_win(self):
        #print(f"temp row: {self.row}")
        #print(f"temp col: {self.col}")
        #print(f"temp dia: {self.dia}")
        # Check row and col
        for i in range(len(self.row)):
            if self.row[i][player_sign] == self.link_num or self.col[i][player_sign] == self.link_num:
                print("Player win.")
                return True
            if self.row[i][pc_sign] == self.link_num or self.col[i][pc_sign] == self.link_num:
                print("PC win.")
                return True
        # Check diagonal
        for dia_p in self.dia_posi:
            if dia_p[player_sign] == self.link_num:
                print("Player win.")
                return True
            if dia_p[pc_sign] == self.link_num:
                print("PC win.")
                return True
        for dia_n in self.dia_neg:
            if dia_n[player_sign] == self.link_num:
                print("Player win.")
                return True
            if dia_n[pc_sign] == self.link_num:
                print("PC win.")
                return True

        return False

    def update_board_state(self, board, fill_x, fill_y):
        # input = fill_x, fill_y
        # board index
        row, col = self.width - fill_y, fill_x - 1
        dia_posi_i = fill_x - fill_y
        dia_neg_i = fill_x + fill_y - 1 - self.width # shifted


        if board[row][col] == player_sign:

            self.row[row][player_sign] = self.row[row][player_sign] + 1
            self.col[col][player_sign] = self.col[col][player_sign] + 1
            # y = x +/- link_num diagonal line (positive slope)
            # from down-right to top-left is {+link_num ~ -link_num}
            if -self.link_num <= dia_posi_i <= self.link_num:
                self.dia_posi[dia_posi_i][player_sign] = self.dia_posi[dia_posi_i][player_sign] + 1
            # x+y = link_num+1 ~ link_num+1+width
            # from left down to right top is {-link_num ~ +link_num}
            if self.link_num - self.width <= dia_neg_i <= self.link_num:
                self.dia_posi[dia_neg_i][player_sign] = self.dia_posi[dia_neg_i][player_sign] + 1

        elif board[row][col] == pc_sign:
            self.row[row][pc_sign] = self.row[row][pc_sign] + 1
            self.col[col][pc_sign] = self.col[col][pc_sign] + 1
            # y = x +/- link_num diagonal line (positive slope)
            # from down-right to top-left is {+link_num ~ -link_num}
            if -self.link_num <= dia_posi_i <= self.link_num:
                self.dia_posi[dia_posi_i][pc_sign] = self.dia_posi[dia_posi_i][pc_sign] + 1
            # x+y = link_num+1 ~ link_num+1+width
            # from left down to right top is {-link_num ~ +link_num}
            if self.link_num - self.width <= dia_neg_i <= self.link_num:
                self.dia_posi[dia_neg_i][pc_sign] = self.dia_posi[dia_neg_i][pc_sign] + 1
        else:
            return True


    def pc_fill_in(self):
        while True:
            # de Cartesian Coordinates.
            print("PC's turn!")
            try:
                fill_x = int(input(f"Place the x (1~{self.width}): "))
                fill_y = int(input(f"Place the y (1~{self.width}): "))
                if self.is_valid(self.width - fill_y, fill_x - 1): # convert to board index
                    print(f"PC place at pos ({fill_x},{fill_y})")
                    self.board[self.width - fill_y][fill_x - 1] = pc_sign
                    self.blank_cnt -= 1
                    self.update_board_state(self.board, fill_x, fill_y)
                    self.draw_board()
                    break
                print("Invalid input.")
            except Exception:
                print("Format error.")

def win_draw(window, board, win_width):
    window.fill(white)
    draw_lines(window, board, win_width)

def draw_lines(window, board, win_width):
    gap = win_width // board.width
    for i in range(len(board.col)):
        pygame.draw.line(window, grey, (0, i*gap), (win_width, i*gap))
        pygame.draw.line(window, grey, (i*gap, 0), (i*gap, win_width))


def main(board):
    if board.link_num > board.width:
        print("Can not start the game by this condition.")
        return -1
    board.generate_board()
    board.draw_board()
    print(f"The first one who links {board.link_num} win!")
    while True:
        '''
        for i in range(len(self.row)):
            print(f"temp row {self.width - i}: {self.row[i]}")
        print("---------------------------------")
        for j in range(len(self.col)):
            print(f"temp col {j + 1}: {self.col[j]}")
        print("---------------------------------")
        for k in range(len(self.dia)):
            print(f"temp dia {k}: {self.dia[k]}")
        print("---------------------------------")
        '''
        board.fill_in()
        if board.is_sb_win() or board.is_full():
            break
        board.pc_fill_in()
        if board.is_sb_win() or board.is_full():
            break
        board.turn += 1
    print(f"Total turns: {board.turn}")


board = Board(5,10)
main(board)

