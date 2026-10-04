import os

from Player import Player
from Room import Room
from Item import Item

SAVE_DIR = "saves"


# ---------- Reading text files ----------
def read_text(filename):
    """Read a text file and return its contents."""
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"[Missing file: {filename}]\n"


# ---------- World setup ----------
def create_rooms():
    """Create the sectors of the game world with their crystals."""
    return [
        Room("Nova City"),
        Room("Asteroid Belt", Item("Aurelium", 2.5)),
        Room("Ion Storm", Item("Voidglass", 1.8)),
        Room("Crystal Nebula", Item("Pulse", 3.0)),
        Room("Deep Space", Item("Nebulite", 1.2)),
    ]


# ---------- Saving and loading ----------
def save_path(name):
    safe = "".join(c for c in name.lower() if c.isalnum() or c in "-_")
    return os.path.join(SAVE_DIR, f"{safe}.txt")


def item_to_text(item):
    return f"{item.name}:{item.weight}" if item else ""


def item_from_text(text):
    if not text:
        return None
    item_name, weight = text.split(":")
    return Item(item_name, float(weight))


def save_game(player, age, rooms):
    """Write the full game state to the player's save file."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(save_path(player.name), "w", encoding="utf-8") as file:
        file.write(f"name={player.name}\n")
        file.write(f"age={age}\n")
        file.write(f"location={player.location.name}\n")
        file.write("inventory=" + ",".join(item_to_text(i) for i in player.items) + "\n")
        for room in rooms:
            file.write(f"room.{room.name}={item_to_text(room.item)}\n")
    print("Game saved.")


def load_game(name, rooms):
    """Load a saved game. Returns (player, age) or None if no save exists."""
    path = save_path(name)
    if not os.path.exists(path):
        return None

    data = {}
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")
            if "=" in line:
                key, value = line.split("=", 1)
                data[key] = value

    # Restore which crystals are still lying in each sector
    for room in rooms:
        room.item = item_from_text(data.get(f"room.{room.name}", ""))

    # Restore the player's location and cargo
    location = rooms[0]
    for room in rooms:
        if room.name == data.get("location"):
            location = room
    player = Player(data.get("name", name), location)
    for text in data.get("inventory", "").split(","):
        item = item_from_text(text)
        if item:
            player.items.append(item)

    return player, int(data.get("age", 18))


# ---------- Menu functions ----------
def show_status(player):
    print(f"Current sector: {player.location.name}")
    if player.items == []:
        print("Cargo hold is empty.")
    else:
        print("Crystals collected so far:")
        for item in player.items:
            print(f"- {item.name} ({item.weight} kg)")


def show_menu(rooms):
    print("\n--- SkyNova Main Menu ---")
    print("move      - fly to a different sector")
    print("collect   - collect the crystal in this sector (if any)")
    print("status    - check your ship's cargo and location")
    print("save      - save your progress")
    print("help      - show instructions")
    print("lopeta    - save and quit the game")
    print("Sectors:", ", ".join(room.name for room in rooms))


def choose_room(rooms):
    destination_name = input("Which sector do you want to fly to? ")
    for room in rooms:
        if room.name.lower() == destination_name.lower():
            return room
    print("Unknown sector.")
    return None


# ---------- Main program ----------
def main():
    print(read_text("intro.txt"))
    print(read_text("instructions.txt"))

    rooms = create_rooms()
    name = input("What is your name? ").strip()

    loaded = load_game(name, rooms)
    if loaded:
        player, age = loaded
        print(f"\nWelcome back, {player.name}! Continuing your saved game.")
    else:
        age_text = input("What is your age? ")
        if not age_text.isdigit():
            print("Please enter your age as a number.")
            return
        age = int(age_text)
        if age < 12:
            print("Sorry, you are a minor and cannot play this game.")
            return
        player = Player(name, rooms[0])
        print(f"\nWelcome to SkyNova, {name}!")

    command = ""
    while command != "lopeta":
        show_menu(rooms)
        command = input("Enter a command: ").strip().lower()

        if command == "move":
            destination = choose_room(rooms)
            if destination:
                player.move(destination)
        elif command == "collect":
            player.collect_item()
        elif command == "status":
            show_status(player)
        elif command == "save":
            save_game(player, age, rooms)
        elif command == "help":
            print(read_text("instructions.txt"))
        elif command == "lopeta":
            save_game(player, age, rooms)
            print("Landing sequence initiated. Thanks for playing SkyNova!")
        else:
            print("Unknown command. Try again.")


if __name__ == "__main__":
    main()