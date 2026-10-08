class Room:
    """A city (sky sector) that the player can visit. May hold one item."""

    def __init__(self, name, item=None, has_station=False, description="", welcome=""):
        self.name = name
        self.item = item
        self.has_station = has_station      # True = can refuel and repair here
        self.description = description
        self.welcome = welcome              # message shown when the player arrives
        self.connections = {}               # neighbour name -> (fuel cost, danger 1-3)

    def connect(self, other, fuel_cost, danger):
        """Make a two-way flight route between this city and another."""
        self.connections[other.name] = (fuel_cost, danger)
        other.connections[self.name] = (fuel_cost, danger)