from Player import Player
from World import create_world, place_stations, place_items, ITEM_COUNT
from Events import travel_event
from Savegame import save_game, load_game, delete_save

DANGER_LABELS = {1: "low", 2: "medium", 3: "HIGH"}


# ---------- Reading text files ----------
def read_text(filename):
    """Read a text file and return its contents."""
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"[Missing file: {filename}]\n"


# ---------- Showing information ----------
def find_room(rooms, name):
    """Return the room with this name, or None."""
    for room in rooms:
        if room.name.lower() == name.lower():
            return room
    return None


def describe(room, rooms, player):
    """Show the current city, its item, station and flight routes."""
    print(f"\n=== {room.name} ===")
    print(room.description)
    if room.item:
        print(f"You see: {room.item.name} ({room.item.weight} kg) - type 'collect'")
    if room.has_station:
        print("Station here: you can 'refuel' and 'repair'.")
    print("Flight routes (fuel includes your cargo weight):")
    for name, (base, danger) in room.connections.items():
        mark = "  [STATION]" if find_room(rooms, name).has_station else ""
        print(f"  {name} - fuel {player.fuel_cost(base)}, "
              f"danger {DANGER_LABELS[danger]}{mark}")


def arrive(player, rooms):
    """Welcome the player to the city they just reached, then describe it."""
    print(f"\n{player.location.welcome}")
    describe(player.location, rooms, player)


def show_status(player):
    print(f"\nPilot: {player.name}")
    print(f"Location: {player.location.name}")
    print(f"Ship health: {player.health}/{Player.MAX_HEALTH}")
    print(f"Fuel: {player.fuel}/{Player.MAX_FUEL}")
    print(f"Cores collected: {len(player.items)}/{ITEM_COUNT}")
    if player.items:
        for item in player.items:
            print(f"- {item.name} ({item.weight} kg)")
    print(f"Cargo weight: {player.cargo_weight()} kg")


def show_menu():
    print("\n--- SkyNova Main Menu ---")
    print("travel  collect  status  look  refuel  repair  save  help  lopeta")
    print("(Tip: type a city name, like 'Wind Plains', to fly straight there)")


# ---------- Travelling ----------
def choose_destination(player, rooms, name=""):
    """Find where to fly. Asks for the city only if no name was given.
    Returns (room, base_cost, danger) or None."""
    if name == "":
        name = input("Which city do you want to fly to? ").strip().lower()
    for neighbour, (base, danger) in player.location.connections.items():
        if neighbour.lower() == name:
            return find_room(rooms, neighbour), base, danger
    print("You can't fly there directly from here.")
    return None


def check_defeat(player):
    """Return a message if the player has lost, otherwise None."""
    if not player.is_alive():
        return "Your ship crashed and cannot fly any more."
    return None


def travel(player, rooms, name=""):
    """Fly to a neighbouring city. Returns a defeat message or None."""
    choice = choose_destination(player, rooms, name)
    if choice is None:
        return None
    destination, base, danger = choice
    cost = player.fuel_cost(base)
    if player.fuel < cost:
        if player.location.has_station:
            # At a station you can still refuel, so this is not a loss yet
            print(f"Not enough fuel for that flight (needs {cost}, you have {player.fuel}).")
            print("Type 'refuel' first.")
            return None
        return "Not enough fuel for flight \U0001F622"    # crying face
    player.move(destination, cost)
    travel_event(player, danger)
    defeat = check_defeat(player)
    if defeat is None:
        arrive(player, rooms)
    return defeat


def station_action(player, action):
    """Refuel or repair, only possible in a city with a station."""
    if not player.location.has_station:
        print("There is no station in this city.")
    elif action == "refuel":
        if player.fuel >= Player.MAX_FUEL:
            print("Your tank is already full.")
        else:
            player.refuel()
            print(f"Tanks filled with clean energy. (fuel {player.fuel}/{Player.MAX_FUEL})")
    else:
        if player.health >= Player.MAX_HEALTH:
            print("Your ship is not damaged. No repairs needed.")
        else:
            player.repair(30)
            print(f"Repairs done. (health {player.health}/{Player.MAX_HEALTH})")


# ---------- Starting a game ----------
def ask_age():
    """Keep asking until the player types a number."""
    while True:
        text = input("What is your age? ")
        if text.isdigit():
            return int(text)
        print("Please type your age as a number.")


def choose_start_city(rooms):
    """Let the player pick the city where the adventure begins."""
    print("\nChoose your starting city:")
    for number, room in enumerate(rooms, 1):
        mark = "  [STATION]" if room.has_station else ""
        print(f"  {number}. {room.name}{mark}")
    while True:
        text = input("Type a number or a city name: ").strip()
        if text.isdigit() and 1 <= int(text) <= len(rooms):
            return rooms[int(text) - 1]
        room = find_room(rooms, text)
        if room:
            return room
        print("Unknown city. Try again.")


# ---------- Main program ----------
def main():
    print(read_text("intro.txt"))
    print(read_text("instructions.txt"))

    rooms = create_world()
    name = ""
    while name == "":
        name = input("What is your name? ").strip()

    loaded = load_game(name, rooms)
    if loaded:
        player, age = loaded
        print(f"\nWelcome back, {player.name}! Continuing your saved game.")
    else:
        age = ask_age()
        if age < 12:
            print("Sorry, you are a minor and cannot play this game.")
            return
        place_stations(rooms)           # random fuel stations every game
        start = choose_start_city(rooms)
        place_items(rooms, start)       # random item places every game
        player = Player(name, start)
    arrive(player, rooms)

    command = ""
    while command != "lopeta":
        show_menu()
        command = input("Enter a command: ").strip().lower()
        message = None
        won = False

        # Shortcuts: "travel wind plains" or just "wind plains"
        city_name = ""
        if command.startswith("travel "):
            city_name = command[7:].strip()
            command = "travel"
        elif find_room(rooms, command):
            city_name = command
            command = "travel"

        if command == "travel":
            message = travel(player, rooms, city_name)
        elif command == "collect":
            player.collect_item()
            if len(player.items) == ITEM_COUNT:
                print(f"\nYOU WIN! All {ITEM_COUNT} clean energy cores are collected "
                      "and the world's power is restored!")
                won = True
        elif command == "status":
            show_status(player)
        elif command == "look":
            describe(player.location, rooms, player)
        elif command == "refuel" or command == "repair":
            station_action(player, command)
        elif command == "save":
            save_game(player, age, rooms)
        elif command == "help":
            print(read_text("instructions.txt"))
        elif command == "lopeta":
            save_game(player, age, rooms)
            print("Landing sequence initiated. Thanks for playing SkyNova!")
        else:
            print("Unknown command. Try again.")

        if message:
            print(f"\nYOU LOSE. {message}")
        if message or won:
            delete_save(player.name)
            break


if __name__ == "__main__":
    main()