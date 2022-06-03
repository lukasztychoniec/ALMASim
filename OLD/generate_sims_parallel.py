import multiprocessing
from functools import partial
import os
import sys
import glob
import time
import argparse
import numpy as np

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
        pwv=0.8,
        niter=0,
        overwrite=True,
        verbose=False
    )
    exportfits(imagename=project+'/gauss_cube_sim_'+str(i)+'.alma.cycle5.3.noisy.image', 
               fitsimage=project+'/gauss_cube_sim_'+str(i)+'.dirty.fits')
    exportfits(imagename=project+'/gauss_cube_sim_'+str(i)+'.alma.cycle5.3.skymodel', 
               fitsimage=project+'/gauss_cube_sim_'+str(i)+'.skymodel.fits')
    
    
    


#parser =argparse.ArgumentParser()
#parser.add_argument("input_dir", type=str, 
#        help='The directory in wich the simulated model cubes are stored;')
#parser.add_argument("output_dir", type=str, 
#        help='The directory in wich to store the simulated dirty cubes and corresponding skymodels;')
#args = parser.parse_args()

start = time.time()
#input_dir = args.input_dir
#output_dir = args.output_dir
input_dir = "models"
output_dir = "sims"
processes = 16
n = len(list(os.listdir(input_dir))) - 1
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
#pool = multiprocessing.Pool()
#pool = multiprocessing.Pool(processes=processes)
#indexes = list(np.arange(n))
#indexes = [0]
#print('starting')
#pool.map(partial(generate_sims, input_dir=input_dir, output_dir=output_dir), indexes)
#pool.close()
#pool.join()
#print(f'Execution took {time.time() - start} seconds')
#os.system('rm *.log')
#for i in range(n):
#    project = "gauss_cube_sim_" + str(i)
    


#Parallel(n_jobs=2)(
#   delayed(lambda i: generate_sims(input_dir, output_dir, i))
#    (i) for i in range(2))
indexes = np.arange(n)
indexes_chunks = np.split(indexes, 16)
for indexes in indexes_chunks:
    indexes = list(indexes)
    pool = multiprocessing.Pool(processes=processes)
    pool.map(partial(generate_sims, input_dir=input_dir, output_dir=output_dir), indexes)
    pool.close()
    pool.join()
    for index in indexes:
        project = "gauss_cube_sim_" + str(index)
        os.system('cp ' + project + '/gauss_cube_sim_'+str(i)+'.dirty.fits {}/'.format(output_dir))
        os.system('cp ' + project + '/gauss_cube_sim_'+str(i)+'.skymodel.fits {}/'.format(output_dir))
        os.system('rm -r {}'.format(project))
