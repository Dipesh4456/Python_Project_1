import os
from Item import Item
from Player import Player

SAVE_DIR = "saves"


def save_path(name):
    """Make a safe file path from the player's name."""
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
        file.write(f"health={player.health}\n")
        file.write(f"fuel={player.fuel}\n")
        file.write("inventory=" + ",".join(item_to_text(i) for i in player.items) + "\n")
        file.write("stations=" + ",".join(r.name for r in rooms if r.has_station) + "\n")
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

    # Put the items and stations back into the cities
    station_names = data.get("stations", "").split(",")
    for room in rooms:
        room.item = item_from_text(data.get(f"room.{room.name}", ""))
        room.has_station = room.name in station_names

    # Rebuild the player
    location = rooms[0]
    for room in rooms:
        if room.name == data.get("location"):
            location = room
    player = Player(data.get("name", name), location)
    player.health = int(data.get("health", Player.MAX_HEALTH))
    player.fuel = int(data.get("fuel", Player.MAX_FUEL))
    for text in data.get("inventory", "").split(","):
        item = item_from_text(text)
        if item:
            player.items.append(item)

    return player, int(data.get("age", 18))


def delete_save(name):
    """Remove the save file (used when the game has ended)."""
    path = save_path(name)
    if os.path.exists(path):
        os.remove(path)