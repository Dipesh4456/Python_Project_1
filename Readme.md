SkyNova
Game idea and story
The world's cities are running out of power and only clean energy can restart the grid. 
Five clean energy cores are hidden in different cities of the sky. You are a pilot who must 
find them all. The hiding places and the fuel stations change every time you start a new 
game, and you choose your own starting city.

Objective
Collect all 5 clean energy cores: Helios (solar), Aqua (water), Flora (plants), Terra (earth) and Zephyr (wind). They are hidden in 5 random cities (never the starting city).
You win when all 5 cores are in your cargo hold. You lose if your ship's health reaches 0, or if you are stranded without enough fuel far from a station.

The world
10 cities connected by flight routes, so every city can be reached. Several paths lead to the same place, so there are many different ways to complete the game.
Every route has a fuel cost and a danger level (low, medium, HIGH).
Only 4 cities have a station (marked [STATION]) where you can refuel and repair. The stations are random in every new game, but the game always makes sure every city is within reach of one.
Heavy cargo uses more fuel: every 2 kg of cargo adds 1 fuel to each flight.
Dangerous flights: air shooters, lightning and tornadoes damage your ship. Higher danger means a bigger chance and more damage. A friendly pilot sometimes helps.
Commands
travel, collect, status, look, refuel, repair, save, help, lopeta (save and quit).

How it works
The player enters a name (and an age if new; players under 12 cannot play). If a save file for that name exists, the game continues from it.
For a new player, the 4 stations are placed randomly, then the player chooses a starting city, then the 5 cores are hidden randomly.
The intro and instructions are read from intro.txt and instructions.txt.
Progress is saved to saves/<name>.txt (location, health, fuel, cargo and which core is in which city and where the stations are). The save is deleted when the game ends in a win or a loss.

## Files
File                  	Purpose
1. Main.py       : Main loop, menu, travelling, win and defeat checks
2. Player.py     : Player class: name, items, location, health, fuel
3. Room.Py       : Room class: a city with an item, station and flight routes
4. Items.py      : Item class: name and weight
5. World.py      : 	Creates the cities, items and routes
6. Events.py     : Random events during flights
7. SaveGame.py   : 	Saving, loading and deleting save files
8. intro.txt, instructions.txt : Texts shown to the player

Sustainable development

The game is about SDG : Affordable and Clean Energy. The goal is to restore the world's power with clean energy sources (sun, water, plants, earth and wind), and the stations refuel the ship with clean energy.
How to run
Put all files in one folder and run python Main.py.