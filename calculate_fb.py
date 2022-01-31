import tifffile
import numpy as np


def run(path, file):
    FREQUENCY = 80000000
    FREE_TAU = 0.4E-09
    BOUND_TAU = 3.4E-09

    omega = 2*np.pi*FREQUENCY
    g_free = 1/(1+(omega*FREE_TAU)**2)
    s_free = (omega*FREE_TAU)/(1+(omega*FREE_TAU)**2)
    g_bound = 1/(1+(omega*BOUND_TAU)**2)
    s_bound = (omega*BOUND_TAU)/(1+(omega*BOUND_TAU)**2)

    gs_im = tifffile.imread(path+'/'+file)
    g_vals = gs_im[0, :, :].flatten()
    s_vals = gs_im[1, :, :].flatten()

    a = np.array([[g_free, s_free, 1],
                  [g_bound, s_bound, 1],
                  [0, 0, 1]])

    x = None
    for pixel in range(np.size(g_vals)):

        y = np.array([g_vals[pixel], s_vals[pixel], 1])
        if x is None:
            if g_vals[pixel]:
                x = np.array([np.linalg.solve(a, y)])
            else:
                x = np.array([[np.nan, np.nan, np.nan]])
        else:
            if g_vals[pixel]:
                x = np.append(x, [np.linalg.solve(a, y)], axis=0)
            else:
                x = np.append(x, np.array([[np.nan, np.nan, np.nan]]), axis=0)

    fb_im = np.empty([3, np.shape(gs_im)[1], np.shape(gs_im)[2]])
    fb_im[0, :, :] = np.array(x[:, 0]).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))
    fb_im[1, :, :] = np.array(x[:, 1]).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))
    fb_im[2, :, :] = np.array(x[:, 2]).reshape((np.shape(gs_im)[1], np.shape(gs_im)[2]))

    return fb_im
