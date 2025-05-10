import random


def clamp_and_bounce(ship, grid_size=25):
    """
    Bounces the ship off the edges of the ASCII map in x,y.
    """
    for i in [0, 1]:
        if ship.position[i] < 0:
            ship.position[i] = 0
            ship.velocity[i] = -ship.velocity[i]
        elif ship.position[i] >= grid_size:
            ship.position[i] = grid_size - 1
            ship.velocity[i] = -ship.velocity[i]


def run_simulation(shipA, shipB, alpha_deg, beta, time_steps=50, grid_size=25):
    """
    Runs the main simulation loop for time_steps or until ships are destroyed.
    Checks for simultaneous firing conditions, but uses a tie breaker instead
    of destroying both at once.
    """
    for t in range(time_steps):
        shipA.update_position()
        shipB.update_position()

        clamp_and_bounce(shipA, grid_size)
        clamp_and_bounce(shipB, grid_size)

        predicted_posA = shipA.position + shipA.velocity
        predicted_posB = shipB.position + shipB.velocity
        shipA.update_forward(predicted_posB)
        shipB.update_forward(predicted_posA)

        # Check firing for BOTH ships in the same time step
        a_can_fire = (not shipB.destroyed) and shipA.is_in_firing_range(
            shipB, alpha_deg, beta
        )
        b_can_fire = (not shipA.destroyed) and shipB.is_in_firing_range(
            shipA, alpha_deg, beta
        )

        if a_can_fire and b_can_fire:
            if random.random() < 0.5:
                shipB.destroyed = True
                print(
                    f"[Time {t}] {shipA.name} destroyed {shipB.name} (tie-break coin toss)"
                )
                return ("A", t)
            else:
                shipA.destroyed = True
                print(
                    f"[Time {t}] {shipB.name} destroyed {shipA.name} (tie-break coin toss)"
                )
                return ("B", t)

        elif a_can_fire:
            shipB.destroyed = True
            print(f"[Time {t}] {shipA.name} destroyed {shipB.name}")
            return ("A", t)

        elif b_can_fire:
            shipA.destroyed = True
            print(f"[Time {t}] {shipB.name} destroyed {shipA.name}")
            return ("B", t)

    if shipA.destroyed and not shipB.destroyed:
        return ("B", time_steps - 1)
    elif shipB.destroyed and not shipA.destroyed:
        return ("A", time_steps - 1)
    elif shipA.destroyed and shipB.destroyed:
        return ("Both", time_steps - 1)
    else:
        return ("None", time_steps - 1)
