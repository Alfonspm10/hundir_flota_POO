import IA
import Player
import os

class BattleshipsCOMP:

    def __init__(self):
        start = input("Empezar? (y or n) -----> ")
        if start in ["y", "Y"]:
            self.playCOMP()
        else:
            print("Abortamos...")

    def playCOMP(self):
        pname = input("Jugador 1, di tu nombre!! -----> ")
        p = Player(pname)
        p.set_fleet()
        p.view_console()
        self.clear_screen()

        c = IA()
        print("La flota enemiga ha sido colocada...")
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
        print("\nGracias por jugar!")

          # Function checks remaining ship counters on a player's board

    def fleet_sunk(self, player):
        ship_counters = 0
        for row in range(len(player.tablero.tablero)):
            for col in range(len(player.tablero.tablero)):
                if player.tablero.tablero[row][col] == "S":
                    ship_counters += 1
        if ship_counters == 0:
            return True
        else:
            return False

    def clear_screen(self):
        input("\nSiguiente?")
        os.system('clear')

    def victory_message(self, winner, loser):
        print("\n\n\n*****************************************")
        print("%s' la flota ha sido destruida, %s ganas!" % (loser.name, winner.name))
        print("*****************************************")

