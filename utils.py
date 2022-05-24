"""
Utility Functions
"""
import numpy as np
from math import pi
import random


def gaussian(x, amp, cen, fwhm):
    """
    Generates a 1D Gaussian given the following input parameters:
    x: position
    amp: amplitude
    fwhm: fwhm
    level: level
    """
    return amp*np.exp(-(x-cen)**2/(2*(fwhm/2.35482)**2))


def twodgaussian(amplitude, center_x, center_y, width_x, width_y, angle, idxs):
    angle = pi/180. * angle
    rcen_x = center_x * np.cos(angle) - center_y * np.sin(angle)
    rcen_y = center_x * np.sin(angle) + center_y * np.cos(angle)
    xp = idxs[0] * np.cos(angle) - idxs[1] * np.sin(angle)
    yp = idxs[0] * np.sin(angle) + idxs[1] * np.cos(angle)
    g = amplitude*np.exp(-(((rcen_x-xp)/width_x)**2+((rcen_y-yp)/width_y)**2)/2.)
    return g


def make_cube(i, amps, xyposs, fwhms, angles,
              line_centres, line_fwhms, idxs, z_idxs):
    number_of_components = random.randint(2,5)
    lines = []
    images = []
    params = []
    for _ in range(number_of_components):
        # Random choice of line parameters
        line_amp = np.random.choice(amps)
        line_cent = np.random.choice(line_centres)
        line_fwhm = np.random.choice(line_fwhms)
        lines.append(gaussian(z_idxs, line_amp, line_cent, line_fwhm))

        # Random choice of source parameters
        amp = np.random.choice(amps)
        pos_x =  np.random.choice(xyposs)
        pos_y =  np.random.choice(xyposs)
        fwhm_x = np.random.choice(fwhms)
        fwhm_y = np.random.choice(fwhms)
        pa = np.random.choice(angles)
        images.append(twodgaussian(amp, pos_x, pos_y, fwhm_x, fwhm_y, pa, idxs))
        params.append([i, amp, pos_x, pos_y, fwhm_x, fwhm_y, pa, line_amp, line_fwhm, line_cent])
    image = np.sum(images, axis=0)
    cube = np.ones([128, 350, 350]) * image
    for z in range(cube.shape[0]):
        for l in range(len(lines)):
            cube[z, :, :] += lines[l][z] * images[l]
    return cube, params



        
