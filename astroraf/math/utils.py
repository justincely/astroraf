__all__ = ['rebin','expand_direct','enlarge','blur_image','gauss_kern']


def gauss_kern(size, sizey=None):
    """ Returns a normalized 2D gauss kernel array for convolutions """

    import scipy

    size = int(size)

    if not sizey:
        sizey = size
    else:
        sizey = int(sizey)

    x, y = scipy.mgrid[-size:size+1, -sizey:sizey+1]
    g = scipy.exp(-(x**2/float(size)+y**2/float(sizey)))

    return g / g.sum()


def blur_image(im, n, ny=None):
    """
    blurs the image by convolving with a gaussian kernel of typical
    size n. The optional keyword argument ny allows for a different
    size in the y direction.
    
    """

    import scipy.signal
    from scipy.signal import convolve
    from . import gauss_kern

    g = gauss_kern(n, sizey=ny)
    improc = scipy.signal.convolve(im,g, mode='same')

    return improc


def rebin(a, bins=(2,2), mode='slice'):
    """
    Rebins input array using array slices
    
    """

    assert mode in ('slice','direct','weird','avg')
    y,x=a.shape
    ybin=bins[0]
    xbin=bins[1]
    assert (x%bins[1]==0),'X binning factor not factor of x.'
    assert (y%bins[0]==0),'Y binning factor not factor of y.'

    if mode=='slice':
    	#From Phil
        a=a[0:y-1:ybin]+a[1:y:ybin]
        a=a[:,0:x-1:xbin]+a[:,1:x:xbin]
	
    elif mode=='direct':
    	#Not tested, from me
        out_array=numpy.zeros((y,x))
        for i in range(y):
            for j in range(x):
                for k in range(bins[0]):
                    for l in range(bins[1]):
                        out_array[i,j]+=a[bins[0]*i+k,bins[1]*j+l]
	a=out_array
	
    elif mode=='avg':
    	#Not tested, from online
        try: sometrue
        except: from numpy import sometrue,mod
        assert len(a.shape) == len(newshape)
        assert not sometrue(mod( a.shape, newshape ))
        slices = [ slice(None,None, old/new) for old,new in zip(a.shape,newshape) ]
        a=a[slices]
	
    elif mode=='weird':
        #not tested, from internet
        shape=(y/bins[0],x/bins[1])
        sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
        a= a.reshape(sh).sum(-1).sum(1)
	
    return a
    

def expand_direct(a,bins=(2,2)):
    """
    Block expand input array
    
    """
    
    import numpy
    import os
    y,x=a.shape
    assert (x%bins[1]==0),'X binning factor not factor of x.'
    assert (y%bins[0]==0),'Y binning factor not factor of y.'
    out_array=numpy.zeros((y*bins[0],x*bins[1]))

    print 'Rebinning array'
    for i in range(y):
        done=100*float(i)/(y*bins[0])
        os.write(1,'\b\b\b\b\b\b%3.2f%%'%(done))
        for j in range(x):
            for k in range(bins[0]):
                for l in range(bins[1]):
                    out_array[bins[0]*i+k,bins[1]*j+l]=a[i,j]
    os.write(1,'\b\b\b\b\b\b%3.2f%%'%(100))
    print
    return out_array


def enlarge(a, x=2, y=None):
    """
    Enlarges 2D image array a using simple pixel repetition in both dimensions.
    Enlarges by factor x horizontally and factor y vertically.
    If y is left as None, uses factor x for both dimensions.

    """

    import numpy as np
    a = np.asarray(a)
    assert a.ndim == 2
    if y == None:
        y = x
    for factor in (x, y):
        assert factor.__class__ == int
        assert factor > 0
    return a.repeat(y, axis=0).repeat(x, axis=1)

