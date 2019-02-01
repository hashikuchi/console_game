from subprocess import call
from getch import getch
import time
from copy import copy

class othello:
    def __init__(self):
        self.height = 8
        self.width = 8
        self.empty = "·"
        self.board = [[self.empty for _ in range(self.width)] for _ in range(self.height)]
        self.black = "●"
        self.white = "○"
        self.turn = self.black
        self.opponent = self.white
        self.py = 0
        self.px = 0

    def __str__(self, key=True):
        call("clear")
        ret = ""
        for i in range(self.height):
            tmp = copy(self.board[i])
            if self.py == i and (key is True):
                tmp[self.px] = "*"
            ret += " ".join(tmp) + "\n"
        ret += "turn: " + self.turn + "\n"
        ret += "how to play\n"
        ret += "a : ←, "
        ret += "w : ↑, "
        ret += "d : →, "
        ret += "s : ↓, "
        ret += "Enter : put\n"
        ret += "Q : quit game"
        return ret
    
    def start(self):
        self.board[3][3] = self.white
        self.board[4][4] = self.white
        self.board[3][4] = self.black
        self.board[4][3] = self.black
        print(self)
        return
    
    def change_turn(self):
        self.turn = [self.black, self.white][self.turn == self.black]
        self.opponent = [self.black, self.white][self.turn == self.black]

    def canPut_line(self, h, w, x, y):
        h += y
        w += x
        if (0<=h<self.height and 0<=w<self.width) is False:
            return False
        elif self.board[h][w] != self.opponent:
            return False
        
        h += y
        w += x
        while 0<=h<self.height and 0<=w<self.width:
            # print(h, w)
            if self.board[h][w] == self.turn:
                return True
            h += y
            w += x
        return False
    
    def canPut(self, h, w):
        if self.board[h][w] != self.empty:
            return False
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                if self.canPut_line(h, w, x, y) is True:
                    return True
        return False
    
    def check(self):
        for i in range(self.height * self.width):
            if self.board[i//self.width][i%self.width] != self.empty:
                continue
            elif self.canPut(i//self.width, i%self.width) is True:
                return True
        return False
    
    def changeColor(self, py, px):
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                elif self.canPut_line(py, px, x, y) is False:
                    continue
                ty = py + y
                tx = px + x
                while self.board[ty][tx] != self.turn:
                    self.board[ty][tx] = self.turn
                    ty += y
                    tx += x
        return

    def count(self, color):
        return sum(A.count(color) for A in self.board)


game = othello()
game.start()
t = 0
while True:
    B = game.count(game.black)
    W = game.count(game.white)
    if B == 0 or W == 0:
        break
    elif B + W == game.width * game.height:
        break
    if game.check() is False:
        print("You cannot put!!")
        print("Change turn in 2 seconds")
        time.sleep(2)
        game.change_turn()
        print(game)
        continue

    while True:
        get = getch()
        if get == "a":
            game.px = max(0, game.px - 1)
        elif get == "d":
            game.px = min(game.width - 1, game.px + 1)
        elif get == "w":
            game.py = max(0, game.py - 1)
        elif get == "s":
            game.py = min(game.height - 1, game.py + 1)
        elif get == "Q":
            print("Quit")
            exit()
        elif get == "\n":
            break
        print(game)
    
    if game.canPut(game.py, game.px) is False:
        print("You cannot put here.")
        continue
    
    game.board[game.py][game.px] = game.turn
    game.changeColor(game.py, game.px)
    game.change_turn()
    print(game)

print(game.__str__(key=False))
B = game.count(game.black)
W = game.count(game.white)
print("Black", B, "-", W, "White")
if B == W:
    print("Draw!!")
elif B > W:
    print("Black Win!!")
elif W > B:
    print("White Win!!")