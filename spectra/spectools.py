"""
Collection of functions for dealing with spectra

"""

LIGHTSPEED = 2.9979E5

def generate_lyman(n, z=0):
    """ 
    Generate a list of Lyman line locations in wavelength.
    
    Line locations are given in Angstroms.
    """
    
    R = 1.0968E7 * 1E-10 # Rydberg constant in A
    line_list = [ 1. / (R * (1. - ( 1. / (i*i) ) ) ) for i in range(2,n+2)  ]

    return line_list


def generate_balmer(n, z=0):
    """
    Generate a list of Hydrogen Balmer lines 

    """

    R = 1.0968E7 * 1E-10 # Rydberg constant in A
    line_list = [ 1. / (R * (1./4 - ( 1. / (i*i) ) ) ) for i in range(3,n+3)  ]

    return line_list


def wavelength_to_velocity(wavelength, zeropoint):
    """
    Convert a wavelength array into velocity around a specific zeropoint.

    Returns velocity in km/s

    """

    zeropoint = float( zeropoint )

    z = (wavelength - float(zeropoint) ) / (zeropoint)
    velocity = z * LIGHTSPEED

    return velocity


def velocity_to_wavelength(velocity, zeropoint):
    return zeropoint * velocity/LIGHTSPEED + zeropoint


def luminosity_distance(redshift,flux):
    from numpy import pi
   
    distance = LIGHTSPEED * redshift
    luminosity = flux * pi * distance**2
  
    return luminosity


def vel_to_z(velocity, zeropt):
    import numpy as np
    ###actually shifts lambda by a velocity
    #return zeropt + zeropt * (np.sqrt( (1+velocity/LIGHTSPEED) / (1-velocity/LIGHTSPEED) ) -1 )
    return zeropt + zeropt * (velocity / LIGHTSPEED)


def vel_to_z_actually(velocity):
    #approximate formula with v << C
    import numpy as np
    z = velocity / LIGHTSPEED
    #z = np.sqrt( (1+velocity/LIGHTSPEED) / (1-velocity/LIGHTSPEED) ) -1

    return z


def z_to_vel(redshift):
    ###broken
    return LIGHTSPEED * redshift


def rest_wavelength(obs_wave,redshift):
    """
    Calculate the rest wavelength from observed wavelength and redshift.

    """

    return obs_wave / (redshift + 1)


def obs_wavelength(rest_wave,redshift):
    """
    Calculate the observed wavelength from rest wavelengh and redshift.

    """

    return rest_wave * (redshift + 1)


def fft_correlate(a,b,alims=(0,-1),blims=None,dispersion=None):
    """ Perform FFT correlation between two spectra
    """

    try: scipy
    except: import scipy
    try: argmax
    except: from numpy import argmax

    if blims == None: 
        blims=alims

    c = (scipy.ifft(scipy.fft(a[alims[0]:alims[1]])*scipy.conj(scipy.fft(b[blims[0]:blims[1]])))).real

    shift = argmax(c)

    if shift > len(a)/2.0 :
        shift = shift - len(a)

    if dispersion:
        shift = shift * dispersion

    return shift


def cross_correlate( flux_a, flux_b, wave_a, wave_b, window=None, subsample=2):
    """ Cross correlate two spectra in wavelength space
    """
    
    from scipy.interpolate import interp1d
    import numpy as np

    dispersion = np.median( (wave_a - np.roll(wave_a,1)) )
    
    #sub sample
    dispersion /= subsample

    flux_a, wave_a = linearize( flux_a, wave_a, dispersion )
    flux_b, wave_b = linearize( flux_b, wave_b, dispersion )

    index_a = np.where( (wave_a > window[0]) & (wave_a < window[1]) )[0]
    index_b = np.where( (wave_b > window[0]) & (wave_b < window[1]) )[0]

    shift = fft_correlate( flux_a[index_a], flux_b[index_b], dispersion=dispersion )

    return shift


def linearize( flux, wave, dispersion=None ):
    """ Return flux and wave arrays with a linear wavelength scale
    """
    from scipy.interpolate import interp1d
    import numpy as np

    interp_func = interp1d( wave, flux, 1 )

    if not dispersion:
        dispersion = np.median( (wave - np.roll(wave,1)) )

    out_wave = np.arange( wave.min(), wave.max(), dispersion )

    out_flux = interp_func( out_wave )

    return out_flux, out_wave

