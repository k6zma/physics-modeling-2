import numpy as np
from scipy.constants import e, m_e
from scipy.integrate import solve_ivp
from config import CM_TO_M


class ParticleTrajectory:
    def __init__(
        self, inner_radius_cm, outer_radius_cm, initial_velocity, capacitor_length_cm
    ):
        self.inner_radius = inner_radius_cm * CM_TO_M
        self.outer_radius = outer_radius_cm * CM_TO_M
        self.capacitor_length = capacitor_length_cm * CM_TO_M

        self.initial_velocity = initial_velocity

        self.distance_between_plates = self.outer_radius - self.inner_radius
        self.mean_radius = (self.outer_radius + self.inner_radius) / 2

    def electric_field(self, y, voltage):
        r_prime = self.mean_radius + y
        return voltage / (r_prime * np.log(self.outer_radius / self.inner_radius))

    def motion_equations(self, t, vars, voltage):
        x, Vx, y, Vy = vars

        Ey = self.electric_field(y, voltage)

        ax = 0
        ay = -e * Ey / m_e

        return [Vx, ax, Vy, ay]

    def inner_plate_collision(self, t, vars, voltage):
        return vars[2] - (-self.distance_between_plates / 2)

    inner_plate_collision.terminal = True
    inner_plate_collision.direction = -1

    def capacitor_exit(self, t, vars, voltage):
        return vars[0] - self.capacitor_length

    capacitor_exit.terminal = True
    capacitor_exit.direction = 1

    def simulate_trajectory(self, voltage):
        initial_conditions = [0, self.initial_velocity, 0, 0]
        time_span = (0, self.capacitor_length / self.initial_velocity * 2)
        time_eval = np.linspace(time_span[0], time_span[1], 1000)

        solution = solve_ivp(
            self.motion_equations,
            time_span,
            initial_conditions,
            args=(voltage,),
            t_eval=time_eval,
            events=[self.inner_plate_collision, self.capacitor_exit],
        )

        return solution

    def find_minimum_voltage(self, voltage_start=1, voltage_end=1e4, voltage_step=1):
        voltage_values = np.arange(voltage_start, voltage_end, voltage_step)
        minimum_voltage = None

        for voltage in voltage_values:
            solution = self.simulate_trajectory(voltage)

            if solution.status == 1 and len(solution.t_events[0]) > 0:
                minimum_voltage = voltage
                break

        if minimum_voltage is not None:
            solution = self.simulate_trajectory(minimum_voltage)

            t = solution.t

            x = solution.y[0]
            y = solution.y[2]

            vy = solution.y[3]
            ay = np.gradient(vy, t)

            return minimum_voltage, t, x, y, vy, ay
        else:
            raise ValueError("Не найдена минимальная разность потенциалов.")
