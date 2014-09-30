from astropy.io import fits as pyfits
import numpy as np

__all__ = [ 'remake_asn', 'read_asn' ]

def remake_asn( asn_name, member_ext='_x1d.fits', product_ext='_x1dsum.fits',
                allow_missing=False ):
    """
    Use the fpavg function to re-create the x1dsum

    """

    from calcos import fpavg
    import os

    if not 'lref' in os.environ:
        os.environ['lref'] = '/grp/hst/cdbs/lref/'
    asn_path, name = os.path.split(asn_name)
    members, product = read_asn(asn_name)

    all_members = [os.path.join(asn_path, item + member_ext) for item in members]
    missing_members = [ item for item in all_members if not os.path.exists(item) ]

    if len( missing_members ) and (not allow_missing):
        raise IOError( "The following members were not found\n %s"% 
                       (','.join( missing_members) ) )

    elif len( missing_members ) and allow_missing:
        members = [ item for item in all_members if not (item in missing_members) ]
    else:
        members = all_members


    if len( product ) > 2:
        raise IOError( 'Too many products' )
    else:
        product = os.path.join(asn_path, product[0] + product_ext)

    fpavg.fpAvgSpec( members, product)

    
def read_asn( asn_name ):
    """

    Reads in an input association table and returns a tuple
    of the members and products.
    
    Inputs:
        asn
        either string or open fits file

    Output:
        (list of members,list of products)
    """


    asn_data = pyfits.open( asn_name )

    members = [ line['MEMNAME'].lower() for line in asn_data['ASN'].data 
                if line['MEMTYPE'] == 'EXP-FP' ]
    products = [ line['MEMNAME'].lower() for line in asn_data['ASN'].data 
                 if line['MEMTYPE'] == 'PROD-FP' ]

    return members, products


def merge_asn(asn1, asn2, rootname):
    """Merge asn2 into asn2 as rootname_asn.fits

    Copied from the Appending Tables section of:
    https://pythonhosted.org/pyfits/users_guide/users_table.html
    """

    t1 = pyfits.open(asn1)
    t2 = pyfits.open(asn2)
    nrows1 = t1[1].data.shape[0]
    nrows2 = t2[1].data.shape[0]
    nrows = nrows1 + nrows2

    hdu = pyfits.BinTableHDU.from_columns(t1[1].columns, nrows=nrows)
    for colname in t1[1].columns.names:
        hdu.data[colname][nrows1:] = t2[1].data[colname]


    index = np.where(hdu.data['MEMTYPE'] == 'PROD-FP')[0]
    hdu.data['MEMPRSNT'][index[1:]] = False
    hdu.data['MEMTYPE'][index[1:]] = 'EXP-FP'
    hdu.data['MEMNAME'][index[0]] = rootname.upper()

    hdu.writeto('{}_asn.fits'.format(rootname))
