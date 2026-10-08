import random


def travel_event(player, danger):
    """Something may happen during the flight. Higher danger = more trouble."""
    chance = 0.15 + 0.15 * danger          # 30%, 45% or 60%
    if random.random() > chance:
        print("Smooth flight. Nothing unusual happens.")
        return

    if random.random() < 0.15:
        player.repair(10)
        print("A friendly pilot shares a repair kit. (health +10)")
        return

    event = random.choice(["air shooter", "lightning", "tornado"])
    if event == "air shooter":
        damage = random.randint(5, 12) * danger
        player.take_damage(damage)
        print(f"Air shooters attack your ship! (health -{damage})")
    elif event == "lightning":
        damage = random.randint(6, 14) * danger
        player.take_damage(damage)
        print(f"Lightning strikes your ship! (health -{damage})")
    else:
        damage = random.randint(4, 10) * danger
        player.take_damage(damage)
        player.fuel = max(0, player.fuel - 5)
        print(f"A tornado throws you off course! (health -{damage}, fuel -5)")