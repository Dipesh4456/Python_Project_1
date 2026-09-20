import Player
import Room
import Item

# --- Ask for the player's name and age ---
name = input("What is your name? ")
age = input("What is your age? ")
age = int(age)

print(name)
print(age)

if age < 12:
    print("Sorry, you are a minor and cannot play this game.")
    quit()

print(f"Welcome to SkyNova, {name}!")

menu = """
--- SkyNova Main Menu ---
fly       - take off and explore the skies
collect   - search for energy crystals
dodge     - practice avoiding obstacles
status    - check Plane's status
lopeta    - quit the game
"""

print(menu)
# --- Set up the game world ---
command = ""

while command != "lopeta":
    command = input("Enter a command: ")

    if command == "fly":
        print("You take off into the neon-lit sky above Nova City.")
    elif command == "collect":
        print("You spot a glowing energy crystal and scoop it into your cargo hold.")
    elif command == "dodge":
        print("An asteroid whizzes by - nice reflexes, pilot!")
    elif command == "status":
        print("Ship status: engines nominal, fuel at 82%, crystals collected: 3.")
    elif command == "lopeta":
        print("Landing sequence initiated. Thanks for playing SkyNova!")
    else:
        print("Unknown command. Try again.")

    if command != "lopeta":
        print(menu)

crystals = []
crystal_types = ["Aurelium", "Voidglass", "Pulse", "Nebulite"]


def fly():
    print("You take off into the neon-lit sky above Nova City.")


def collect():
    print(f"Possible crystals: {', '.join(crystal_types)}")
    crystal_name = input("What did you find? ")
    crystals.append(crystal_name)
    print(f"{crystal_name} was added to your cargo hold.")


def dodge():
    print("An asteroid whizzes by - nice reflexes, pilot!")


def status():
    if crystals == []:
        print("Your cargo hold is empty.")
    else:
        print("Crystals collected so far:")
        for crystal in crystals:
            print(f"- {crystal}")

# SkyNova - Main Menu (object-oriented version)

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
    print("lopeta    - quit the game")
    print("Sectors:", ", ".join(room.name for room in rooms))


def choose_room(rooms):
    destination_name = input("Which sector do you want to fly to? ")
    for room in rooms:
        if room.name.lower() == destination_name.lower():
            return room
    print("Unknown sector.")
    return None