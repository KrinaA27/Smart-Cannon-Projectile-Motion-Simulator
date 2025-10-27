"""

Smart Cannon: Projectile Motion Simulator
-------------------------------------

Simulates a projectile (cannonball) launched from the ground, iteratively adjusts the
launch angle to hit a specific target distance like an automated aiming system.

Concepts demonstrated:
- Projectile motion under constant gravity
- Euler integration
- Analytical vs. simulated results comparison
- Feedback control through iteratie aim correction
- Data visualization with Matplotlib 

Written by Krina Amin

"""


import math
import numpy as np
import matplotlib.pyplot as plt

def simulate_projectile(speed = 5, angle_deg = 45, dt = 0.01, g = 9.81, y0 = 0, max_time = 10):

    """Simulates projectile motion using Euler integration."""
    
    t = 0.0
    x = 0.0 # initial x positon
    y = y0 # initial height
    theta = math.radians(angle_deg) # initial angle
    vx = speed * math.cos(theta) # velocity x component, constant
    vy = speed * math.sin(theta) # velocity y component, dynamic

    # Logs for values during motion
    times = [t]
    x_positions = [x]
    y_positions = [y]
    y_velocities = [vy]
    
    # Dynamics simulated using Euler's method
    while t < max_time and y >= 0:
        t += dt
        x += dt * vx
        vy += dt * -g
        y += dt * vy
        # linear interpolation between previous and current step
        if y < 0:
            y_prev = y_positions[-1]
            x_prev = x_positions[-1]
            frac = y_prev / (y_prev - y)     # fraction of step before impact
            impact_x = x_prev + frac * (x - x_prev)
            x_positions[-1] = impact_x
            y_positions[-1] = 0
            break
        times.append(t)
        x_positions.append(x)
        y_positions.append(y)
        y_velocities.append(vy)
    return np.array(times), np.array(x_positions), np.array(y_positions), np.array(y_velocities)


def plot_position(x_positions, y_positions):

    """Plots the projectile’s trajectory."""

    plt.plot(x_positions, y_positions, label="projectile trajectory")
    plt.axhline(0, color="k", lw=1)
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Projectile's Position(no drag)")
    plt.grid(True)
    plt.legend()
    plt.show()
    

def plot_velocity(times, y_velocities):

    """Plots the projectile’s velocity."""

    plt.plot(times, y_velocities, label= "projectile speed")
    plt.axhline(0, color= "c", lw=1)
    plt.xlabel("t (s)")
    plt.ylabel("vertical velocity (m/s)")
    plt.title("Projectile's Velocity Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()


def compare_to_analytic(speed, angle_deg, g, sim_metrics):

    """Compare simulated results to physics formulas."""

    theta = math.radians(angle_deg)
    H_theory = (speed**2 * math.sin(theta)**2) / (2*g)
    T_theory = (2 * speed * math.sin(theta)) / g
    R_theory = (speed**2 * math.sin(2*theta)) / g

    print("\nTheoretical Values\n"
        f"- Max height (theory): {H_theory:.2f} m\n"
        f"- Range (theory):      {R_theory:.2f} m\n"
        f"- Flight time (theory):{T_theory:.2f} s\n")
    

def compute_metrics(times, xs, ys):

    """Compute and print metrics from simulation."""


    max_y = np.max(ys)
    t_at_max_y = times[np.argmax(ys)]
    x_range = xs[-1]
    flight_time = times[-1]
    print("\nSimulated Values\n"
        f"Maximum height reached: {max_y:.2f} at Time t = {t_at_max_y:.2f} s\n"
        f"Horizontal Distance Aquired: {x_range:.2f} m\n"
        f"Total Flight Time: {flight_time:.2f} s\n")


def solve_angles(S):

    """Return two angles θ₁ and θ₂ (degrees) that satisfy sin(2θ)=S."""
    
    # keep S inside [-1,1]
    S = max(-1.0, min(1.0, S))
    a = math.asin(S)  # a = 2θ₁
    b = math.pi - a  # second solution for 2θ
    th1 = math.degrees(a/2.0)
    th2 = math.degrees(b/2.0)
    return sorted({round(th1, 6), round(th2, 6)})


def angle_for_target_x(speed, target_x, g=9.81):

    """
    Compute launch angle(s) (deg) that hit a horizontal target at x = target_x, assuming level ground and no air drag.
    Returns a list of 0–2 angles.
    """
    
    R_max = (speed**2) / g
    if target_x < 0 or target_x > R_max:
        print("Target too far for this speed.")
        return []

    S = (g * target_x) / (speed**2)
    return solve_angles(S)


def demo_target_hit():

    """Demonstrate angles that hit a given target distance."""
    
    speed = 25.0
    target_x = 50.0
    angles = angle_for_target_x(speed, target_x)

    if not angles:
        return  # no valid angles for this speed

    plt.figure()
    for a in angles:
        t, xs, ys, _ = simulate_projectile(speed=speed, angle_deg=a, dt=0.01)
        plt.plot(xs, ys, label=f"{a:.2f}°")

    # Plotting the trajectories of the two angles hit the target x distance
    plt.axvline(target_x, color="g", linestyle="--", label="target")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Angles That Hit the Target (no drag)")
    plt.legend()
    plt.grid(True)
    plt.show()


def iterative_aim(speed, target_x, initial_angle, learn_rate = 0.05, max_iters = 10, tol = 0.05):

    """
    Repeatedly adjust angle to make projectile hit the target.
    Returns final_angle and a history list of attempts.
    """

    angle = initial_angle
    history = []
    for i in range(max_iters):
        t, xs, ys, vys = simulate_projectile(speed, angle)
        impact_x = xs[-1]
        miss = target_x - impact_x
        history.append({"try": i+1, "angle": angle, "impact_x": impact_x, "miss": miss})
        if abs(miss) <= tol:
            break
        else:
            angle += learn_rate * np.sign(miss) * math.log1p(abs(miss))
            angle = max(0.0, min(85.0, angle))
        print(f"Try {i+1}: angle={angle:.2f}°, miss={miss:.2f} m") # prints the real-time state of the system
    best = min(history, key=lambda h: abs(h["miss"]))
    if abs(history[-1]["miss"]) > tol and len(history) == max_iters:
        print(f"Warning: Did not converge within {max_iters} iterations.")


    # Visualization of angle correction
    plt.figure()
    for attempt in history:
        t, xs, ys, _ = simulate_projectile(speed=speed, angle_deg=attempt["angle"])
        plt.plot(xs, ys, label=f"Try {attempt['try']}: {attempt['angle']:.1f}° (miss={attempt['miss']:.2f})")
    plt.axvline(target_x, color="g", linestyle="--", label=f"Target ({target_x} m)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.legend()
    plt.grid(True)
    plt.title("Iterative Aiming Convergence")
    plt.show()

    plt.figure()
    plt.plot(range(1, len(history)+1), [h["miss"] for h in history], 'o-')
    plt.axhline(0, color='k', lw=1)
    plt.xlabel("Iteration")
    plt.ylabel("Miss (m)")
    plt.title("Miss Convergence Over Iterations")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot([h["try"] for h in history], [h["angle"] for h in history], 'o-')
    plt.xlabel("Iteration")
    plt.ylabel("Launch Angle (°)")
    plt.title("Angle Adjustment Over Time")
    plt.grid(True)
    plt.show()
    
    errors = [abs(h["miss"]) for h in history]
    print("Miss magnitudes per try:", np.round(errors, 2)) # Prints summary of absolute errors using history list

    return best["angle"], history, abs(best["miss"])
                
    
if __name__ == "__main__":
    # Base projectile test
    t, xs, ys, vys = simulate_projectile()
    plot_position(xs, ys)
    plot_velocity(t, vys)
    compute_metrics(t, xs, ys)

    # Target-hitting demo
    demo_target_hit()

    # Controller test
    best_angle, history, final_error = iterative_aim(
        speed = 25.0,
        target_x = 45.0,
        initial_angle = 25.0,
        learn_rate = 0.05,
        max_iters = 15,
        tol = 0.5
        )
    print(f"Final best angle ≈ {best_angle:.2f}° (error={final_error:.3f} m) after {len(history)} tries")
