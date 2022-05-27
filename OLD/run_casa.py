import argparse
import glob, os
from natsort import natsorted
import casatasks
import casatools

parser =argparse.ArgumentParser()
parser.add_argument("data_dir", type=str, 
        help='The directory in wich the simulated model cubes are stored;')

args = parser.parse_args()
data_dir = args.data_dir
filelist = natsorted([f for f in os.listdir(data_dir) if '.fits' in f])
for i in range(len(filelist)):
    filename = os.path.join(data_dir, filelist[i])

    simalma(
		project = 'gauss_cubes_sim_'+str(i), 
		overwrite = True,
		skymodel  = filename,
		indirection = "J2000 03h59m59.96s -34d59m59.50s",
		incell = "0.1arcsec",
		inbright = "0.001Jy/pix",
		incenter = "230GHz",
		inwidth = "10MHz",
		antennalist = ["alma.cycle5.3.cfg"],
		totaltime = "720s",
		pwv = 0.8,
		dryrun = False,
		niter= 0
		)