# -*- coding: utf-8 -*-

# Original file is located at
#     https://colab.research.google.com/drive/1f8C9Sspb2fGo5s0l91qBrioHCT2sDvNa


#  title: Deriving the Speed–Torque Curve for a Knee Exoskeleton
# author: Keegan Green <kmgreen@sfu.ca>


fs            =  100
window        =    5
reps          =    2
knots_per_rep =  100
nq            = 2000


import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt
import csv


def my_smooth(arr_p, window):

    start = - window // 2
    stop  = + window // 2 + np.size(arr_p)

    idx   = range(start, stop)
    idx_p = range(0, np.size(arr_p))

    arr = np.interp(idx, idx_p, arr_p, period = np.size(arr_p))

    return pd.Series(arr).rolling(window, center = True).mean().to_numpy()[- start : stop]


def my_show(txt):

    plt.grid()

    plt.xlim([ 0,   1 ])
    plt.ylim([ 0, 180 ])

    plt.xticks([ 0,       1 ])
    plt.yticks([ 0, 90, 180 ])

    plt.savefig(txt, format = 'svg', dpi = 300, transparent = True)  # plt.show()


def get_xy(Y, fs, window, cycles, reps, knots_per_rep, nq):

    Y = np.squeeze(Y)

    Y_smooth = pd.Series(Y).rolling(window, center = True).mean().to_numpy()

    from scipy.signal import find_peaks

    peaks, _ = find_peaks(Y_smooth)
    heights = - Y_smooth[peaks]

    peaks = pd.DataFrame(np.c_[peaks, heights]).sort_values(1).iloc[: cycles + 1, 0].sort_values().to_numpy().astype(int)

    T = np.diff(peaks) / fs

    x, y, x_data, y_data = [], [], [], []

    for i in range(0, np.size(peaks) - 1):

        x.append(np.linspace(0, 1, peaks[i + 1] - peaks[i] + 1))
        y.append(Y_smooth[peaks[i] : peaks[i + 1] + 1])

        plt.plot(x[i], y[i], color = '#CFD8DC')

        x_data = np.r_[x_data, x[i][1 :]]
        y_data = np.r_[y_data, y[i][1 :]]

    x_data = np.r_[x[0][0], x_data]
    y_data = np.r_[y[0][0], y_data]

    X1, X2 = np.meshgrid(x_data[1 :], range(0, reps))

    X_data = np.r_[x_data[0], np.ndarray.flatten(X1 + X2)]
    Y_data = np.r_[y_data[0], np.tile(y_data[1 :], reps)]

    n_knots = 1 + knots_per_rep * reps

    from get_natural_cubic_spline_model import get_natural_cubic_spline_model

    model = get_natural_cubic_spline_model(X_data, Y_data, min(X_data), max(X_data), n_knots)

    spl = lambda x: model.predict(x)

    df = pd.DataFrame(np.c_[X_data, Y_data]).pivot_table(values = 1, index = 0, aggfunc = ['mean', 'count'])

    X_data = df.index.to_numpy()

    Y_data = df.to_numpy()[:, 0]  # mean
    w      = df.to_numpy()[:, 1]  # count

  # from scipy.interpolate import UnivariateSpline

  # spl = UnivariateSpline(X_data, Y_data, w, s = 5e4)

    if reps % 2 != 0:

        xq = np.linspace(0, 1, nq + 1)[: -1]
        yq = spl(xq + (reps - 1) / 2)

    else:

        xq1 = np.linspace(0.0, 0.5, round(nq / 2) + 1)
        xq2 = np.linspace(0.5, 1.0, round(nq / 2) + 1)

        yq1 = spl(xq1 + reps / 2 - 0)
        yq2 = spl(xq2 + reps / 2 - 1)

        xq = np.r_[xq1[: -1], (xq1[-1] + xq2[0]) / 2, xq2[1 : -1]]
        yq = np.r_[yq1[: -1], (yq1[-1] + yq2[0]) / 2, yq2[1 : -1]]

    line = plt.plot(np.r_[xq, 1], np.r_[yq, yq[0]], color = '#000000')

    plt.legend(line, ['Cubic Spline'], frameon = False, loc = 'upper center')

    plt.xlabel('Arbitrary Fraction of Gait Cycle')
    plt.ylabel('\n Angle (deg) Below Anterior Horizontal Plane \n')

    return T, xq, yq


# 1. Downhill (`_D`)
# ==================


# 1.2. Upper Leg (`_U`) Angle
# ---------------------------


plt.figure()

Y_U_D = pd.read_csv('https://raw.github.com/keeganmjgreen/MSE-420-Project/master/data/Y_U_D.csv').to_numpy()

T_U_D, xq, yq_U_D = get_xy(Y_U_D, fs, window, 37, reps, knots_per_rep, nq)

plt.title('\n Downhill — Upper Leg \n')

my_show('y_U_D.svg')


# 1.1. Lower Leg (`_L`) Angle
# ---------------------------


plt.figure()

Y_L_D = pd.read_csv('https://raw.github.com/keeganmjgreen/MSE-420-Project/master/data/Y_L_D.csv').to_numpy()

T_L_D, xq, yq_L_D = get_xy(Y_L_D, fs, window, 38, reps, knots_per_rep, nq)

plt.title('\n Downhill — Lower Leg \n')

my_show('y_L_D.svg')


# 1.3. Upper and Lower Leg Angles
# -------------------------------


plt.figure()

θq_U_D = np.roll(yq_U_D, - np.argmin(yq_U_D))
θq_L_D = np.roll(yq_L_D, - np.argmin(yq_L_D))

plt.plot(np.r_[xq, 1], np.r_[θq_U_D, θq_U_D[0]], color = '#BA000D')
plt.plot(np.r_[xq, 1], np.r_[θq_L_D, θq_L_D[0]], color = '#0069C0')

plt.legend(('Upper Leg', 'Lower Leg'), frameon = False, loc = 'upper center', ncol = 2)

plt.xlabel('Matched Fraction of Gait Cycle')
plt.ylabel('\n Angle (deg) Below Anterior Horizontal Plane \n')

plt.title('\n Downhill — Upper and Lower Leg \n')

my_show('θ_D.svg')


# 1.4. Knee (`_K`) Angle
# ----------------------


plt.figure()

θq_K_D = θq_U_D - θq_L_D + 180

plt.plot(np.r_[xq, 1], np.r_[θq_K_D, θq_K_D[0]], color = '#087F23')

plt.xlabel('Matched Fraction of Gait Cycle')
plt.ylabel('\n Angle (deg) \n')

plt.title('\n Downhill — Knee \n')

my_show('θ_K_D.svg')


θq_K_D = np.deg2rad(θq_K_D)

Ts_D = np.mean(np.r_[T_L_D, T_U_D]) / nq

x = np.linspace(0, 1, 2 * nq + 1)[: -1]


# 1.5. Knee Angular Velocity
# --------------------------


plt.figure()

ωq_K_D = np.diff(np.r_[θq_K_D, θq_K_D[0]]) / Ts_D
ωq_K_D = my_smooth(ωq_K_D, window * round(nq / fs))

ω_K_D = np.interp(x, xq + 1 / (2 * nq), ωq_K_D, period = 1)

plt.plot(np.r_[x, 1], np.r_[ω_K_D, ω_K_D[0]], color = '#087F23')

plt.xlabel('Matched Fraction of Gait Cycle')
plt.ylabel('\n Angular Velocity (rad/s) \n')

plt.title('\n Downhill — Knee \n')

plt.grid()

plt.xlim([ 0, 1 ])
plt.ylim([-5, 5 ])

plt.xticks([ 0,    1 ])
plt.yticks([-5, 0, 5 ])

plt.savefig('ω_K_D.svg', format = 'svg', dpi = 300, transparent = True)  # plt.show()


# 1.6. Knee Angular Acceleration
# ------------------------------


plt.figure()

αq_K_D = np.diff(np.r_[ωq_K_D, ωq_K_D[0]]) / Ts_D
αq_K_D = my_smooth(αq_K_D, window * round(nq / fs))

α_K_D = np.interp(x, xq + 1 / (2 * nq), αq_K_D, period = 1)

plt.plot(np.r_[x, 1], np.r_[α_K_D, α_K_D[0]], color = '#087F23')

plt.xlabel('Matched Fraction of Gait Cycle')
plt.ylabel('Angular Acceleration (rad/s²)')

plt.title('\n Downhill — Knee \n')

plt.grid()

plt.xlim([   0,   1 ])
plt.ylim([-150, 150 ])

plt.xticks([   0,      1 ])
plt.yticks([-150, 0, 150 ])

plt.savefig('α_K_D.svg', format = 'svg', dpi = 300, transparent = True)  # plt.show()


# 1.7. Knee Drive Speed–Torque Relationship
# -----------------------------------------


plt.figure()

H   = 1.8
m_B = 1.0
g   = 9.8

l_T = (0.720 - 0.530) * H
l_U = (0.530 - 0.285) * H

ι_D = m_B * (l_T ** 2 + l_U ** 2 - 2 * l_T * l_U * np.cos(np.deg2rad(θq_U_D + 90)))

τq_K_D = ι_D * αq_K_D + m_B * l_U * np.cos(np.deg2rad(θq_U_D)) * g

plt.plot(abs(τq_K_D), abs(ωq_K_D), color = '#087F23')

plt.xlim([ 0, 100 ])
plt.ylim([ 0,   5 ])

plt.xticks([ 0, 100 ])
plt.yticks([ 0,   5 ])

plt.xlabel('Torque (N-m)')
plt.ylabel('\n Speed (rad/s²) \n')

plt.title('\n Downhill — Knee Drive \n')

plt.savefig('ω_vs_τ_K_D.svg', format = 'svg', dpi = 300, transparent = True)  # plt.show()


writer = csv.writer(open('_D.csv', 'w', newline = ''))

writer.writerows([['abs(τq_K_D)', 'abs(ωq_K_D)']])
writer.writerows(np.c_[abs(τq_K_D), abs(ωq_K_D)].tolist())


# 2. Uphill (`_I`)
# ================


# 2.2. Upper Leg (`_U`) Angle
# ---------------------------


plt.figure()

Y_U_I = pd.read_csv('https://raw.github.com/keeganmjgreen/MSE-420-Project/master/data/Y_U_I.csv').to_numpy()

T_U_I, xq, yq_U_I = get_xy(Y_U_I, fs, window, 34, reps, knots_per_rep, nq)

plt.title('Uphill — Upper Leg')

my_show('y_U_I.svg')


# 2.1. Lower Leg (`_L`) Angle
# ---------------------------


plt.figure()

Y_L_I = pd.read_csv('https://raw.github.com/keeganmjgreen/MSE-420-Project/master/data/Y_L_I.csv').to_numpy()

T_L_I, xq, yq_L_I = get_xy(Y_L_I, fs, window, 38, reps, knots_per_rep, nq)

plt.title('Uphill — Lower Leg')

my_show('y_L_I.svg')


# (C) Copyright 2021, Keegan Green.
