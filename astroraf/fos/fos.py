"""
Functions for dealing with FOS data

"""

import glob
from astropy.io import fits as pyfits
import numpy as np

from astroraf.spectra.spectools import cross_correlate

from pyraf import iraf
from iraf import stsdas, hst_calib, ctools

class assemble:
    """
    Assemble FOS fits files into a single MEF file

    """

    def __init__(self, rootname):
        
        rootname = rootname[:9]

        if not self._files_available( rootname ):
            raise IOError('Missing files')

        self.outname = rootname + '_x1d.fits'
        
        self.hdu = pyfits.open( rootname + '_c0f.fits' )

        self.wavelength_file = rootname + '_c0f.fits'
        self.flux_file = rootname + '_c1f.fits'
        self.error_file = rootname + '_c2f.fits'
        self.background_file = rootname + '_c5f.fits'
        self.dq_file = rootname + '_cqf.fits'

        self.wavelength = self._get_data( self.wavelength_file )
        self.flux = self._get_data( self.flux_file )
        self.error = self._get_data( self.error_file )
        self.background = self._get_data( self.background_file )
        self.dq = self._get_data( self.dq_file )

        

    def _files_available(self, rootname):
        """Check that all necessary files exist
        """

        all_files = glob.glob( rootname + '*.fits' )
                
        found_endings = set( [item[-8:-5] for item in all_files] )

        needed_endings = set( ['c0f', 'c1f', 'c2f',
                               'c4f', 'c5f'] )

        return needed_endings.issubset( found_endings )


    def _get_data(self, filename):
        """Grab the data from the given file
        """

        return np.array( [ array for array in pyfits.open( filename )[0].data ] )


    def _monotonize_all(self):
        """ Make sure all arrays are monotonically increasing with 
        wavelength.

        """

        sorted_index = np.argsort( self.wavelength )
        
        self.wavelength = self.wavelength[ sorted_index ]
        self.flux = self.flux[ sorted_index ]
        self.error = self.error[ sorted_index ]
        self.background = self.background[ sorted_index ]
        self.dq = self.dq[ sorted_index ]


    def write(self, outname=None, clobber=False):
        """ Write out to FITS file
        """

        if isinstance( outname, str ):
            self.outname = outname

        hdu_out = pyfits.HDUList(pyfits.PrimaryHDU())

        keyword_list = ['INSTRUME', 'DETECTOR', 
                        'ROOTNAME', 'TARGNAME', 
                        'RA_TARG', 'DEC_TARG', 'DATE-OBS', 'TIME-OBS',
                        'EXPSTART', 'EXPEND', 'EXPTIME',
                        'PROPOSID']

        for kw in keyword_list:
            hdu_out[0].header[kw] = self.hdu[0].header[kw]

        print self.wavelength.shape
        print len(self.wavelength) 
        try:
           rows, cols = self.wavelength.shape
           self.wavelength = self.wavelength[-1]
           self.flux = self.flux[-1]
           self.error = self.error[-1]
           self.background = self.background[-1]
           self.dq = self.dq[-1]
        except:
           pass

        wavelength_col = pyfits.Column('wavelength', 'D', 'second', array=self.wavelength)
        flux_col = pyfits.Column('flux', 'D', 'ergs/s', array=self.flux)
        error_col = pyfits.Column('error', 'D', 'counts', array=self.error)
        bkgnd_col = pyfits.Column('background', 'D', 'cnts', array=self.background)
        dq_col = pyfits.Column('dq', 'D', 'cnts', array=self.dq)

        tab = pyfits.new_table([wavelength_col, 
                               flux_col,
                               error_col,
                               bkgnd_col, 
                               dq_col])

        hdu_out.append(tab)
        #hdu_out[1].header['NELEM'] = array_size

        hdu_out.writeto(self.outname, clobber=clobber)  
        '''
        iraf.splice(self.outname, 
                    self.outname.replace('x1d', 'x1dsum'), 
                    sdqflags=16, 
                    wl_name='wavelength', 
                    flux_name='flux', 
                    sw_name='',
                    wgt_name='', 
                    spacing='coarse')
        '''
