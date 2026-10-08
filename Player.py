class Player:
    """The pilot. Owns items, has a location, ship health and fuel."""

    MAX_HEALTH = 100
    MAX_FUEL = 100

    def __init__(self, name, location):
        self.name = name
        self.items = []
        self.location = location
        self.health = Player.MAX_HEALTH
        self.fuel = Player.MAX_FUEL

    def cargo_weight(self):
        """Total weight of everything in the cargo hold."""
        total = 0
        for item in self.items:
            total += item.weight
        return total

    def fuel_cost(self, base_cost):
        """Flight cost grows with the cargo weight (+1 fuel per 2 kg)."""
        return base_cost + int(self.cargo_weight() / 2)

    def move(self, destination, fuel_cost):
        """Fly to another city and use fuel."""
        self.fuel -= fuel_cost
        self.location = destination
        print(f"{self.name} flew to {destination.name}. (fuel -{fuel_cost})")

    def collect_item(self):
        if self.location.item is None:
            print("There is nothing to collect here.")
        else:
            collected = self.location.item
            self.items.append(collected)
            self.location.item = None
            print(f"{collected.name} was added to your cargo hold.")

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def is_alive(self):
        return self.health > 0

    def refuel(self):
        self.fuel = Player.MAX_FUEL

    def repair(self, amount):
        self.health = min(Player.MAX_HEALTH, self.health + amount)