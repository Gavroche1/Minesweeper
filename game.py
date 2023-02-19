""" This file contains the class which manages the game """

import copy
import random


class Game:
    """
        This class manages the game : the grid and the user's actions.
        The grid contains :
            - " " : for nothing
            - "0" : for a case which is already visited
            - "l" : for a landmine
            - "f" : for a flag
            - "h" : for a flag on a landmine
            - number : show the landmines around
    """

    def __init__(self, nb_landmine, col, row):
        """ Initialize """

        self._grid = []
        self.col = col
        self.row = row
        self.is_lost = False
        self.nb_landmine = nb_landmine
        self.create_grid()

    def replay(self):
        """ Reset the grid """

        self.create_grid()
        self.is_lost = False

    @property
    def grid(self):
        """ Return the grid that is displayed to the user """

        grid_user = copy.deepcopy(self._grid)

        if not self.is_lost:
            for i in range(len(self._grid)):
                for j in range(len(self._grid[0])):
                    if self._grid[i][j] == "l":
                        grid_user[i][j] = " "
                    else:
                        grid_user[i][j] = self._grid[i][j]
        else:
            for i in range(len(self._grid)):
                for j in range(len(self._grid[0])):
                    if self._grid[i][j] == "h":
                        grid_user[i][j] = "l"
                    else:
                        grid_user[i][j] = self._grid[i][j]

        return grid_user

    def test_win(self):
        """ Return True if the user has win """

        for i in range(self.row):
            for j in range(self.col):
                if self._grid[i][j] in (" ", "f"):
                    return False

        return True

    def add_flag(self, posx, posy):
        """ When the user wants to add a flag """

        if self._grid[posy][posx] == "l":
            self._grid[posy][posx] = "h"
        elif self._grid[posy][posx] == "f":
            self._grid[posy][posx] = " "
        elif self._grid[posy][posx] == "h":
            self._grid[posy][posx] = "l"
        else:
            self._grid[posy][posx] = "f"

    def click_user(self, posx, posy):
        """ When the user clicks on the grid """

        if self._grid[posy][posx] == "f":
            self._grid[posy][posx] = " "
        elif self._grid[posy][posx] == "h":
            self._grid[posy][posx] = "l"
        elif self._grid[posy][posx] == "l":
            self.is_lost = True
        elif self._grid[posy][posx] == " ":
            self.destroy_case(posx, posy)

    def destroy_case(self, x, y):
        """ Destroy the case around a case """

        nb_landmine = 0
        max_bottom = self.row - 1
        max_right = self.col - 1

        # Top
        if y != 0 and self._grid[y - 1][x] in ("h", "l"):
            nb_landmine += 1
        # Bottom
        if y != max_bottom and self._grid[y + 1][x] in ("h", "l"):
            nb_landmine += 1
        # Right
        if x != max_right and self._grid[y][x + 1] in ("h", "l"):
            nb_landmine += 1
        # Left
        if x != 0 and self._grid[y][x - 1] in ("h", "l"):
            nb_landmine += 1
        # Top left
        if y != 0 and x != 0 and self._grid[y - 1][x - 1] in ("h", "l"):
            nb_landmine += 1
        # Top right
        if y != 0 and x != max_right and self._grid[y - 1][x + 1] in ("h", "l"):
            nb_landmine += 1
        # Bottom left
        if y != max_bottom and x != 0 and self._grid[y + 1][x - 1] in ("h", "l"):
            nb_landmine += 1
        # Bottom right
        if y != max_bottom and x != max_right and self._grid[y + 1][x + 1] in ("h", "l"):
            nb_landmine += 1

        if nb_landmine == 0:
            self._grid[y][x] = "0"

            if y != 0 and self._grid[y - 1][x] == " ":
                self.destroy_case(x, y - 1)
            if y != max_bottom and self._grid[y + 1][x] == " ":
                self.destroy_case(x, y + 1)
            if x != max_right and self._grid[y][x + 1] == " ":
                self.destroy_case(x + 1, y)
            if x != 0 and self._grid[y][x - 1] == " ":
                self.destroy_case(x - 1, y)
            if y != 0 and x != 0 and self._grid[y - 1][x - 1] == " ":
                self.destroy_case(x - 1, y - 1)
            if y != 0 and x != max_right and self._grid[y - 1][x + 1] == " ":
                self.destroy_case(x + 1, y - 1)
            if y != max_bottom and x != 0 and self._grid[y + 1][x - 1] == " ":
                self.destroy_case(x - 1, y + 1)
            if y != max_bottom and x != max_right and self._grid[y + 1][x + 1] == " ":
                self.destroy_case(x + 1, y + 1)
        else:
            self._grid[y][x] = str(nb_landmine)

    def create_grid(self):
        """ Create the grid with the right number of columns/rows/landmines """

        self._grid = [[" " for j in range(self.col)] for i in range(self.row)]

        for _ in range(self.nb_landmine):
            i = random.randint(0, self.row - 1)
            j = random.randint(0, self.col - 1)

            while self.grid[i][j] == "l":
                i = random.randint(0, self.row - 1)
                j = random.randint(0, self.col - 1)

            self._grid[i][j] = "l"
