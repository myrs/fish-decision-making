import numpy as np
import scipy.optimize
from matplotlib import pyplot as plt


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

    fig, ax = plt.subplots(1, 1)
    ax.set_ylim((y_axis_bottom, y_axis_top))
    ax.set_xlim((x_axis_left, x_axis_right))

    if fit_sin_flag:
        fit_sin_params = fit_sin(xx, yy)
        print("Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % fit_sin_params)

        xx_fit = np.linspace(x_axis_left, x_axis_right, regression_points)
        ax.plot(xx_fit, fit_sin_params["fitfunc"](xx_fit),
                "r-", label="y fit curve", linewidth=2)
        ax.scatter(xx, yy)

        print(fit_sin_params['verbose'])

        ax.set_title(fit_sin_params['verbose'])

        return points, fit_sin_params

    # polyfit
    else:
        polyfit = np.polyfit(xx, yy, 1)
        fit_function = np.poly1d(polyfit)
        xxfit = np.linspace(xx[0], xx[-1], regression_points)
        yyfit = fit_function(xxfit)
        plt.plot(xx, yy, 'o', xxfit, yyfit)

        return points, polyfit


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

    width = 531
    height = 383

    points = [
        [12, 238],
        [34, 292],
        [56, 325],
        [78, 358],
        [100, 351],
        [122, 361],
        [145, 374],
        [167, 341],
        [189, 316],
        [211, 323],
        [232, 273],
        [255, 228],
        [277, 194],
        [299, 144],
        [321, 119],
        [343, 94],
        [365, 78],
        [387, 64],
        [409, 63],
        [431, 51],
        [453, 69],
        [476, 95],
        [497, 138],
        [519, 190]
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

    # points = [
    #     [38, 192],
    #     [76, 213],
    #     [118, 229],
    #     [159, 238],
    #     [197, 242],
    #     [237, 251],
    #     [277, 257],
    #     [319, 264],
    #     [357, 272],
    #     [400, 298],
    #     [436, 308],
    #     [478, 324],
    #     [516, 340],
    #     [557, 359],
    #     [596, 378]
    # ]

    return fit_data(points, width, height, x_axis_left, x_axis_right,
                    y_axis_bottom, y_axis_top, fit_sin_flag=False)


# def fit_acceleration():
#     points = [
#         [14, 209],
#         [24, 206],
#         [34, 224],
#         [44, 222],
#         [54, 228],
#         [64, 222],
#         [74, 225],
#         [83, 219],
#         [93, 218],
#         [103, 223],
#         [113, 226],
#         [123, 225],
#         [133, 224],
#         [143, 227],
#         [153, 218],
#         [163, 209],
#         [173, 197],
#         [183, 187],
#         [193, 140],
#         [202, 100],
#         [212, 167],
#         [222, 195],
#         [232, 174],
#         [242, 153],
#         [252, 135],
#         [262, 117],
#         [272, 111],
#         [282, 91],
#         [292, 86],
#         [302, 81],
#         [312, 75],
#         [322, 62],
#         [332, 61],
#         [342, 48],
#         [352, 36],
#         [361, 41],
#         [371, 58],
#         [381, 57],
#         [391, 69],
#         [401, 63]
#     ]

#     width = 406
#     height = 326

#     x_axis_length = 40
#     y_axis_length = 3

#     points, xx, yy = reformat_data(points, width, height, x_axis_length, y_axis_length)

#     fig, ax = plt.subplots(1, 1)
#     ax.set_ylim((-y_axis_length, y_axis_length))
#     ax.set_xlim((-x_axis_length, x_axis_length))

#     ax.scatter(xx, yy)

#     start = 0
#     stop = 14
#     polyfit1 = np.polyfit(xx[:stop], yy[:stop], 2)
#     poly1 = np.poly1d(polyfit1)
#     xxfit1 = np.linspace(xx[start], xx[stop - 1], 20)
#     yyfit1 = poly1(xxfit1)
#     plt.plot(xx[start:stop - 1], yy[start:stop - 1], 'o', xxfit1, yyfit1)

#     start = 14
#     stop = 20
#     polyfit1 = np.polyfit(xx[start:stop], yy[start:stop], 2)
#     poly1 = np.poly1d(polyfit1)
#     xxfit1 = np.linspace(xx[start], xx[stop - 1], 20)
#     yyfit1 = poly1(xxfit1)
#     plt.plot(xx[start:stop - 1], yy[start:stop - 1], 'o', xxfit1, yyfit1)

#     plt.scatter(xx, yy)

#     return points, xx, yy
