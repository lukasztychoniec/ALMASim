"""
Utility Functions
"""
import numpy as np
from math import pi
import random
from astropy.io import fits
import pandas as pd
import os
from tqdm import tqdm


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


def threedgaussian(amplitude, spind, chan, center_x, center_y, width_x, width_y, angle, idxs):
    angle = pi/180. * angle
    rcen_x = center_x * np.cos(angle) - center_y * np.sin(angle)
    rcen_y = center_x * np.sin(angle) + center_y * np.cos(angle)
    xp = idxs[0] * np.cos(angle) - idxs[1] * np.sin(angle)
    yp = idxs[0] * np.sin(angle) + idxs[1] * np.cos(angle)
    v1 = 230e9
    v2 = v1+100e6*chan

    g = (np.log10(amplitude) - (spind) * np.log10(v1/v2))*np.exp(-(((rcen_x-xp)/width_x)**2+((rcen_y-yp)/width_y)**2)/2.)
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
        params.append([int(i), round(amp, 2), round(pos_x, 2), round(pos_y, 2), 
                       round(fwhm_x, 2), round(fwhm_y, 2), round(pa, 2), round(line_amp, 2), 
                       round(line_fwhm, 2), round(line_cent, 2)])
    image = np.sum(images, axis=0)
    cube = np.ones([128, 350, 350]) * image
    for z in range(cube.shape[0]):
        for l in range(len(lines)):
            cube[z, :, :] += lines[l][z] * images[l]
    return cube, params



def make_spind_cube(i, amps, xyposs, fwhms, angles,
              line_centres, line_fwhms, spectral_indexes, idxs, z_idxs):
    number_of_components = random.randint(2,5)
    lines = []
    images = []
    params = []
    cube = np.ones([128, 350, 350])

    for _ in range(number_of_components):
        # Random choice of line parameters
        line_amp = np.random.choice(amps)
        line_cent = np.random.choice(line_centres)
        line_fwhm = np.random.choice(line_fwhms)

        # Random choice of source parameters
        amp = np.random.choice(amps)
        pos_x =  np.random.choice(xyposs)
        pos_y =  np.random.choice(xyposs)
        fwhm_x = np.random.choice(fwhms)
        fwhm_y = np.random.choice(fwhms)
        pa = np.random.choice(angles)
        spidx = np.random.choice(spectral_indexes)
        for z in range(cube.shape[0]):
            temp_source =  threedgaussian(amp, spidx, z, pos_x, pos_y, fwhm_x, fwhm_y, pa, idxs)
            cube[z, :, :] += temp_source
            cube[z, :, :] += gaussian(z_idxs, line_amp, line_cent, line_fwhm)[z] * temp_source

        params.append([int(i), round(amp, 2), round(pos_x, 2), round(pos_y, 2),
                       round(fwhm_x, 2), round(fwhm_y, 2), round(pa, 2), round(line_amp, 2),
                       round(line_fwhm, 2), round(line_cent, 2), round(spidx,2)])

    image = np.sum(images, axis=0)

    return cube, params



def generate_cubes(data_dir, csv_name, n):
    columns = ['ID', 'amplitude', 'x', 'y', 'width_x', 
               'width_y', 'angle', 'line_peak', 'line_fwhm', 'z', 'sp_idx']
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    amps = np.linspace(1.,5.,num=100).astype(np.float)
    xyposs = np.arange(100,250).astype(np.float)
    fwhms = np.linspace(2.,8.,num=100).astype(np.float)
    angles = np.linspace(0,90,num=900).astype(np.float)
    line_centres = np.linspace(20, 100, num=100).astype(np.float)
    line_fwhms = np.linspace(3, 10, num=100).astype(np.float)
    spectral_indexes = np.linspace(-2, 2, num=100).astype(np.float)
    idxs = np.indices([350, 350])
    z_idxs = np.linspace(0, 128, 128)
    parameters = []
    print('Generating Cubes....')
    for i in tqdm(range(n)):
        #cube, params = make_cube(i, amps, xyposs, fwhms, angles, line_centres, line_fwhms, idxs, z_idxs)
        cube, params = make_spind_cube(i, amps, xyposs, fwhms, angles, line_centres, line_fwhms, spectral_indexes, idxs, z_idxs)

        hdu = fits.PrimaryHDU(data=cube)
        hdu.writeto(data_dir + '/gauss_cube_' + str(i) + '.fits', overwrite=True)
        for par in params:
            parameters.append(par)
    parameters = np.array(parameters)
    df = pd.DataFrame(parameters, columns=columns)
    df.to_csv(os.path.join(data_dir, csv_name), index=False)
    print('Finished!')

            
def generate_sims(input_dir, output_dir, i):
    filename = os.path.join(input_dir, "gauss_cube_{}.fits".format(str(i)))
    project = "gauss_cube_sim_" + str(i)
    simalma(
        project=project,
        dryrun=False,
        skymodel=filename,
        inbright="0.001Jy/pix",
        indirection="J2000 03h59m59.96s -34d59m59.50s",
        incell="0.1arcsec",
        incenter="230GHz",
        inwidth="10MHz",
        antennalist=["alma.cycle5.3.cfg"],
        totaltime="720s",
        pwv=0.8,
        niter=0,
        overwrite=True,
        verbose=False
    )
    exportfits(imagename=project+'/gauss_cube_sim_'+str(i)+'.alma.cycle5.3.noisy.image', 
               fitsimage=project+'/gauss_cube_sim_'+str(i)+'.dirty.fits')
    exportfits(imagename=project+'/gauss_cube_sim_'+str(i)+'.alma.cycle5.3.skymodel', 
               fitsimage=project+'/gauss_cube_sim_'+str(i)+'.skymodel.fits')

    os.system('cp ' + project + '/gauss_cube_sim_'+str(i)+'.dirty.fits {}/'.format(output_dir))
    os.system('cp ' + project + '/gauss_cube_sim_'+str(i)+'.skymodel.fits {}/'.format(output_dir))
    os.system('rm -r {}'.format(project))
    os.system('rm *.last')

