import os
import sys
import glob
import time
import argparse
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
from casatasks import simalma, exportfits

def generate_sims(i, input_dir, output_dir):
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
        mapsize="0",
        pwv=0.8,
        niter=0,
        imsize=0,
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


parser =argparse.ArgumentParser()
parser.add_argument("model_dir", type=str, 
        help='The directory in wich the simulated model cubes are stored;')
parser.add_argument("output_dir", type=str, 
         help='The directory in wich to store the simulated dirty cubes and corresponding skymodels;')
args = parser.parse_args()
input_dir = args.model_dir
output_dir = args.output_dir

n_cores = multiprocessing.cpu_count() // 4
n = len(list(os.listdir(input_dir))) - 1
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


if __name__ == "__main__":
    start = time.time()
    Parallel(n_cores)(delayed(generate_sims)(i, input_dir, output_dir) for i in range(n))
    print(f'Execution took {time.time() - start} seconds')
    os.system('rm -r *.log')
    
