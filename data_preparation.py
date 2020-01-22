import numpy as np
import scipy.optimize
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator


def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1] - tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    # excluding the zero frequency "peak", which is related to offset
    guess_freq = abs(ff[np.argmax(Fyy[1:]) + 1])
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c): return A * np.sin(w * t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w / (2. * np.pi)
    fitfunc = lambda t: A * np.sin(w * t + p) + c

    verbose = f'${A:.2f} \\cdot \\sin ({w:.2f} \\cdot x + {p:.2f}) + {c:.2f}$'

    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1. / f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess, popt, pcov), "verbose": verbose}


def fit_tan(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1] - tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    # excluding the zero frequency "peak", which is related to offset
    guess_freq = abs(ff[np.argmax(Fyy[1:]) + 1])
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])

    def tanfunc(t, A, w, p, c): return A * np.tan(w * t + p) + c
    popt, pcov = scipy.optimize.curve_fit(tanfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w / (2. * np.pi)
    fitfunc = lambda t: A * np.tan(w * t + p) + c

    verbose = f'${A:.2f} \\cdot \\tan ({w:.2f} \\cdot x + {p:.2f}) + {c:.2f}$'

    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1. / f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess, popt, pcov), "verbose": verbose}


# def resize_x(x, width, x_axis_length):
#     full_x_axis_length = 2 * x_axis_length
#     x_resize = full_x_axis_length / width
#     return x * x_resize - x_axis_length

def resize_y(y, height, y_axis_bottom, y_axis_top):
    y = height - y
    full_y_axis_length = y_axis_top - y_axis_bottom
    y_resize = full_y_axis_length / height
    return y * y_resize + y_axis_bottom


def resize_x(x, width, x_axis_left, x_axis_right):
    full_x_axis_length = x_axis_right - x_axis_left
    x_resize = full_x_axis_length / width
    return x * x_resize + x_axis_left

# def resize_y(y, height, y_axis_length):
#     y = height - y
#     fill_y_axis_length = 2 * y_axis_length
#     y_resize = fill_y_axis_length / height
#     return y * y_resize - y_axis_length


def reformat_data(points, width, height, x_axis_right, x_axis_left,
                  y_axis_bottom, y_axis_top):
    new_points = []

    for point in points:
        new_x = resize_x(point[0], width, x_axis_left, x_axis_right)
        new_y = resize_y(point[1], height, y_axis_bottom, y_axis_top)

        new_point = [new_x, new_y]
        new_points.append(new_point)

    new_points = np.array(new_points)
    xx = new_points[:, 0]
    yy = new_points[:, 1]

    return new_points, xx, yy


def fit_data(points, width, height, x_axis_left, x_axis_right,
             y_axis_bottom, y_axis_top, regression_points=50, fit_sin_flag=True):

    points, xx, yy = reformat_data(points, width, height, x_axis_right, x_axis_left,
                                   y_axis_bottom, y_axis_top)

    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.set_ylim((y_axis_bottom, y_axis_top))
    ax.set_xlim((x_axis_left, x_axis_right))

    if fit_sin_flag:
        ax.set_xlabel('diction to neighbor (rad)')
        ax.set_ylabel('fish tuning angle (rad/second)')
        ax.xaxis.set_major_formatter(FuncFormatter(
            lambda val, pos: '{:.0g}$\pi$'.format(val / np.pi) if val != 0 else '0'
        ))
        ax.xaxis.set_major_locator(MultipleLocator(base=np.pi / 4))        

        fit_sin_params = fit_sin(xx, yy)
        print("Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % fit_sin_params)

        xx_fit = np.linspace(x_axis_left, x_axis_right, regression_points)
        ax.plot(xx_fit, fit_sin_params["fitfunc"](xx_fit),
                "r-", label="y fit curve", linewidth=2)
        ax.scatter(xx, yy)

        print(fit_sin_params['verbose'])

        return points, fit_sin_params

    # polyfit
    else:
        ax.set_xlabel('fish speed ($cm/s$)')
        ax.set_ylabel('fish acceleration ($cm/s^2$)')
        polyfit = np.polyfit(xx, yy, 1)
        fit_function = np.poly1d(polyfit)
        xxfit = np.linspace(xx[0], xx[-1], regression_points)
        yyfit = fit_function(xxfit)
        ax.plot(xx, yy, 'o', xxfit, yyfit)

        return points, polyfit

    fig.show()


def fit_rotation_angle():
    # rotation angle
    width = 549
    height = 458

    x_axis_right = -np.pi
    x_axis_left = np.pi
    y_axis_bottom = -0.6
    y_axis_top = 0.6

    points = [
        [12, 274],
        [35, 331],
        [58, 380],
        [80, 410],
        [103, 422],
        [127, 425],
        [149, 429],
        [172, 425],
        [195, 408],
        [218, 386],
        [241, 336],
        [263, 275],
        [287, 215],
        [309, 158],
        [332, 115],
        [353, 89],
        [377, 67],
        [402, 70],
        [424, 70],
        [446, 67],
        [468, 95],
        [491, 124],
        [514, 170],
        [537, 224]
    ]

    return fit_data(points, width, height, x_axis_left, x_axis_right,
                    y_axis_bottom, y_axis_top)


def fit_speed_acceleration():
    # rotation angle
    width = 636
    height = 494

    x_axis_left = 0
    x_axis_right = 20
    y_axis_bottom = -6
    y_axis_top = 6

    points = [
        [38, 192],
        [118, 229],
        [197, 242],
        [277, 257],
        [357, 272],
        [436, 308],
        [516, 340],
        [596, 378]
    ]

    return fit_data(points, width, height, x_axis_left, x_axis_right,
                    y_axis_bottom, y_axis_top, fit_sin_flag=False)