# Smart Cannon: Projectile Motion Simulator

**Author:** Krina Amin  
**Language:** Python  
**Category:** Physics Simulation & Control Systems  

---

## Overview

This project simulates a projectile (cannonball) launched from the ground. It demonstrates how a computer can iteratively adjust the launch angle to hit a specific target distance like an automated aiming system. The simulation uses Euler integration to model the motion of a projectile under constant gravity (no air resistance) and visualizes both the motion and the aim correction process.  

I wrote it as an introduction to:
- Numerical physics simulation
- Basic control principles
- Python data visualization

I learned how discrete-time simulation (Euler integration) approximates motion equations, and how simple feedback logic can make systems self-correcting.

---

## Concepts Demonstrated

- **Projectile motion** under constant gravity  
- **Euler integration** (discretized differential equations)  
- **Analytical vs. simulated results** comparison  
- **Feedback control** through *iterative aim correction*  
- **Data visualization** with Matplotlib  

---

## How It Works

### Physics Model
The cannonball’s position is updated using Euler’s method:
\[
v_y(t + \Delta t) = v_y(t) - g \cdot \Delta t
\]
\[
x(t + \Delta t) = x(t) + v_x \cdot \Delta t
\]
\[
y(t + \Delta t) = y(t) + v_y(t) \cdot \Delta t
\]
Simulation stops when \( y < 0 \) (the cannonball hits the ground).


### Analytical Reference
For level ground (no drag), the theoretical range, height, and flight time are:
\[
R = \frac{v^2 \sin(2\theta)}{g}, \quad
H = \frac{v^2 \sin^2(\theta)}{2g}, \quad
T = \frac{2v \sin(\theta)}{g}
\]
These are compared to simulation results for validation.


### Iterative Aiming Controller
A simple “auto-aim” loop repeatedly fires, measures the miss, and adjusts the angle:
miss = target_x - impact_x
angle += learn_rate * sign(miss) * log1p(abs(miss))

This mimics a feedback control system, showing how repeated correction converges on the target.


### What Happens
- The cannon fires once — trajectory & velocity plots appear.
- The program compares simulated results to analytical physics formulas.
- The “Smart Cannon” controller starts firing iteratively, adjusting its aim until it hits the target.
- You’ll see graphs showing:
  - All trajectories for each try
  - Miss distance convergence over iterations
  - Angle adjustment over time

---

## Features

- Euler-integrated motion simulation  
- Linear interpolation for exact ground impact detection  
- Theoretical vs. simulated performance comparison  
- Visualizations for trajectory, velocity, and controller convergence  
- Iterative aim controller with adjustable learning rate and tolerance  
- Six clear plots:
  1. Projectile's position over time
  2. Projectile's velocity over time
  3. Projectile's position as it is launched at two angles to hit a target x upon impact
  4. Convergence of calculations of those angles
  5. Convergence of missed launches
  6. Angle Adjustment over time

---

### Prerequisites
Make sure you have Python 3 installed with these libraries:
pip install matplotlib numpy


### How to Run
1. Download the file and run it through the Python IDLE, or enter python Projectile_Motion_Simulation.py into the command prompt.
2. Code will run the simulation.

### References
Fundamentals of Physics — Halliday, Resnick & Walker
An Introduction to Classical Mechanics — Taylor
[Projectile Motion (hyperphysics)](http://hyperphysics.phy-astr.gsu.edu/hbase/traj.html)
