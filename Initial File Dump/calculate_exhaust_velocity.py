import math

def calculate_exhaust_velocity(R, gamma, Tc, Pe, Pc):
    psi_to_Pa = 6894.75729
    Pc *= psi_to_Pa
    u_exhaust = math.sqrt(
        (2 * R * gamma / (gamma - 1))
        * Tc
        * (1 - (Pe / Pc)**((gamma - 1) / gamma))
    )

    return u_exhaust