import numpy as np
from math import pi
import random
from astropy.io import fits
import pandas as pd
import os
from tqdm import tqdm
import utils
from joblib import Parallel, delayed
import multiprocessing
import time
import glob
import argparse

def make_cube(i, data_dir, amps, xyposs, fwhms, angles, 
              line_centres, line_fwhms, spectral_indexes, 
              idxs, z_idxs):
    number_of_components = random.randint(2,5)
    params = []
    cube = np.ones([128, 360, 360])
    columns = ['ID', 'amplitude', 'x', 'y', 'width_x', 
               'width_y', 'angle', 'line_peak', 'line_fwhm', 'z', 'sp_idx']
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
            temp_source =  utils.threedgaussian(amp, spidx, z, pos_x, pos_y, fwhm_x, fwhm_y, pa, idxs)
            cube[z, :, :] += temp_source
            cube[z, :, :] += utils.gaussian(z_idxs, line_amp, line_cent, line_fwhm)[z] * temp_source

        params.append([int(i), round(amp, 2), round(pos_x, 2), round(pos_y, 2),
                       round(fwhm_x, 2), round(fwhm_y, 2), round(pa, 2), round(line_amp, 2),
                       round(line_fwhm, 2), round(line_cent, 2), round(spidx,2)])
    hdu = fits.PrimaryHDU(data=cube)
    hdu.writeto(data_dir + '/gauss_cube_' + str(i) + '.fits', overwrite=True)
    params = np.array(params)
    df = pd.DataFrame(params, columns=columns)
    df.to_csv(os.path.join(data_dir, 'params_{}.csv'.format(i)), index=False)



amps = np.linspace(1.,5.,num=100).astype(float)
xyposs = np.arange(100,250).astype(float)
fwhms = np.linspace(2.,8.,num=100).astype(float)
angles = np.linspace(0,90,num=900).astype(float)
line_centres = np.linspace(20, 100, num=100).astype(float)
line_fwhms = np.linspace(3, 10, num=100).astype(float)
spectral_indexes = np.linspace(-2, 2, num=100).astype(float)
idxs = np.indices([360, 360])
z_idxs = np.linspace(0, 128, 128)

parser =argparse.ArgumentParser()
parser.add_argument("data_dir", type=str, 
        help='The directory in wich the simulated model cubes are stored;')
parser.add_argument("csv_name", type=str, 
        help='The name of the .csv file in which to store the simulated source parameters;')
parser.add_argument('n', type=int, help='The number of cubes to generate;')
args = parser.parse_args()

data_dir = args.data_dir
csv_name = args.csv_name
n = args.n

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

n_cores = multiprocessing.cpu_count() // 4

if __name__ == '__main__':
    start = time.time()
    Parallel(n_cores)(delayed(make_cube)(i, data_dir,
             amps, xyposs, fwhms, angles, line_centres, 
             line_fwhms, spectral_indexes, idxs, z_idxs) for i in tqdm(range(n)))
    files = os.path.join(data_dir, 'params_*.csv')
    files = glob.glob(files)
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    os.system("rm -r {}/*.csv".format(data_dir))
    df = df.sort_values(by="ID")
    df.to_csv(os.path.join(data_dir, csv_name), index=False)
    print(f'Execution took {time.time() - start} seconds')
