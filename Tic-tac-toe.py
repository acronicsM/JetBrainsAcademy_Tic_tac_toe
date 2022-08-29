class TicTacToe:
    """A class to represent TicTacToe game.

     Attributes
     ----------
         grid : List of game cells.
         symbol_gamer1 : symbol representation of player #1's completed moves
         symbol_gamer2 : symbol representation of player #2's completed moves
         free_cell : symbol, empty cell
     """

    errors = ['You should enter numbers!',
              'Coordinates should be from 1 to 3!',
              'This cell is occupied! Choose another one!']

    statuses = ['Game not finished', 'Impossible', 'X wins', 'O wins', 'Draw']

    def __init__(self, size: int, symbol_gamer1: str = 'X', symbol_gamer2: str = 'O', free_cell: str = ' '):

        null_line = free_cell*size
        self.grid = [[*null_line] for _ in null_line]
        self.symbol_gamer1 = symbol_gamer1
        self.symbol_gamer2 = symbol_gamer2
        self.free_cell = free_cell
        self.status_game = 0
        self.gamer_1_move = True

    def update(self, step_game: str):
        """
       Updates the grid with the new status passed in argument 'cells'.

       Parameters
       ----------
       step_game : str
           Status of all the cells of the game.
           Accepted symbols are 'X', 'O' and '_'
       """
        size = len(self.grid)
        self.grid = [list(step_game[i:i + size]) for i in range(0, size**2, size)]
        self.update_status()

    def update_status(self):
        """
            Returns the current game status
        """

        grid = self.grid
        symbol_gamer1 = self.symbol_gamer1
        symbol_gamer2 = self.symbol_gamer2
        free_cell = self.free_cell

        size = len(grid)

        win1 = win2 = False

        column1 = [True for _ in range(size)]
        column2 = [True for _ in range(size)]

        line1 = line2 = True
        free_cell_count = count_1 = count_2 = 0

        diagonal1_gamer1 = diagonal2_gamer1 = True
        diagonal1_gamer2 = diagonal2_gamer2 = True

        diagonal1, diagonal2 = 0, size-1

        for line_i in grid:
            pass
            for column_index, colum_i in enumerate(line_i):
                sg1 = colum_i == symbol_gamer1
                sg2 = colum_i == symbol_gamer2

                free_cell_count += 1 if colum_i == free_cell else 0
                count_1 += 1 if sg1 else 0
                count_2 += 1 if sg2 else 0

                if not win1:
                    line1 = line1 and sg1
                    column1[column_index] = column1[column_index] and sg1
                    if column_index == diagonal1:
                        diagonal1_gamer1 = diagonal1_gamer1 and sg1

                    if column_index == diagonal2:
                        diagonal2_gamer1 = diagonal2_gamer1 and sg1

                if not win2:
                    line2 = line2 and sg2
                    column2[column_index] = column2[column_index] and sg2
                    if column_index == diagonal1:
                        diagonal1_gamer2 = diagonal1_gamer2 and sg2

                    if column_index == diagonal2:
                        diagonal2_gamer2 = diagonal2_gamer2 and sg2

            win1, win2 = line1, line2
            diagonal1 += 1
            diagonal2 -= 1

        win1 = win1 or any(column1) or diagonal1_gamer1 or diagonal2_gamer1
        win2 = win2 or any(column2) or diagonal1_gamer2 or diagonal2_gamer2

        impossible = abs(count_1 - count_2) > 1

        status = 0

        if (win1 and win2) or impossible:
            status = 1
        elif win1:
            status = 2
        elif win2:
            status = 3
        elif not free_cell_count:
            status = 4

        self.status_game = status

    def __str__(self):
        """
        Returns a representation of the current state of the game with the status
        """

        return self.painting() + self.statuses[self.status_game]

    def painting(self):
        """
        Return a representation of the current status of the game.
        """
        lb = '\n'
        dashes = '-' * (len(self.grid) ** 2)

        return dashes + lb + lb.join([f'| {" ".join(i) } |' for i in self.grid]) + lb + dashes + lb

    def next_step(self):
        step_symbol = self.symbol_gamer1 if self.gamer_1_move else self.symbol_gamer2
        doit = True
        while doit:
            command = input("next step: ").split()
            check_command = self.checking_command(command)
            if check_command <= len(self.errors):
                print(self.errors[check_command])
            else:
                step_line, step_column = map(int, command)

                self.grid[step_line - 1][step_column - 1] = step_symbol
                self.gamer_1_move = not self.gamer_1_move
                doit = False

        self.update_status()

    def checking_command(self, command: list):
        all_digit = all(isinstance(char, int) or isinstance(char, str) and char.isdigit() for char in command)
        if len(command) != 2 or not all_digit:
            return 0

        size = len(self.grid)
        step_line, step_column = map(int, command)
        if (step_line < 1 or step_line > size) or (step_column < 1 or step_column > size):
            return 1
        elif self.grid[step_line - 1][step_column - 1] != self.free_cell:
            return 2

        return 99


def run_game(size_game):
    game = TicTacToe(size_game)

    while game.status_game < 2:
        print(game.painting())
        game.next_step()
    else:
        print(game)


if __name__ == '__main__':
    run_game(3)
