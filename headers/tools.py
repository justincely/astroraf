
__all__ = ['key_exists','hselect']

import pyfits
import glob

def key_exists( header, keyword ):
    """ Check existance of keyword in given header
    """

    if keyword in header.keys():
        return True
    else:
        return False


def hselect( filename_list, keyword_list, extension='all', verbose=1 ):
    """ returns list of keyword values from header

    prints output as well if verbose is True
    """
    
    if ',' in filename_list:
        filename_list = filename_list.split( ',' )
    elif isinstance( filename_list, list ):
        pass
    else:
        filename_list = glob.glob( filename_list ) 

    if not isinstance( keyword_list,str ):
        raise Exception( "Keyword list must be a comma separated string" )
    
    keyword_list = keyword_list.split(',')

    all_info = []
    for filename in filename_list:
        hdu = pyfits.open( filename )

        if extension == 'all':
            extension_list = range( len( hdu ) )
        elif isinstance( extension, int ):
            extension_list = [ extension ]
        elif isinstance( extension, str ):
            extension_list = map( int, extension.split(',') )
        else:
            raise Exception( "extension not understood" )

        found_vals = []
        found_vals.append( filename )

        for kw in keyword_list:
            KEY_FOUND = False
            for ext in extension_list:
                if key_exists( hdu[ ext ].header, kw ):
                    KEY_FOUND = True
                    found_vals.append( hdu[ ext ].header[ kw ] )
                    break
            if not KEY_FOUND:
                found_vals.append( 'DNE' )

        if verbose:
            print '  '.join( map( str,found_vals) )
        all_info.append( found_vals )

    if len( all_info ) == 1:
        all_info = all_info[0]

    return all_info

