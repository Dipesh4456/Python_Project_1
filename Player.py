class Player:
    """The player piloting the ship. Owns items and has a current location."""

    def __init__(self, name, location):
        self.name = name
        self.items = []
        self.location = location

    def move(self, destination):
        self.location = destination
        print(f"{self.name} flew to {destination.name}.")

    def collect_item(self):
        if self.location.item is None:
            print("There is nothing to collect here.")
        else:
            collected = self.location.item
            self.items.append(collected)
            self.location.item = None
            print(f"{collected.name} was added to your cargo hold.")