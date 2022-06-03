import os
import sys
import glob
import time
import argparse
import numpy as np

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
n = len(list(os.listdir(input_dir)))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
indexes = list(np.arange(n))
for i in indexes:
    generate_sims(input_dir, output_dir, i)

print(f'Execution took {time.time() - start} seconds')



"""    
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
print(f'Execution took {time.time() - start} seconds')
"""
