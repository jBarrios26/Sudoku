board2 = [[7, 8, 4, 0, 0, 0, 2, 0, 0],
         [0, 0, 0, 0, 8, 4, 0, 9, 0],
         [0, 0, 6, 3, 2, 0, 0, 1, 0],
         [0, 9, 7, 0, 0, 0, 0, 8, 0],
         [8, 0, 0, 9, 0, 3, 0, 0, 2],
         [0, 1, 0, 0, 0, 0, 9, 5, 0],
         [0, 7, 0, 0, 4, 5, 8, 0, 0],
         [0, 3, 0, 7, 1, 0, 0, 0, 0],
         [0, 0, 8, 0, 0, 0, 0, 4, 0]]


def prettyPrint(board):
    for i in range(0, 9):
        line = ""
        for j in range(0, 9):
            line += str(board[i][j]) + " "
        print(line)


def checkRow(x, value, board):
    for col in range(0, 9):
        if board[x][col] == value:
            return False
    return True


def checkCol(y, value, board):
    for row in range(0, 9):
        if board[row][y] == value:
            return False
    return True


def subGridCoordenate(n):
    return (n // 3) * 3 + 1


def getSubGrid(x, y):
    return [subGridCoordenate(x), subGridCoordenate(y)]


def checkSubgrid(x, y, value, board):
    subgrid = getSubGrid(x, y)
    for row in range(-1, 2):
        for col in range(-1, 2):
            if (board[subgrid[0] + row][subgrid[1] + col] == value):
                return False
    return True


def isPossible(x, y, value, board):
    return checkRow(x, value, board) and checkCol(y, value, board) and checkSubgrid(x, y, value, board)


def solver(board):
    recursiveSolver(0, 0,board)
    return board


def recursiveSolver(row, col,board):
    if row == 8 and col == 9:
        return True
    elif row <= 8 and col == 9:
        return recursiveSolver(row + 1, 0,board)
    elif board[row][col] == 0:
        for k in range(1, 10):
            if isPossible(row, col, k, board):
                board[row][col] = k
                if recursiveSolver(row, col + 1,board):
                    return True
                board[row][col] = 0
    else:
        return recursiveSolver(row, col + 1,board)
    return False

