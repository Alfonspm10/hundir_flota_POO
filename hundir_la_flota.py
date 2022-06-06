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




class Radar:

    """Creates a grid to track the state of an opponent's tablero grid"""
    """Crea una casilla paraz"""

    def __init__(self, width=10, height=10):
        self.radar = [["." for i in range(width)] for i in range(height)]

    def __getitem__(self, point):
        row, col = point
        return self.radar[row][col]

    def __setitem__(self, point, value):
        row, col = point
        self.radar[row][col] = value

    def view_radar(self):
        for row in self.radar:
            print(" ".join(row))

class Ship:

    def __init__(self, ship_type, size):
        self.ship_type = ship_type
        self.size = size
        self.coords = []

    def plot_vertical(self, row, col):
        for i in range(self.size):
            self.coords.append((row, col))
            row = row + 1

    def plot_horizontal(self, row, col):
        for i in range(self.size):
            self.coords.append((row, col))
            col = col + 1

    def check_status(self):
        if self.coords == []:
            return True
        else:
            return False

class Player:

    ships = {"Aircraft Carrier": 5, "Crusier": 4, "Destroyer": 3, 
"Submarine": 2}

    def __init__(self, name):
        self.tablero = Tablero()
        self.radar = Radar()
        self.name = name
        self.fleet = []

   # Function uses player input to set up fleet positions on a player board.
   # For each ship, a ship object containing relevant coordinates is appended to self.fleet

    def set_fleet(self):
        input("Elige una coordenada entre 0 y 9 para las columnas y las filas de tu tablero")
        input("Los barcos estan colocados de derecha a izquierda.")
        
        for ship, size in self.ships.items():

            flag = True
            while flag:
                self.view_console()
                try:
                    print("Coloca tu %s" % (ship))
                    row = int(input("Elige una fila-----> "))
                    col = int(input("Elige una columna -----> "))
                    orientation = str(input("¿Vertical o horizontal? (elige v or h) -----> "))

                    if orientation in ["v", "V"]:
                        if self.tablero.can_use_row(row, col, size):
                            self.tablero.set_ship_row(row, col, size)
                            boat = Ship(ship, size)
                            boat.plot_vertical(row, col)
                            self.fleet.append(boat)
                            flag = False
                        else:
                            input("Choque de barcoos! Elige otra vez")

                    elif orientation in ["h", "H"]:
                        if self.tablero.can_use_col(row, col, size):
                            self.tablero.set_ship_col(row, col, size)
                            boat = Ship(ship, size)
                            boat.plot_horizontal(row, col)
                            self.fleet.append(boat)
                            flag = False
                        else:
                            input("Choque de barcoos! Elige otra vez")

                    else:
                        continue

                    self.view_console()
                    input()
                    os.system('clear')

                except ValueError:
                    print("¿No recuerdas tu entrenamiento?\nEscribe un numero..\n")

    # Function displays player tablero/radar in readable format

    def view_console(self):
        self.radar.view_radar()
        print("|                 |")
        self.tablero.view_tablero()

    # Function checks status of ship objects within player fleet

    def register_hit(self, row, col):
        for boat in self.fleet:
            if (row, col) in boat.coords:
                boat.coords.remove((row, col))
                if boat.check_status():
                    self.fleet.remove(boat)
                    print("%s's %s ha sido hundido!" % (self.name, boat.ship_type))

    # Player interface for initiating in-game strikes,
    # updates the state of the boards of both players

    def strike(self, target):
        self.view_console()
        try:
            print("\n%s Elige un objetivo..." % (self.name))
            row = int(input("Elige una fila -----> "))
            col = int(input("Elige una columna -----> "))

            if self.tablero.valid_row(row) and self.tablero.valid_col(col):
                if target.tablero.tablero[row][col] == "S":
                    print("Golpe directo!!!")
                    target.tablero.tablero[row][col] = "X"
                    target.register_hit(row, col)
                    self.radar.radar[row][col] = "X"

                else:
                    if self.radar.radar[row][col] == "O":
                        print("Ya has bombardeado esta zona.... Mira tu radar")
                        self.strike(target)
                    else:
                        print("Negativo...")
                        self.radar.radar[row][col] = "O"

            else:
                print("Coordenadas fuera de rango...")
                self.strike(target)

        except ValueError:
            print("Necesitas insertar un numero....\n")
            self.strike(target)
        input()
        os.system('clear')

class IA(Player):

    def __init__(self):
        super().__init__(self)
        self.name = "ia"

    # Automated version of set_fleet function from Player

    def set_compu_fleet(self):
        positions = ["v", "h"]

        for ship, size in self.ships.items():

            flag = True
            while flag:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice(positions)

                if orientation == "v":
                    if self.tablero.can_use_row(row, col, size):
                        self.tablero.set_ship_row(row, col, size)
                        boat = Ship(ship, size)
                        boat.plot_vertical(row, col)
                        self.fleet.append(boat)
                        flag = False

                    else:
                        row = row + 2

                elif orientation == "h":
                    if self.tablero.can_use_col(row, col, size):
                        self.tablero.set_ship_col(row, col, size)
                        boat = Ship(ship, size)
                        boat.plot_horizontal(row, col)
                        self.fleet.append(boat)
                        flag = False

                    else:
                        col = col + 2

                else:
                    continue

    # Automated strike function

    def compu_strike(self, target):
        row = random.randint(0, 9)
        col = random.randint(0, 9)

        if self.radar.radar[row][col] == ".":
            input("...Target acquired....%s, %s" % (row, col))

            if target.tablero.tablero[row][col] == "S":
                print("DIRECT HIT!")
                target.tablero.tablero[row][col] = "X"
                target.register_hit(row, col)
                self.radar.radar[row][col] = "X"

            else:
                print("Missed....recalibrating")
                self.radar.radar[row][col] = "O"

        else:
            self.compu_strike(target)

class BattleshipsCOMP:

    def __init__(self):
        start = input("Begin? (y or n) -----> ")
        if start in ["y", "Y"]:
            self.playCOMP()
        else:
            print("Aborted...")

    def playCOMP(self):
        pname = input("Player 1, state your name! -----> ")
        p = Player(pname)
        p.set_fleet()
        p.view_console()
        self.clear_screen()

        c = IA()
        print("Computer setting its fleet...")
        c.set_compu_fleet()
        self.clear_screen()

        flag = True
        while flag is True:
            p.strike(c)
            if self.fleet_sunk(c) is True:
                self.victory_message(p, c)
                flag = False
            else:
                self.clear_screen()

                c.compu_strike(p)
                if self.fleet_sunk(p) is True:
                    self.victory_message(c, p)
                    flag = False
                else:
                    self.clear_screen()
        print("\nThanks for playing!")

          # Function checks remaining ship counters on a player's board

    def fleet_sunk(self, player):
        ship_counters = 0
        """Traverses grid looking for 's' counters"""
        for row in range(len(player.tablero.tablero)):
            for col in range(len(player.tablero.tablero)):
                if player.tablero.tablero[row][col] == "S":
                    ship_counters += 1
        if ship_counters == 0:
            return True
        else:
            return False

    def clear_screen(self):
        input("\nNext Turn?")
        os.system('clear')

    def victory_message(self, winner, loser):
        print("\n\n\n*****************************************")
        print("%s's fleet has been destroyed, %s wins!" % (loser.name, winner.name))
        print("*****************************************")

# Script initiates game of battleships


def playbattleships():
    print("\n\n**********************************************")
    print("            Welcome to Battleships!")
    print("\n**********************************************")
    print('''
            ────║─▄──▄──▄──────
            ────║─▓──▓──▓──────
            ────░░░░░░░░░░─────
            ▀███████████████▀──
            ───────────────────
''')

    print("**********************************************\n")



playbattleships()
BattleshipsCOMP()