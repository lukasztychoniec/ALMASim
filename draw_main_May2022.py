import matplotlib.pyplot as plt
from math import pi
import numpy as np,numpy
import os
from astropy.io import fits
import sys
import random

original_stdout = sys.stdout


def gaussian(x, amp, cen, fwhm, level):
    return level+amp*np.exp(-(x-cen)**2/(2*(fwhm/2.35482)**2))



def twodgaussian(inpars, circle=0, rotate=1, vheight=1, shape=None):
    """Returns a 2d gaussian function of the form:
        x' = numpy.cos(rota) * x - numpy.sin(rota) * y
        y' = numpy.sin(rota) * x + numpy.cos(rota) * y
        (rota should be in degrees)
        g = b + a * numpy.exp ( - ( ((x-center_x)/width_x)**2 +
        ((y-center_y)/width_y)**2 ) / 2 )

        inpars = [b,a,center_x,center_y,width_x,width_y,rota]
                 (b is background height, a is peak amplitude)

        where x and y are the input parameters of the returned function,
        and all other parameters are specified by this function

        However, the above values are passed by list.  The list should be:
        inpars = (height,amplitude,center_x,center_y,width_x,width_y,rota)

        You can choose to ignore / neglect some of the above input parameters 
            unumpy.sing the following options:
            circle=0 - default is an elliptical gaussian (different x, y
                widths), but can reduce the input by one parameter if it's a
                circular gaussian
            rotate=1 - default allows rotation of the gaussian ellipse.  Can
                remove last parameter by setting rotate=0
            vheight=1 - default allows a variable height-above-zero, i.e. an
                additive constant for the Gaussian function.  Can remove first
                parameter by setting this to 0
            shape=None - if shape is set (to a 2-parameter list) then returns
                an image with the gaussian defined by inpars
        """

    inpars_old = inpars
    inpars = list(inpars)
    if vheight == 1:
        height = inpars.pop(0)
        height = float(height)
    else:
        height = float(0)
    amplitude, center_y, center_x = inpars.pop(0),inpars.pop(0),inpars.pop(0)
    amplitude = float(amplitude)
    center_x = float(center_x)
    center_y = float(center_y)
    if circle == 1:
        width = inpars.pop(0)
        width_x = float(width)
        width_y = float(width)
        rotate = 0
    else:
        width_x, width_y = inpars.pop(0),inpars.pop(0)
        width_x = float(width_x)
        width_y = float(width_y)
    if rotate == 1:
        rota = inpars.pop(0)
        rota = pi/180. * float(rota)
        rcen_x = center_x * numpy.cos(rota) - center_y * numpy.sin(rota)
        rcen_y = center_x * numpy.sin(rota) + center_y * numpy.cos(rota)
    else:
        rcen_x = center_x
        rcen_y = center_y
    if len(inpars) > 0:
        raise ValueError("There are still input parameters:" + str(inpars) + \
                " and you've input: " + str(inpars_old) + \
                " circle=%d, rotate=%d, vheight=%d" % (circle,rotate,vheight) )
            
    def rotgauss(x,y):
        if rotate==1:
            xp = x * numpy.cos(rota) - y * numpy.sin(rota)
            yp = x * numpy.sin(rota) + y * numpy.cos(rota)
        else:
            xp = x
            yp = y
        g = height+amplitude*numpy.exp(
            -(((rcen_x-xp)/width_x)**2+
            ((rcen_y-yp)/width_y)**2)/2.)
        return g
    if shape is not None:
        return rotgauss(*numpy.indices(shape))
    else:
        return rotgauss
#####################

rand1 = np.linspace(1.,5.,num=100)
rand2 = np.arange(100,250)
rand3 = np.linspace(2.,8.,num=100)
rand4 = np.linspace(0,90,num=900)

print ('in')

directory = 'cubes_030522'
with open(directory+'/gauss_cubes.csv','w') as file:
	sys.stdout = file
	print ('#file,amplitude,center_x,center_y,width_x,width_y,rot_angle,line_peak,line_fwhm,line_pos,sum_peak')

	CompDictionary = {}
	LineDict = {}
	#loop over all simulations
	#for i in range(99):
	for i in range(1000):
		number_of_components = random.randint(2,5)
			#loop over components

		final_image = np.zeros([350,350])

		# let's create line for each gaussian separately
		for k in range(number_of_components):
			LineDict[str(k)]={'amp':'',
					  'cen':'',
					  'fwhm':'',
					  'level':0,
					  'gauss_y':''}
			chan_in=0
			chan_out=128
			line_amp = np.random.choice(np.linspace(1.,5,num=100))
			line_cen = np.random.choice(np.linspace(20,100,num=100))
			line_fwhm = np.random.choice(np.linspace(3,10,num=100))
			line_level= 0
			xx = np.linspace(chan_in,chan_out,num=chan_out-chan_in)
			gauss_y = gaussian(xx, line_amp, line_cen, line_fwhm, line_level)
			LineDict[str(k)]={'amp':line_amp,
					  'cen':line_cen,
					  'fwhm':line_fwhm,
					  'level':line_level,
					  'gauss_y':gauss_y}


		for k in range(number_of_components):
				CompDictionary[str(k)]={'amp':'',
							   'xy':'',
							   'fwhm_x,fwhm_y':'',
							   'pa':'',
						  	   'image_array':''}

				amp = np.random.choice(rand1)
				pos_x =  np.random.choice(rand2)
				pos_y =  np.random.choice(rand2)
				fwhm_x = np.random.choice(rand3)
				fwhm_y = np.random.choice(rand3)
				pa = np.random.choice(rand4)
				inpars1 = [0,amp,pos_x,pos_y,fwhm_x,fwhm_y,pa]
				image  = twodgaussian(inpars1,shape=[350,350])
				
				CompDictionary[str(k)]['amp']=amp
				CompDictionary[str(k)]['xy']=[pos_x,pos_y]
				CompDictionary[str(k)]['fwhm']=[fwhm_x,fwhm_y]
				CompDictionary[str(k)]['pa']=pa
				CompDictionary[str(k)]['image_array']=image
			
				final_image = final_image+image

				line_peak = LineDict[str(k)]['amp']
				line_fwhm = LineDict[str(k)]['fwhm']
				line_center = LineDict[str(k)]['cen']
				print ("%i,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f"%(i,amp,pos_x,pos_y,fwhm_x,fwhm_y,pa,line_peak,line_fwhm,line_center,amp+line_peak))


		cube = np.zeros((128,350,350))
		for j in range(128):
			cube[j,:,:]=final_image
			for l in range(len(LineDict)):
		    		cube[j,:,:]+=LineDict[str(l)]['gauss_y'][j]*CompDictionary[str(l)]['image_array']

		fig, ax = plt.subplots()
		ax.imshow(final_image)
		fig.savefig(directory+'/gauss_'+str(i)+'.png')



		hdu = fits.PrimaryHDU(data=cube)
		hdu.writeto(directory+'/gauss_cube_'+str(i)+'.fits',overwrite=True)

sys.stdout = original_stdout

print ('out')



