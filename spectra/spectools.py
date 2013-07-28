
LIGHTSPEED = 2.9979E5

def wavelength_to_velocity(wavelength, zeropoint):
    zeropoint = float(zeropoint)

    z = (wavelength - float(zeropoint) ) / (zeropoint)
    #z2 = (1 + z) ** 2
    #velocity = ((z2 - 1 ) / (z + 1)) * LIGHTSPEED
    velocity = z * LIGHTSPEED

    return velocity


def velocity_to_wavelength(velocity, zeropoint):
    return zeropoint * velocity/LIGHTSPEED + zeropoint


def luminosity_distance(redshift,flux):
    PI = 3.14159
    distance = LIGHTSPEED * redshift
    luminosity = flux * PI * distance**2
  
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
    return float(obs_wave) / (redshift + 1)


def obs_wavelength(rest_wave,redshift):
    return float(rest_wave) * (redshift + 1)
