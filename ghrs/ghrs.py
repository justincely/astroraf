"""
Functions for dealing with GHRS data

"""

import glob
import pyfits
import numpy as np

class assemble:
    """
    Assemble GHRS fits files into a single MEF file

    """

    def __init__(self, rootname):
        
        rootname = rootname[:9]

        if not self._files_available( rootname ):
            raise IOError('Missing files')

        
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

        self._monotonize_all()


    def _files_available(self, rootname):
        """Check that all necessary files exist
        """

        all_files = glob.glob( rootname + '*.fits' )
                
        found_endings = set( [item[-8:-5] for item in all_files] )

        needed_endings = set( ['c0f', 'c1f', 'c2f', 'c3f',
                               'c4f', 'c5f'] )
        
        return needed_endings.issubset( found_endings )


    def _get_data(self, filename):
        """Grab the data from the given file
        """

        return pyfits.open( filename )[0].data.flatten() 


    def _monotonize_all(self):
        
        sorted_index = np.argsort( self.wavelength )
        
        self.wavelength = self.wavelength[ sorted_index ]
        self.flux = self.flux[ sorted_index ]
        self.error = self.error[ sorted_index ]
        self.background = self.background[ sorted_index ]
        self.dq = self.dq[ sorted_index ]


    def write(self, outname):
        pass
