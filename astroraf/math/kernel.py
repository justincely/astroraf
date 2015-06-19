def gaussian(sigma=1,array_size=None,normed=True):
    """
    Generate a gaussian kernal
    
    """

    from scipy.signal import gaussian as sp_gauss

    window = sp_gauss( array_size, sigma )

    if normed:
        window /= window.sum()

    return window

