def gaussian(sigma=1,array_size=None,height=1):
    """
    Generate a gaussian kernal
    
    """

    from scipy.signal import gaussian as sp_gauss

    return height * sp_gauss( array_size, sigma )

