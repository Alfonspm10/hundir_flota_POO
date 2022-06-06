import os
import random

class Tablero:

   

    def __init__(self, width=10, height=10):
        self.tablero = [["~" for i in range(width)] for i in range(height)]

    def __getitem__(self, point):
        row, col = point
        return self.tablero[row][col]

    def __setitem__(self, point, value):
        row, col = point
        self.tablero[row][col] = value

    def view_tablero(self):
        for row in self.tablero:
            print(" ".join(row))

    # Las dos funciones comprueban si la coordenada esta en la casilla

    def valid_col(self, row):
        try:
            self.tablero[row]
            return True
        except IndexError:
            return False

    def valid_row(self, col):
        try:
            self.tablero[0][col]
            return True
        except IndexError:
            return False

    # Las dos funciones comprueban una epsacio valido para colocar el barco

    def can_use_col(self, row, col, size):

        valid_coords = []

        for i in range(size):

            if self.valid_col(col) and self.valid_row(row):
                if self.tablero[row][col] == "~":
                    valid_coords.append((row, col))
                    col = col + 1
                else:
                    col = col + 1
            else:
                return False

        if size == len(valid_coords):
            return True
        else:
            return False

    def can_use_row(self, row, col, size):

        valid_coords = []

        for i in range(size):

            if self.valid_row(row) and self.valid_col(col):
                if self.tablero[row][col] == "~":
                    valid_coords.append((row, col))
                    row = row + 1
                else:
                    row = row + 1
            else:
                return False

        if size == len(valid_coords):
            return True
        else:
            return False

    # Corresponding fucntions set ship counters on valid space

    def set_ship_col(self, row, col, size):
        for i in range(size):
            self.tablero[row][col] = "S"
            col = col + 1

    def set_ship_row(self, row, col, size):
        for i in range(size):
            self.tablero[row][col] = "S"
            row = row + 1

