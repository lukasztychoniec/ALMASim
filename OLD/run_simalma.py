import os
import sys
import glob
import time


start = time.time()
data_dir = "test_data"
filename = os.path.join(data_dir, "gauss_cube_0.fits")
i = 0
simalma(
    project="gauss_cubes_sim_" + str(i),
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
    verbose=True
)

exportfits(imagename='gauss_cubes_sim_'+str(i)+'/gauss_cubes_sim_'+str(i)+'.alma.cycle5.3.noisy.image', fitsimage='gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.dirty.fits')
exportfits(imagename='gauss_cubes_sim_'+str(i)+'/gauss_cubes_sim_'+str(i)+'.alma.cycle5.3.skymodel', fitsimage='gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.skymodel.fits')
os.system('cp gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.dirty.fits {}/'.format(data_dir))
#os.system('cp gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.tclean.fits gauss_cubes/')
os.system('cp gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.skymodel.fits {}/'.format(data_dir))
print(f'Execution took {time.time() - start} seconds')
