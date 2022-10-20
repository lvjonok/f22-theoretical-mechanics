import matplotlib.pyplot as plt
import numpy as np
import json
import sympy as sm


def yoyo(time, rope_length):
    L = rope_length / 100.0
    g = 9.8418913692
    k = 0.5
    m = 0.06385
    I = 0.0000248
    r = 0.006

    dt = 0.001

    tyv = np.zeros((int(time/dt), 3))

    for i in range(1, tyv.shape[0]):
        tyv[i, 0] = dt * i
        if tyv[i - 1, 1] < L:
            tyv[i, 1] = tyv[i - 1, 1] + tyv[i - 1, 2] * dt
            tyv[i, 2] = tyv[i - 1, 2] + \
                (m * g - k * tyv[i - 1, 2]) / (m + I / (r ** 2)) * dt
        else:
            tyv[i, 1] = 2 * L - tyv[i - 1, 1]
            tyv[i, 2] = -tyv[i - 1, 2]

    tyv[:, 1] = tyv[:, 1] * 100
    return tyv[:, [0, 1]]


def yoyo2(t_end, rope_length):
    m = 0.06385

    p = 0.022530346
    # lx = 0.000020159
    ly = 0.000024800
    # lz = 0.000020384
    r = 0.0065
    mu = 0.005 / 4  # To complex approximation to describe, sorry
    g = 9.8418913692

    I = ly

    t = sm.Symbol('t')
    phi_0, w_0, t_0 = sm.symbols('phi_0 w_0 t_0')
    phi = sm.Function('phi')(t)
    d_phi = sm.Derivative(phi)
    dd_phi = sm.Derivative(d_phi)

    goes_down = (I + m*r**2) * dd_phi - m*r*g + r*mu*d_phi
    goes_up = (I + m*r**2) * dd_phi + m*r*g + r*mu*d_phi

    # display(goes_down)
    # display(goes_up)

    phi_down = sm.dsolve(
        goes_down,
        ics={phi.subs(t, t_0): phi_0,
             phi.diff(t).subs(t, t_0): w_0}
    ).rhs

    w_down = sm.diff(phi_down, t)
    e_down = sm.diff(w_down, t)

    phi_up = sm.dsolve(
        goes_up,
        ics={phi.subs(t, t_0): phi_0,
             phi.diff(t).subs(t, t_0): w_0}
    ).rhs

    w_up = sm.diff(phi_up, t)
    e_up = sm.diff(w_up, t)

    step = 0.01
    time = step

    phi_range = []
    l_range = []
    w_range = []
    e_range = []
    time_range = []

    phi = 0
    w = 0
    e = 0

    h = rope_length
    print(h)
    l = 0
    z = h

    last_desc = 0
    last_asc = 0

    while time < t_end:
        phi_t = sm.lambdify(
            t, phi_down.subs(
                {
                    sm.Symbol('t_0'): time,
                    sm.Symbol('phi_0'): phi,
                    sm.Symbol('w_0'): w
                }
            )
        )
        w_t = sm.lambdify(
            t, w_down.subs(
                {
                    sm.Symbol('t_0'): time,
                    sm.Symbol('w_0'): w
                }
            )
        )
        e_t = sm.lambdify(
            t, e_down.subs(
                {
                    sm.Symbol('t_0'): time,
                    sm.Symbol('w_0'): w
                }
            )
        )

        # print('-'*50)
        # print('Descending')

        while l < h and time < t_end:
            phi = phi_t(time)
            w = w_t(time)
            e = e_t(time)
            l = np.abs(phi) * r
            # print(f"Time: {time}")
            # print(f"\tphi={phi}")
            # print(f"\tw={w}")
            # print(f"\te={e}")
            # print(f"\tl={l}")

            phi_range.append(phi)
            w_range.append(w)
            e_range.append(e)
            l_range.append(l)
            time_range.append(time)

            z = h - l
            time += step

        last_desc = phi

        phi_t = sm.lambdify(
            t, phi_up.subs(
                {
                    sm.Symbol('t_0'): time,
                    sm.Symbol('phi_0'): phi,
                    sm.Symbol('w_0'): w
                }
            )
        )
        w_t = sm.lambdify(
            t, w_up.subs(
                {
                    sm.Symbol('t_0'): time,
                    sm.Symbol('w_0'): w
                }
            )
        )
        e_t = sm.lambdify(
            t, e_up.subs(
                {
                    sm.Symbol('t_0'): time,
                    sm.Symbol('w_0'): w
                }
            )
        )

        # print('-'*50)
        # print('Ascending')
        while w > 0 and time < t_end:
            phi = phi_t(time)
            w = w_t(time)
            e = e_t(time)
            l = np.abs((2*last_desc - phi)) * r
            # print(f"Time: {time}")
            # print(f"\tphi={phi}")
            # print(f"\tw={w}")
            # print(f"\te={e}")
            # print(f"\tl={l}")

            phi_range.append(phi)
            w_range.append(w)
            e_range.append(e)
            l_range.append(l)
            time_range.append(time)

            z = h - l
            time += step
        phi = l / r

    return time_range, l_range


for experiment in range(16):
    sidedata = json.load(open(f'data/{experiment}/side.json'))
    values = yoyo(12, sidedata['l'])
    values2 = yoyo2(12, sidedata['l'] / 100.0)

    # load data for experiment 0
    posy = np.array(json.load(open(f'data/{experiment}/poscm.json')))
    time = np.array(json.load(open(f'data/{experiment}/time.json')))

    posy = posy[:len(time)]

    # pyplot clear plot
    plt.clf()

    plt.plot(values[:, 0], values[:, 1], label="simulation others")
    plt.plot(values2[0], np.array(values2[1]) * 100.0, label="simulation ours")
    plt.plot(time, posy, label="real")

    plt.legend()
    plt.savefig(f'reportimages/comparison_{experiment}.png')
