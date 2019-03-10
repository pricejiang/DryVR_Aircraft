# Aircraft Model Simulation
# Written by Aditi Ghosalkar and Sayan Mitra
# UIUC Feb 2019
# Model aircraft from Barron Associates

import numpy as np
from numpy import linalg as l
from numpy import array
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def aircraft_dynamic(ode_vars, t, C, w, M, K, v_init, wpx, wpy, wpx_n, wpy_n):
    # models the dynamics of a simple aircraft.
    # Returns dv, dpsi, dx, dy
    # T_c,phi_c: Thrust input, bank angle input
    # C: Drag coefficient
    # w: additive noise term
    # M: mass
    # ode_vars: [Velocity (v), Heading angle (\Psi) ]
    
    g = 32.2
    v, psi, x, y = ode_vars

    K1, K2, K3 = K

    p_1 = array([(x - wpx), (y - wpy)])
    p_2 = array([(x - wpx_n), (y - wpy_n)])

    lmbd = (p_2 - p_1) / l.norm(p_2 - p_1)
    F = l.norm(np.cross(lmbd, p_1))
    psi_c = get_psi_c(wpx, wpy, wpx_n, wpy_n)

    T_c = K1 * M * (v_init - v)
    phi_c = ((K2 * v_init * (psi_c - psi)) / g) + K3 * F

    dvdt = ((T_c - (C * v * v)) / M) + w
    dpsidt = ((g * np.sin(phi_c)) / v) + w  

    # Question. Subtract pi/2 from \Psi as \phi is measured along x axis and \Psi is measured
    # along north.
    #    dxdt = (ode_vars[0]*np.cos(ode_vars[1] - np.pi/2)) + w
    #    dydt = (ode_vars[0]*np.sin(ode_vars[1] -  np.pi/2)) + w
    dxdt = (v * np.cos(np.pi/2 - psi)) + w
    dydt = (v * np.sin(np.pi/2 - psi)) + w
    return dvdt, dpsidt, dxdt, dydt

def get_psi_c(wpx_1, wpy_1, wpx_2, wpy_2):
    # Returns psi_c control bank angle between two way-points
    # This angle is measured relative to north
    # The angle is in radians

    opp = (wpx_2 - wpx_1)
    adj = (wpy_2 - wpy_1)
    angle = np.arctan(opp / adj)

    if angle <  0 and opp > 0 and adj < 0 :
        angle = angle + np.pi
    elif angle > 0 and opp < 0 and adj < 0:
        angle = angle + np.pi

    return angle

def TC_Simulate(Mode,initialCondition,time_bound):
    # Hybrid simulation for aircraft model across sequence of way-points
    # Mode: containing the current and next way points
    # initialCondition: initial position (v, psi, X,Y)

    # Setting time step
    time_step = 0.05
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt
    
    # Some constants; some are arbitrary, subject to future change
    C = 0.002 
    w = 0
    M = 1
    K = [15, 0.4, np.power(np.e, -6)]
    v_init = initialCondition[0]

    # Parse Mode, in format of "wpx:wpy wpx_n:wpy_n"
    wpx = int(Mode.split(" ")[0].split(":")[0])
    wpy = int(Mode.split(" ")[0].split(":")[1])
    wpx_n = int(Mode.split(" ")[1].split(":")[0])
    wpy_n = int(Mode.split(" ")[1].split(":")[1])
    
    sol = odeint(aircraft_dynamic, initialCondition, t, args=(C, w, M, K, v_init, wpx, wpy, wpx_n, wpy_n), hmax=time_step)

    # For loops to determine the most relevant parts of the path
    min_dist_sqr = 500000
    min_in = len(sol)/2
    for j in range(0, len(sol)):
        dist_sqr = (wpx_n-(sol[j][2]))*(wpx_n-(sol[j][2])) + (wpy_n-(sol[j][3]))*(wpy_n-(sol[j][3]))
        if dist_sqr < min_dist_sqr:
            min_dist_sqr = dist_sqr
            min_in = j
    v = sol[min_in][0]
    psi = sol[min_in][1]
    x = sol[min_in][2]
    y = sol[min_in][3]

    # Construct the final output
    trace = []
    for j in range(len(t)):
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,0]))
        tmp.append(float(sol[j,1]))
        tmp.append(float(sol[j,2]))
        tmp.append(float(sol[j,3]))
        trace.append(tmp)

    return trace#, [v, psi, x, y]


if __name__ == "__main__":
    WP = ["-10:-20 133:192", "133:192 176:239", "176:239 430:409", "430:409 475:100"]
    WP_x = array([-10, 133, 176, 430, 475])
    WP_y = array([-20, 192, 239, 409, 100])
    Init = [4.0, 0, 0, 100]
    for i in range(4):
        sol = TC_Simulate(WP[i], Init, 100.0)

        time = [row[0] for row in sol]

        x = [row[3] for row in sol]

        y = [row[4] for row in sol]

        plt.plot(x, y, "b")
    plt.plot(WP_x, WP_y, "g", label="Way-point path")
    plt.show()