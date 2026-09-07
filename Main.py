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
