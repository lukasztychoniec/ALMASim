
import os 
from casatasks import simalma
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from casatasks import exportfits
import time

start = time.time()

i = 0
data_dir = 'test_data'
file = 'gauss_cube_' + str(i) + '.fits'
filename = os.path.join(data_dir, file)

i = 4
simalma(
    project = 'gauss_cubes_sim_'+str(i),
	dryrun = False,
	skymodel  = filename,
	inbright = "0.001Jy/pix",
	indirection = "J2000 03h59m59.96s -34d59m59.50s",
	incell = "0.1arcsec",
	incenter = "230GHz",
	inwidth = "10MHz",
	antennalist = ["alma.cycle5.3.cfg"],
	totaltime = "720s",
	mapsize="36arcsec",
	imsize=0,
	pwv = 0.8,
	niter= 0,
	overwrite=True,
	verbose=True
    )

exportfits(imagename='gauss_cubes_sim_'+str(i)+'/gauss_cubes_sim_'+str(i)+'.alma.cycle5.3.noisy.image', fitsimage='gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.dirty.fits')
exportfits(imagename='gauss_cubes_sim_'+str(i)+'/gauss_cubes_sim_'+str(i)+'.alma.cycle5.3.skymodel', fitsimage='gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.skymodel.fits')
os.system('cp gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.dirty.fits {}/'.format(data_dir))
os.system('cp gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.skymodel.fits {}/'.format(data_dir))
print(f'Execution took {time.time() - start} seconds')