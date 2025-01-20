# spaceship.py
import numpy as np

class Spaceship:
    def __init__(self, name, initial_position, initial_velocity):
        """
        Represents a spaceship in 3D space.
        """
        self.name = name
        self.position = initial_position.astype(float)
        self.velocity = initial_velocity.astype(float)

        vel_norm = np.linalg.norm(self.velocity)
        if vel_norm > 0:
            self.forward = self.velocity / vel_norm
        else:
            # If velocity is zero, pick an arbitrary forward direction
            self.forward = np.array([1.0, 0.0, 0.0])

        self.destroyed = False

    def update_position(self):
        """
        Move the ship by adding velocity to its position.
        """
        self.position += self.velocity

    def update_forward(self, target_position):
        """
        Adjust forward direction towards the given 'target_position'.
        """
        direction = target_position - self.position
        dist = np.linalg.norm(direction)
        if dist != 0:
            self.forward = direction / dist

    def is_in_firing_range(self, target, alpha_deg, beta):
        """
        Checks if 'target' is within firing angle 'alpha_deg' and distance 'beta'.
        """
        if target.destroyed:
            return False  

        # Distance check
        diff = target.position - self.position
        dist = np.linalg.norm(diff)
        if dist > beta:
            return False

        # Angle check
        forward_len = np.linalg.norm(self.forward)
        if forward_len == 0 or dist == 0:
            # If no forward vector or the distance is effectively zero, lets say its in range
            return True

        dot_val = np.dot(self.forward, diff)
        cos_theta = dot_val / (forward_len * dist)

        # Numerical safety clamp
        cos_theta = max(min(cos_theta, 1.0), -1.0)

        angle_rad = np.arccos(cos_theta)
        angle_deg = np.degrees(angle_rad)

        return angle_deg <= alpha_deg
