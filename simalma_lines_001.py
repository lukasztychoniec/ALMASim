#run this in casa

#set simalma to default parameters

import glob, os


directory = 'cubes_030522'


for i in range(1000):


	filename= directory+'/gauss_cube_'+str(i)+'.fits'

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
	
	### clean image
	if False:
		vis = 'gauss_cubes_sim_'+str(i)+'/gauss_cubes_sim_'+str(i)+'.alma.cycle5.3.noisy.ms'
		tclean(vis=vis,
			imagename = 'gauss_cubes_sim_'+str(i)+'/gauss_cubes_sim_'+str(i)+'.tclean',
			specmode='cube',
			outframe = 'LSRK',
			restfreq = '230GHz',
			deconvolver = 'hogbom',
			gridder = 'standard',
			imsize = [350,350],
			cell = '0.1arcsec',
			weighting = 'briggs',
			restoringbeam = 'common',
			interactive = False,
			niter = 1000,
			threshold = '0.00004Jy',
			usemask = 'auto-multithresh',
			sidelobethreshold = 2.0,
			noisethreshold = 4.25,
			lownoisethreshold = 1.5,
			minbeamfrac = 0.3,
			growiterations = 75,
			negativethreshold=15.0,
			verbose = True)
	#exportfits(imagename='gauss_cubes_sim_'+str(i)+'/gauss_cubes_sim_'+str(i)+'.tclean.image', 			fitsimage='gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.tclean.fits')
	exportfits(imagename='gauss_cubes_sim_'+str(i)+'/gauss_cubes_sim_'+str(i)+'.alma.cycle5.3.noisy.image', fitsimage='gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.dirty.fits')
	exportfits(imagename='gauss_cubes_sim_'+str(i)+'/gauss_cubes_sim_'+str(i)+'.alma.cycle5.3.skymodel', fitsimage='gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.skymodel.fits')



	os.system('cp gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.dirty.fits final_output_030522/')
	#os.system('cp gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.tclean.fits gauss_cubes/')
	os.system('cp gauss_cubes_sim_'+str(i)+'/gauss_cube_sim_'+str(i)+'.skymodel.fits final_output_030522/')

	os.system('mv -f gauss_cubes_sim_'+str(i)+' gauss_sims/')


