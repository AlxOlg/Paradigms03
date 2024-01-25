import random
import time

# Вывод игры в терминал.
def print_game():
    col_count = 0 # Счетчик столбцов для прехода на следущую строку.
    print("\033[H\033[J") # "Очистка терминала".
    for i in range(len(cells)): # Цикл по списку значений клеток.
        if cells[i] == 1: # Если значение соответствует человеку.
            print("\033[33m{}\033[0m".format(PLAYERS[1]), end='') # Печать символа игрока.
        elif cells[i] == 2: # Если значение соответствует победителю-человеку.
            print("\033[31m{}\033[0m".format(PLAYERS[1]), end='') # Печать символа победителя.
        elif cells[i] == -1: # Если значение соответствует ИИ.
            print("\033[33m{}\033[0m".format(PLAYERS[-1]), end='') # Печать символа игрока.
        elif cells[i] == -2: # Если значение соответствует победителю-ИИ.
            print("\033[31m{}\033[0m".format(PLAYERS[-1]), end='') # Печать символа победителя.
        else: # Иначе - пустая клетка.
            if winner == 0: # В процессе игры.
                print(DISPLAY[i], end='') # Номер клетки.
            else: # В финале игры.
                print(' ', end='') # Пробел вместо номера клетки.
        if col_count == 2:
            print() # Переход на следущую строку.
            if i < 6:
                print('---------') # Горизонтальные линии игрового поля.
            col_count = 0
        else:
            print(' | ', end='')  # Вертикальные линии игрового поля.
            col_count += 1
    print()

# Получить список индексов пустых клеток.
def get_empty():
    empty.clear()
    for i in range(len(cells)):
        if cells[i] == 0:
            empty.append(i)

# Ход человека.
def move_human():
    index_move = -1 # Несуществующий индекс хода.
    while index_move == -1: # Пока индекс хода не присвоен.
        print_game() # Обновление игры в терминале.
        key_move = input(f"Ваш ход '{PLAYERS[1]}': ") # Запрос хода.
        # Проверка допустимости хода.
        for i in empty:
            if key_move == DISPLAY[i]:
                index_move = i
                return index_move

# Ход ИИ.
def move_ai():
    print('Думаю...')
    time.sleep(1) # Типа думает.
    if -2 in sum_lines: # Если ИИ занял две клетки линии из трех.
        return find_one_empty(-2) # Определить свободную клетку линии.
    elif 2 in sum_lines: # Если человек занял две клетки линии из трех.
        return find_one_empty(2) # Определить свободную клетку линии.
    elif 4 in empty: # Если центральная клетка свободна.
        return 4 # Занять центральную клетку.
    else: # Здесь можно сделать ИИ умнее (не в этот раз).
        return empty[random.randint(0, len(empty)-1)] # Случайная клетка из свободных.

# Получить список сумм значений клеток выигрышных комбинаций.
def get_sum():
    sum_lines.clear()
    for i in range(len(LINES)):
        sum_lines.append(0)
        for j in range(len(LINES[i])):
            sum_lines[i] += cells[LINES[i][j]]

# Определение свободной клетки линии.
def find_one_empty(value):
    for i in range(len(LINES)):
        if sum_lines[i] == value:
            for j in range(len(LINES[i])):
                if cells[LINES[i][j]] == 0:
                    return LINES[i][j]

# Проверка выигрыша.
def winning_check():
    global winner
    if 3 in sum_lines or -3 in sum_lines:
        show_winner()
        winner = turn_order
        
# Показать комбинацию победителя.
def show_winner():
    for i in range(len(sum_lines)):
        if abs(sum_lines[i]) == 3:
            for j in range(len(LINES[i])):
                cells[LINES[i][j]] *= 2 if abs(cells[LINES[i][j]]) < 2 else None
    print_game()

# Константы.
# Символы игроков.
PLAYERS = {1: 'X', -1: 'O'}
# Результат игры.
RESULT = {0: 'НИЧЬЯ', 1: 'Поздравляю с победой!', -1: 'Увы...'}
# Отображение клеток игрового поля в соответствии с цифровой клавиатурой.
DISPLAY = ('7', '8', '9', '4', '5', '6', '1', '2', '3', )
# Выигрышные комбинации.
LINES = (
    (0, 1, 2), 
    (3, 4, 5), 
    (6, 7, 8), 
    (0, 3, 6), 
    (1, 4, 7), 
    (2, 5, 8), 
    (0, 4, 8), 
    (2, 4, 6), 
)

# Переменные.
winner = 0 # Победитель: 0 - нет, 1 - человек, -1 - ИИ.
# Значения клеток:
# 0 - пустая, 1 - человек, -1 - ИИ, 2 и -2 победитель соответственно.
cells = [0 for i in range(9)]
empty = [] # Свободные клетки.
sum_lines = [] # Суммы значений клеток выигрышных комбинаций.

# Основной процесс.
def main():
    global turn_order # Очередь хода: 1 - человек, -1 - ИИ.
    turn_order = 1
    while 0 in cells and winner == 0: # Пока есть свободные клетки и нет победителя.
        get_empty() # Получить список индексов свободных клеток.
        if turn_order == 1: # Ход человека.
            move = move_human()
        else: # Ход ИИ.
            move = move_ai()
        cells[move] = turn_order # Заполнение клетки значением соответствующим игроку.
        print_game() # Обновление игры в терминале.
        get_sum()# Получить список сумм значений клеток выигрышных комбинаций.
        winning_check() # Проверка выигрыша.
        turn_order *= -1 # Переход очереди хода.
    print(RESULT[winner])

if __name__ == "__main__":
    main()
