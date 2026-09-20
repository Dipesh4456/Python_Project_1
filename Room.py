class Room:
    """A room (sky sector) that the player can visit. May hold one item."""

    def __init__(self, name, item=None):
        self.name = name
        self.item = item