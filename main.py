import random
import sys

import numpy as np

from src.engine import run_simulation
from src.graphics import print_ascii_map
from src.spaceship import Spaceship


def main():
    random_mode = any(arg in ("-random", "--random") for arg in sys.argv[1:])

    alpha_deg = 30.0
    beta = 10.0
    grid_size = 25
    total_steps = 20

    if random_mode:
        print("Random mode with restricted spawns (ships on the map initially).")

        xA = random.uniform(0, grid_size - 1)
        yA = random.uniform(0, grid_size - 1)
        zA = random.uniform(-10, 10)

        xB = random.uniform(0, grid_size - 1)
        yB = random.uniform(0, grid_size - 1)
        zB = random.uniform(-10, 10)

        vxA, vyA, vzA = [random.uniform(-2, 2) for _ in range(3)]
        vxB, vyB, vzB = [random.uniform(-2, 2) for _ in range(3)]

        initial_posA = np.array([xA, yA, zA])
        initial_velA = np.array([vxA, vyA, vzA])
        initial_posB = np.array([xB, yB, zB])
        initial_velB = np.array([vxB, vyB, vzB])

    else:
        print("Deterministic mode (default).")
        initial_posA = np.array([0.0, 0.0, 0.0])
        initial_velA = np.array([1.0, 0.0, 0.0])
        initial_posB = np.array([20.0, 5.0, 0.0])
        initial_velB = np.array([-1.0, 0.0, 0.0])

    shipA = Spaceship("ShipA", initial_posA, initial_velA)
    shipB = Spaceship("ShipB", initial_posB, initial_velB)

    print(f"Ship A start: pos={shipA.position}, vel={shipA.velocity}")
    print(f"Ship B start: pos={shipB.position}, vel={shipB.velocity}\n")

    # We will call run_simulation in increments of 1 step so we can see ASCII each time
    winner = "None"
    final_step = 0

    for step in range(total_steps):
        print(f"--- Time Step {step} ---")
        print_ascii_map(shipA, shipB, grid_size=grid_size)

        winner, sim_step = run_simulation(
            shipA, shipB, alpha_deg, beta, time_steps=1, grid_size=grid_size
        )

        if winner != "None":
            final_step = sim_step + step
            break

    if winner == "A":
        print(f"Ship B was destroyed at step {final_step}. Ship A won.")
    elif winner == "B":
        print(f"Ship A was destroyed at step {final_step}. Ship B won.")
    elif winner == "Both":
        print(f"Both ships destroyed each other at step {final_step}.")
    else:
        print("Both ships survived.")


if __name__ == "__main__":
    main()
