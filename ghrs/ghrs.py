"""
Functions for dealing with GHRS data

"""

import glob
import pyfits

class assemble:
    """
    Assemble GHRS fits files into a single MEF file

    """

    def __init__(self, rootname):
        
        rootname = rootname[:9]

        if not self._files_available( rootname ):
            raise IOError('Missing files')

    def _files_available(self, rootname):
        """Check that all necessary files exist
        """

        all_files = glob.glob( rootname + '*.fits' )
                
        found_endings = set( [item[-8:-5] for item in all_files] )

        needed_endings = set( ['c0f', 'c1f', 'c2f', 'c3f',
                               'c4f', 'c5f'] )
        
        return needed_endings.issubset( found_endings )
