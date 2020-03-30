import requests

url = 'http://www.cs.utep.edu/cheon/ws/sudoku/new/?size={}&level={}'


def ask_sudoku(level, size=9, ):
    response = requests.get(url.format(size, level))
    if response.status_code == 200:
        return response.json()
    else:
        return None


def build_sudoku(suduko_board):
    if suduko_board is not None:
        board = empty_sudoku()
        for elem in suduko_board['squares']:
            x = int(elem['x'])
            y = int(elem['y'])
            value = int(elem['value'])
            board[x][y] = value
        return board


def empty_sudoku():
    result = []
    for i in range(0, 9):
        aux = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        result.append(aux)
    return result


def create(level):
    return build_sudoku(ask_sudoku(level))
