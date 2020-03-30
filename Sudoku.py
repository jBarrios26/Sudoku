import pygame
import SudokuSolver
import SudokuDownloader

FONT = None

# colors:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Grid:
    last_change = None

    def __init__(self, game, size,board):
        self.game = game
        self.board = board
        self.size = size
        self.cubes = self.create_cubes()
        self.selected = None


    def solve(self):
        aux = SudokuSolver.solver(self.board)
        for i in range(0, 9):
            for j in range(0, 9):
                self.cubes[j][i].value = aux[i][j]
                self.cubes[j][i].temp = 0

    def create_cubes(self):
        grid = []
        for i in range(0, 9):
            aux = []
            for j in range(0, 9):
                aux.append(Cube(i, j, self.size // 9, self.board[j][i]))
            grid.append(aux)
        return grid

    def temporal(self, value):
        if self.selected is not None and not self.cubes[self.selected[0]][self.selected[1]].final:
            x = self.selected[0]
            y = self.selected[1]
            self.cubes[x][y].temp = value

    def delete(self):
        square = self.cubes[self.selected[0]][self.selected[1]]
        if not square.initial:
            square.value = 0
            square.final = False
            self.board[square.row][square.col] = 0

    def submit(self, value):
        if self.selected is not None:
            x = self.selected[0]
            y = self.selected[1]

            if SudokuSolver.isPossible(y, x, value, self.board) and not self.cubes[x][y].final:
                self.last_change = [[x, y], True]
                self.cubes[x][y].value = value
                self.board[y][x] = value
                self.cubes[x][y].temp = 0
                self.cubes[x][y].final = True
            else:
                self.last_change = [[x, y], False]

    def draw(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if (i, j) == self.selected:
                    if self.last_change is not None and i == self.last_change[0][0] and j == self.last_change[0][1]:
                        self.cubes[i][j].draw(self.game, self.last_change, True)
                    else:
                        self.cubes[i][j].draw(self.game, None, True)
                self.cubes[i][j].draw(self.game, None)
        self.last_change = None

    def get_cell(self, pos):
        x = pos[0] // (self.size // 9)
        y = pos[1] // (self.size // 9)
        return x, y

    def select(self, pos):
        if 0 <= pos[0] < 9 and 0 <= pos[1] < 9 and not self.cubes[pos[0]][pos[1]].initial:
            self.selected = pos

    def summit_value(self, value):
        x = self.selected[0]
        y = self.selected[1]

        if SudokuSolver.isPossible(x, y, value, self.board):
            self.cubes[x][y].value = value

    def complete(self):
        for i in self.board:
            for j in i:
                if j == 0:
                    return False
        return True


class Cube:

    def __init__(self, i, j, size, value):
        self.row = i
        self.col = j
        self.size = size
        self.value = value
        self.temp = 0
        self.initial = True if value != 0 else False
        self.final = False

    def print(self, win, pos, color, value):
        text = FONT.render(str(value), True, color)
        text_rect = text.get_rect()
        text_rect.center = (pos[0] + (self.size // 2), pos[1] + (self.size // 2))
        win.blit(text, text_rect)

    def put_text(self, win, pos):
        if self.value != 0 and self.temp == 0:
            self.print(win, pos, BLACK, self.value)
        elif self.value == 0 and self.temp != 0:
            self.print(win, pos, GRAY, self.temp)

    def draw(self, game, changed, sel=False):
        x = self.row * self.size
        y = self.col * self.size
        thickness = 3 if not sel else 8
        rect_color = BLACK if changed is None else ((255, 0, 0) if not changed[1] else (0, 255, 0))
        pygame.draw.rect(game, rect_color, (x, y, self.size, self.size), thickness)
        self.put_text(game, (x, y))


def check_exit(event):
    if event.type == pygame.QUIT:
        return False
    return True


def check_keys(event, board):
    if event.type == pygame.KEYDOWN:
        if 48 < event.key <= 57:
            key = event.key - 48
            board.temporal(key)
        elif event.key == pygame.K_RETURN:
            x, y = board.selected
            if board.cubes[x][y] != 0:
                board.submit(board.cubes[x][y].temp)
            if board.complete():
                return False
        elif event.key == pygame.K_DELETE:
            board.delete()
        elif event.key == pygame.K_SPACE:
            board.solve()
            return False
    return True


def check_mouse(event, board):
    if event.type == pygame.MOUSEBUTTONUP:
        pos = board.get_cell(event.pos)
        board.select(pos)


def get_timer(time):
    minutes = int((time / 1000) / 60)
    seconds = int((time / 1000) % 60)
    return str.format("{:0>2}:{:02}", minutes, seconds)


def print_timer(game, time):
    text = FONT.render(get_timer(time), True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (405, 850)
    game.blit(text, text_rect)


def draw(game, board, time):
    game.fill((255, 255, 255))
    print_timer(game, time)
    board.draw()
    pygame.display.update()

def start():
    level = int(input("Escoja un nivel de 1 a 3: "))
    board = SudokuDownloader.create(level)
    return board

def main():
    global FONT
    board = start()
    pygame.init()
    FONT = pygame.font.Font(None, 76)
    game = pygame.display.set_mode((810, 900))
    pygame.display.set_caption("Sudoku")
    board = Grid(game, 810, board)
    alive = True
    clock = pygame.time.Clock()
    time = clock.get_time()
    while alive:
        time += clock.get_time()
        for event in pygame.event.get():
            alive = check_exit(event) and check_keys(event, board)
            check_mouse(event, board)
        draw(game, board, time)
        clock.tick(60)

    wait = True
    while wait:
        for event in pygame.event.get():
            wait = check_exit(event)
    pygame.quit()


main()
