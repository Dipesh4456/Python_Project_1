import random
from Room import Room
from Item import Item

ITEM_COUNT = 5
STATION_COUNT = 4
MAX_STATION_DISTANCE = 25  # every city must be this close to a station


def create_world():
    """Build 10 connected cities and the flight routes.
    Stations and items are added randomly by place_stations() and place_items()."""
    nova = Room("Nova City", None, False, "A big city glowing with neon lights.",
                "Welcome to Nova City! Neon lights sparkle as people wave at your ship.")
    valley = Room("Crystal Valley", None, False, "Glittering cliffs full of crystals.",
                  "Welcome to Crystal Valley! The crystals hum softly as you fly in.")
    harbor = Room("Ion Harbor", None, False, "A busy sky port.",
                  "Welcome to Ion Harbor! Dockworkers cheer as you land at the busy sky port.")
    ridge = Room("Storm Ridge", None, False, "Lightning flashes around the mountain tops.",
                 "Welcome to Storm Ridge! Hold on tight - thunder rumbles all around you.")
    plains = Room("Wind Plains", None, False, "Endless fields swept by strong winds.",
                  "Welcome to Wind Plains! Giant windmills spin gently as you glide down.")
    sun = Room("Sun Harbor", None, False, "A solar-powered city.",
               "Welcome to Sun Harbor! Golden sunlight shines on the solar rooftops.")
    peak = Room("Aurora Peak", None, False, "A frozen peak under glowing lights.",
                "Welcome to Aurora Peak! Green and purple lights dance across the sky.")
    bay = Room("Cloud Bay", None, False, "A floating town above the clouds.",
               "Welcome to Cloud Bay! Soft clouds drift around your ship as you land.")
    isles = Room("Ember Isles", None, False, "Warm volcanic islands drifting in the sky.",
                 "Welcome to Ember Isles! The warm air smells of volcanic rock.")
    frost = Room("Frost Harbor", None, False, "A cold harbour full of icy towers.",
                 "Welcome to Frost Harbor! Icy winds greet you at the frozen docks.")

    # connect(other, base fuel cost, danger level 1=low 2=medium 3=high)
    nova.connect(valley, 10, 1)
    nova.connect(harbor, 15, 1)
    nova.connect(plains, 20, 1)
    valley.connect(ridge, 15, 3)
    valley.connect(sun, 20, 2)
    harbor.connect(ridge, 10, 2)
    harbor.connect(plains, 15, 1)
    plains.connect(sun, 15, 1)
    ridge.connect(peak, 25, 3)
    ridge.connect(frost, 25, 3)
    sun.connect(peak, 30, 2)
    sun.connect(isles, 20, 2)
    peak.connect(bay, 15, 2)
    bay.connect(isles, 15, 1)
    bay.connect(frost, 20, 2)
    isles.connect(frost, 10, 3)

    return [nova, valley, harbor, ridge, plains, sun, peak, bay, isles, frost]


def create_items():
    """The 5 clean energy cores the player must find."""
    return [Item("Helios", 3.5),  # solar energy
            Item("Aqua", 3.0),  # water energy
            Item("Flora", 2.5),  # plant (bio) energy
            Item("Terra", 5.0),  # earth (geothermal) energy
            Item("Zephyr", 4.0)]  # wind energy


def place_items(rooms, start_room):
    """Hide the 5 items in 5 random different cities (never the start city)."""
    candidates = [room for room in rooms if room is not start_room]
    chosen = random.sample(candidates, ITEM_COUNT)
    for room, item in zip(chosen, create_items()):
        room.item = item


def distances_to_station(rooms, stations):
    """For every city, find the cheapest fuel cost to reach the nearest station."""
    distance = {}
    for room in rooms:
        distance[room.name] = 0 if room in stations else 9999
    changed = True
    while changed:  # keep improving until nothing changes
        changed = False
        for room in rooms:
            for neighbour, (cost, danger) in room.connections.items():
                if distance[neighbour] + cost < distance[room.name]:
                    distance[room.name] = distance[neighbour] + cost
                    changed = True
    return distance


def place_stations(rooms):
    """Pick random cities for the fuel stations. Try again until every city
    is close enough to a station, so the game stays fair."""
    while True:
        chosen = random.sample(rooms, STATION_COUNT)
        distance = distances_to_station(rooms, chosen)
        if max(distance.values()) <= MAX_STATION_DISTANCE:
            break
    for room in rooms:
        room.has_station = room in chosen