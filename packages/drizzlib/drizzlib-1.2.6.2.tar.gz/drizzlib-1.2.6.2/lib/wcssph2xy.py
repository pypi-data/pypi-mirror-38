
import numpy as n

#Defining Angle Constants
pi = n.pi
pi2 = n.pi/2.0
radeg = 180.0/pi

def wcssph2xy(longitude, latitude, map_type=0, ctype="", face="", pv2="", crval="", crxy="", longpole="", latpole="", north_offset="", south_offset=""):

    map_types=['DEF','AZP','TAN','SIN','STG','ARC','ZPN','ZEA','AIR','CYP',
               'CAR','MER','CEA','COP','COD','COE','COO','BON','PCO','SFL',
               'PAR','AIT','MOL','CSC','QSC','TSC', 'SZP']

    n_long = n.size(longitude)
    n_lat = n.size(latitude)
    projection_type = ""

    # Error Checking

    if n_long != n_lat:
        raise TypeError, 'ERROR - longitude and latitude do not have equal number of elements'

    if map_type and (map_type >= 0) and (map_type <= 25):
        projection_type=map_types[map_type]
    elif map_type:
        raise TypeError, 'ERROR - map_type must be >= 0 and <= 25'

    # Checking if ctype is set correctly

    if ctype != "":
        ctype = n.array(ctype)
        if n.size(ctype) >= 1:
            ctype1 = ctype[0]
            projection_type = str.upper(ctype1[5:8])

        if n.size(ctype) >= 2:
            ctype2 = ctype[1]
            if projection_type != str.upper(ctype2[5:8]):
                raise TypeError, 'ERROR - the same map projection type \
                must be in characters 5-8 of both CTYPE1 and CTYPE2.'
            if ((str.upper(ctype1[1:3]) == 'RA' and str.upper(ctype2[1,5]) != 'DEC') or
                (str.upper(ctype[1:5]) == 'GLON' and str.upper(ctype[1:5]) != 'GLAT') or
                (str.upper(ctype[1:5]) == 'ELON' and str.upper(ctype[1:5]) != 'ELAT') ):
                raise TypeError, 'The same standard system must be in the first 4 characters of both CTYPE1 and CTYPE2.'
            else:
                projection_type = 'DEF'

    if (projection_type == "") or (projection_type == "DEF"):
        projection_type = 'CAR'
        print('Projection type not supplied, set to default (Cartesian)')

    if (face != '') or (projection_type == 'CSC') or \
    (projection_type == 'QSC') or (projection_type == 'TSC'):
        if face == '': noface = 1
        else: noface = 0

    # Converting all longitude values into the range -180 to 180
    lng = n.array(longitude)
    lat = n.array(latitude)
    temp = n.where(lng >= 180.0)
    if n.size(temp):
        lng[temp] = lng[temp] - 360.0

    # Make small offsets at poles to allow the transformations to be
    # completely invertible.  These generally introduce a small fractional
    # error but only at the poles.  They are necessary since all maps
    # lose information at the poles when a rotation is applied, because
    # all points within NORTH_ or SOUTH_OFFSET of the poles are mapped to
    # the same points.

    if north_offset == "": north_offset = 1.0e-7
    if south_offset == "": south_offset = 1.0e-7

    bad = n.where(n.abs(lat - 90.0) < north_offset*radeg)

    badindex = n.array([])

    if n.size(bad) > 0:
        lat[bad] = 90.0 - north_offset*radeg
        badindex = bad

    bad = n.where(n.abs(lat + 90.0) < south_offset*radeg)

    if n.size(bad) > 0:
        lat[bad] = south_offset*radeg - 90.0
        badindex = n.sort(n.append(badindex, bad)).tolist()

    return x, y, badindex

if __name__ == '__main__':
