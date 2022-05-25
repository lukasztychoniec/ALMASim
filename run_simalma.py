import os
import sys
import glob


data_dir = "DATA"
filename = os.path.join(data_dir, "gauss_cube_0.fits")
simalma(
    project="gauss_cubes_sim_0",
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
)
