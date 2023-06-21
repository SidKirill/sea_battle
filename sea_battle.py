from random import randint
class Dot:
    def __init__(self, h, v):
        self.h = h
        self.v = v

    def __eq__(self, other):
        return self.h == other.h and self.v == other.v

    def __repr__(self):
        return f'Dot({self.h}, {self.v})'

    class BoardException(Exception):
        pass

    class BoardOutException(BoardException):
        def __str__(self):
            return('Нельзя выстрелить за пределы доски')
    class BoardUsedException(BoardException):
        def __str__(self):
            return ('В эту клетку уже стреляли')
    class WrongShipException(BoardException):
        pass
class Boat:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        boat_dots = []
        for b in range(self.l):
            cur_h = self.bow.h
            cur_v = self.bow.v
            if self.o == 0:
                cur_h += b
            elif self.o == 1:
                cur_v += b

            boat_dots.append(Dot(cur_h, cur_v))
        return boat_dots
    def shoot(self, shot):
        return shot in self.dots
class Board:
    def __init__(self, hide=False, size=6):
        self.size = size
        self.hide = hide

        self.count = 0

        self.field = [['O'] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += " | 1 | 2 | 3 | 4| 5 | 6 |"
        for i in enumerate(self.field):
            res += f' \n{i+1} | " + " | ".join(row) + " |'

            if self.hide:
                res = res.replace("■", "O")

    def out(self, d):
        return not((0<= d.h < self.size) and (0 <= d.v < self.size))

    def contour(self, ship, verb = False):
        near = [(-1. -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:
            for dh, dv in ship.dots:
                cur = Dot(d.h + dh, d.v + dv)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.h][cur.v] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise WrongShipException()
        for d in ship.dots:
            self.field[d.h][d.v] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

    for ship in self.ships:
        if d in ship.dots:
            ship.lives -= 1
            self.field[d.h][d.v] = "X"
            if ship.lives == 0:
                self.count += 1
                self.contour(ship, verb=True)
                print("Ранил!")
                return False
            else:
                print("Потопил!")
                return True

    self.field[d.h][d.v] = "."
    print("Мимо!")
    return False

    def begin(self):
        self.busy = []
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    def ask(self):
        raise NotImplementedError()
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)
class Ai(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0, 5))
        print(f'Ходит компьютер: {d.h+1}{d.v+1}')
        return d
class User(Player):
    def ask(self):
        while True:
            cords = input('Ходит игрок: ').split()
            if len(cords) != 2:
                print('Введите 2 координаты')
                continue
            h, v = cords
            if not(h.isdigit()) or not (v.isdigit()):
                print('Введите числа')
                continue
            h, v = int(h), int(v)
            return Dot(h-1, v-1)
class Game:
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
                board.begin()
                return board
    def random_board(self):
        board = None
        while board in None:
            board = self.try_board()
        return board
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co_hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: h v ")
        print(" h - номер строки  ")
        print(" v - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print('-'*20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1
    def start(self):
        self.greet()
        self.loop()
g = Game()
g.start()