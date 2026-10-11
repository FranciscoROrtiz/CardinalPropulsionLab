import numpy as np
from scipy.optimize import least_squares

# Given data
I = 1.0                  # Moment of inertia (kg*m^2)
omega_0 = 60.0            # Initial angular velocity (rad/s)
t1 = 0.5                  # First measurement time (s)
omega_1 = 45.0            # Angular velocity at t1 (rad/s)
t2 = 2.5                  # Second measurement time (s)
omega_2 = 8.0             # Angular velocity at t2 (rad/s)


def equations(unknowns):

    b, Tf = unknowns

    omega_pred_1 = (
        (omega_0 + Tf/b) * np.exp(-b*t1/I) - Tf/b
    )

    omega_pred_2 = (
        (omega_0 + Tf/b) * np.exp(-b*t2/I) - Tf/b
    )

    # Residuals: predicted - measured
    eq1 = omega_pred_1 - omega_1
    eq2 = omega_pred_2 - omega_2

    return [eq1, eq2]


# Solve
initial_guess = [0.4, 8.7] # Given

solution = least_squares(
    equations,
    x0=initial_guess,
    bounds=([1e-10, 0], [np.inf, np.inf]),
    xtol=1e-14,
    ftol=1e-14,
    gtol=1e-14
)

b, Tf = solution.x

# Results
print(f"Linear viscous damping coefficient:")
print(f"b = {b:.6f} kg*m^2/s")
print(f"\nCoulomb friction torque:")
print(f"Tf = {Tf:.6f} N*m")
