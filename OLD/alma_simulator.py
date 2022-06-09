from casatasks import simalma, exportfits
import os
import sys
import glob
import time
import argparse
import numpy as np

def generate_sims(i, input_dir, output_dir):
    filename = os.path.join(input_dir, "gauss_cube_" + str(i) + ".fits")
    project = 'sim'
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
        verbose=True
    )
    exportfits(imagename=project+'/sim.alma.cycle5.3.noisy.image', 
               fitsimage=project+'/gauss_cube_sim_'+ str(i) +'.dirty.fits')
    exportfits(imagename=project+'/sim.alma.cycle5.3.skymodel', 
               fitsimage=project+'/gauss_cube_sim_'+ str(i) +'.skymodel.fits')
    os.system('cp ' + project + '/gauss_cube_sim_'+ str(i) +'.dirty.fits {}/'.format(output_dir))
    os.system('cp ' + project + '/gauss_cube_sim_'+ str(i) +'.skymodel.fits {}/'.format(output_dir))
    os.system('rm -r {}'.format(project))

parser =argparse.ArgumentParser()
parser.add_argument("i", type=str, 
        help='the index of the simulation to be run;')
parser.add_argument("model_dir", type=str, 
        help='The directory in wich the simulated model cubes are stored;')
parser.add_argument("output_dir", type=str, 
         help='The directory in wich to store the simulated dirty cubes and corresponding skymodels;')

args = parser.parse_args()
input_dir = args.model_dir
output_dir = args.output_dir
i = args.i
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

generate_sims(i, input_dir, output_dir)
