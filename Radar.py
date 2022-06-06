class Radar:

    """Crea una casilla para trackear el estado de un oponente en el tablero"""

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