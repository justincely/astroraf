from astropy.io import fits as pyfits

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
