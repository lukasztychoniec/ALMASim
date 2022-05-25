import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import gridspec
from astropy.wcs import WCS
from astropy import constants as const
import tycholib_jupyter_finalpaper_v2 as tj
import pandas as pd
import sys

original_stdout = sys.stdout


catalog = pd.read_csv('gauss_cubes_030522.csv')
catalog_conv = pd.read_csv('gauss_cubes_030522_converted.csv')



with open('gauss_cubes_dirty_fixed_140522.csv','w') as file:

	sys.stdout = file

	print ('cube_id, comp_num, pos_x, pos_y, ra, dec, line_chan, cont_level, line_peak_with_cont, line_peak_contsub, cont_area_sum,  int_box, line_integrated, line_box')
	print ('int, int,pix, pix, deg, deg, int, Jy/beam, Jy/beam, Jy/beam, Jy/beam,  pix, Jy/beam, int')



	for i in range(100):
		cube_index = i
		linedf = catalog.loc[(catalog.file == cube_index)].reset_index()
		comp_num = len(linedf)

		if comp_num <5:
				continue

		convdf = catalog_conv.loc[(catalog_conv.file == cube_index)].reset_index()

		directory = 'gauss_sims/gauss_cubes_sim_{}/'.format(i)
		image = directory + 'gauss_cube_sim_{}.dirty.fits'.format(i)
		dataset, header = fits.getdata(image, header=True)
		dataset = dataset[0,:,:,:]
		w = WCS(header)
		w = w.dropaxis(3)
		w = w.dropaxis(2)


		for k in range(len(linedf)):
			x = int(linedf['center_x'][k])
			y = int(linedf['center_y'][k])
			width_x = int(linedf['width_x'][k])
			width_y = int(linedf['width_y'][k])
			line_fwhm = int(linedf['line_fwhm'][k])
			ra = convdf['ra'][k]
			dec = convdf['dec'][k]
			cont_level=np.max(dataset[0,y-2:y+2,x-2:x+2])
			if width_x > width_y:
				box = width_x*4
			else:
				box = width_y*4
#		print('box',box)
			cont_area_sum =np.sum(dataset[0,y-box:y+box,x-box:x+width_x+box])
		
		#print ('continuum level {} Jy/pix'.format(cont_level))
			line_pos = int(linedf['line_pos'][k])
			line_peak_with_cont = np.max(dataset[line_pos-1:line_pos+1,y-2:y+2,x-2:x+2])
		#print ('line peak level with cont {} Jy/pix'.format(line_peak_with_cont))
			line_peak_contsub = line_peak_with_cont - cont_level
		#print ('line peak level contsub {} Jy/pix'.format(line_peak_contsub))

#		print ('line_fwhm',line_fwhm)

			chan_no = np.shape(dataset[line_pos-3*line_fwhm:line_pos+line_fwhm*3,y-box:y+box,x-box:x+width_x+box])[0]
			line_integrated  = np.sum(dataset[line_pos-3*line_fwhm:line_pos+line_fwhm*3,y-box:y+box,x-box:x+width_x+box])-chan_no*cont_area_sum 
			



			print ('%i, %i, %i, %i, %.8f, %.8f, %i, %.8f, %.8f, %.8f, %.8f, %i, %.8f,  %i '%(i, comp_num, x , y, ra, dec, line_pos, cont_level, line_peak_with_cont, line_peak_contsub, cont_area_sum,  box, line_integrated, chan_no))



sys.stdout = original_stdout


