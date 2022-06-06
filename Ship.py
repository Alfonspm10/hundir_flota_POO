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