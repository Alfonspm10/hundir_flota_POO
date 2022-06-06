import random
import Player
import Ship

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
                print("Fallo....")
                self.radar.radar[row][col] = "O"

        else:
            self.compu_strike(target)
