import random

"""
self.gameGrid = [
    [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [4, 4, 4, 5, 5, 5, 6, 6, 6],
    [4, 4, 4, 5, 5, 5, 6, 6, 6],
    [4, 4, 4, 5, 5, 5, 6, 6, 6],
    [7, 7, 7, 8, 8, 8, 9, 9, 9],
    [7, 7, 7, 8, 8, 8, 9, 9, 9],
    [7, 7, 7, 8, 8, 8, 9, 9, 9],
]
            ⬇️ _to_triplets()

triplets = [
    [ [1, 1, 1], [2, 2, 2], [3, 3, 3] ], 
    [ [1, 1, 1], [2, 2, 2], [3, 3, 3] ], 
    [ [1, 1, 1], [2, 2, 2], [3, 3, 3] ], 
    [ [4, 4, 4], [5, 5, 5], [6, 6, 6] ], 
    [ [4, 4, 4], [5, 5, 5], [6, 6, 6] ], 
    [ [4, 4, 4], [5, 5, 5], [6, 6, 6] ], 
    [ [7, 7, 7], [8, 8, 8], [9, 9, 9] ], 
    [ [7, 7, 7], [8, 8, 8], [9, 9, 9] ], 
    [ [7, 7, 7], [8, 8, 8], [9, 9, 9] ]
]
            ⬇️ _flatten()

flattened = [
    [1, 1, 1], [2, 2, 2], [3, 3, 3], 
    [1, 1, 1], [2, 2, 2], [3, 3, 3], 
    [1, 1, 1], [2, 2, 2], [3, 3, 3], 
    [4, 4, 4], [5, 5, 5], [6, 6, 6], 
    [4, 4, 4], [5, 5, 5], [6, 6, 6], 
    [4, 4, 4], [5, 5, 5], [6, 6, 6], 
    [7, 7, 7], [8, 8, 8], [9, 9, 9], 
    [7, 7, 7], [8, 8, 8], [9, 9, 9], 
    [7, 7, 7], [8, 8, 8], [9, 9, 9]
]
            ⬇️ _to_subgrids()

subgrids = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],            1, 1, 1, | 2, 2, 2, | 3, 3, 3
    [2, 2, 2, 2, 2, 2, 2, 2, 2],            1, 1, 1, | 2, 2, 2, | 3, 3, 3
    [3, 3, 3, 3, 3, 3, 3, 3, 3],            1, 1, 1, | 2, 2, 2, | 3, 3, 3
                                            -----------------------------
    [4, 4, 4, 4, 4, 4, 4, 4, 4],            4, 4, 4, | 5, 5, 5, | 6, 6, 6
    [5, 5, 5, 5, 5, 5, 5, 5, 5],     ==     4, 4, 4, | 5, 5, 5, | 6, 6, 6
    [6, 6, 6, 6, 6, 6, 6, 6, 6],            4, 4, 4, | 5, 5, 5, | 6, 6, 6
                                            -----------------------------
    [7, 7, 7, 7, 7, 7, 7, 7, 7],            7, 7, 7, | 8, 8, 8, | 9, 9, 9
    [8, 8, 8, 8, 8, 8, 8, 8, 8],            7, 7, 7, | 8, 8, 8, | 9, 9, 9
    [9, 9, 9, 9, 9, 9, 9, 9, 9]             7, 7, 7, | 8, 8, 8, | 9, 9, 9
]

"""

class GridError(Exception):
    pass

class Sudoku:
    def __init__(self, gameGrid):
        self.gameGrid = gameGrid

    def run(self):
        self.generate_grid()
        self.print_grid()
        self.check_state()
        self.user_control()

    def generate_grid(self) -> None:
        for _ in range(random.randint(17, 41)):
            y, x = random.randint(0,8), random.randint(0,8)
            number = random.randint(1,9)
            try:
                self.validate_and_insert(number=number, y=y, x=x)
            except GridError:
                _ -= 1

    def print_grid(self) -> None:
        iterator: int = 0

        print("\n\t0  1  2    3  4  5    6  7  8")
        print("\t-----------------------------\n")

        for i in self.gameGrid:
            print(" ", iterator,' |  ', end="")
            row_iter: int = 0
            for j in i:
                print(f"{j}  ", end="")
                if (row_iter+1) % 3 == 0: print("  ", end="")
                row_iter+=1

            if (iterator+1) % 3 == 0: print('\n')
            else: print()

            iterator+=1

    def user_control(self) -> None:
        number = int(input("[>] Wähle eine Zahl: "))
        y = int(input("[>] Wähle eine Stelle auf der y-Achse: "))
        x = int(input("[>] Wähle eine Stelle auf der x-Achse: "))
        try:
            self.insert(number=number, y=y, x=x)
        except GridError as GE:
            print(GE)
        self.update()

    def update(self) -> None:
        self.check_state()
        self.print_grid()
        self.user_control()

    def check_state(self) -> None:
        if 'x' not in self._flatten(self.gameGrid):
            command = input("[?] Das Spielfeld is voll. Überprüfen? [y/n]: ")
            if command == "y" or command == "yes":
               if self.validate_all():
                    print("[✓] Gewonnen!")
                    exit()
            elif command == "n" or command == "no":
                self.user_control()
    
    def validate_all(self) -> bool:
        for i in range(9):
            if not self._is_unique(self.gameGrid[i]):
                print(f"[x] Doppelte Zahl in Zeile {i}!")
                return False
            if not self._is_unique(self._get_column(x=i, grid=self.gameGrid)):
                print(f"[x] Doppelte Zahl in Spalte {i}!")
                return False
            if not self._is_unique(self._get_subgrids(self.gameGrid)[i]):
                print(f"[x] Doppelte Zahl in Subgrid {i}!")
                return False
        return True
                    
    def validate(self, number: int, y: int, x: int) -> None:
        if self.validate_subgrid(number=number, y=y, x=x):
            if self.validate_row(number=number, y=y):
                if self.validate_column(number=number, x=x, column=self._get_column(x=x, grid=self.gameGrid)):
                    self.insert(number=number, y=y, x=x)
    
    def insert(self, number: int, y: int, x: int) -> None:
        if (number > 9 or number < 1) or (y > 8 or y < 0) or (x > 8 or x < 0):
            raise GridError("[x] Falsche Stelle oder Zahl! Zahlen 1 - 9, Stellen 0 - 8")
        self.gameGrid[y][x] = number
                        
    def _is_unique(self, lst: list) -> bool:
        if len(lst) > len(set(lst)): return False
        return True

    def get_absolute_index(self, y: int, x:int, grid: list) -> int:
        grid = self._flatten(grid)
        if y != 0:
            index = (y-1)*8 + x
        else:
            index = x
        return index

    def validate_subgrid(self, number: int, y: int, x:int) -> bool:
        absolute_index = self.get_absolute_index(y=y, x=x, grid=self.gameGrid)
        subgrid_number = (absolute_index % 9)//3+3*(absolute_index//27)
        subgrids = self._get_subgrids(grid=self.gameGrid)
        if number in subgrids[subgrid_number]:
            return False
        return True

    def validate_row(self, number: int, y: int) -> bool:
        if number in self.gameGrid[y]: return False 
        return True

    def validate_column(self, number: int, x: int, column: list) -> bool:
        if number in column: return False
        return True

    def _get_column(self, x: int, grid: list) -> list:
        _columnList = []
        [_columnList.append(i[x]) for i in grid]
        return _columnList

    def _get_subgrids(self, grid: list) -> list:
        chunks: list = self._to_chunks(grid=grid)
        
        flattened: list = self._flatten(grid=chunks)
        
        subgrids: list = []
        start, end = 0, 3
        for _ in range(3):
            for j in range(start, end):
                subgrids.append(flattened[j] + flattened[j+3] + flattened[j+6])
            start, end = start+9, end+9 
        
        return subgrids

    def _flatten(self, grid: list) -> list:
        flattened: list = []
        for i in grid:
            for j in i:
                flattened.append(j)
        return flattened

    def _to_chunks(self, grid: list) -> list:
        chunks = []
        for i in grid:
            chunks.append([i[:3], i[3:6], i[6:]])
        return chunks