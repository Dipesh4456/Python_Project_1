About (SkyNova)
The game is split into separate modules, each containing one class or the main program
logic:
Main.py - runs the game: sets up the world (rooms and items), asks for the player's 
name and age, and runs the main menu loop.
Player.py - the Player class. A player has a name, a list of items they are carrying,
and a location (the Room they are currently in). Players can move() to a different room and collect_item() from their current room.
Room.py - the Room class. A room has a name and may contain one item.
Item.py - the Item class. An item (energy crystal) has a name and a weight.

When the program starts, a Player object is created along with a few Room and Item
objects representing the sectors of space the player can explore. From the main menu,
the player can move between rooms and collect the crystal in their current room.