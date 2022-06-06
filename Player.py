import os
import random
import Tablero
import Radar
import Ship

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