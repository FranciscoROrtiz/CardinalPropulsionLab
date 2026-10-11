from nozzle_rao_parabola_angles import calculate_parabolic_angles

epsilon = 3.85

angles = calculate_parabolic_angles(epsilon)

theta_n = angles["theta_n"]
theta_e = angles["theta_e"]

print(f"theta_n = {theta_n}")
print(f"theta_e = {theta_e}")