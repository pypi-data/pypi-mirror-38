# Core imports
from sys import getsizeof
from itertools import chain
from collections import deque

# Numpy is your best friend when you have to handle numerical arrays of data.
import numpy as np

# Healpy reads / writes to [HEALPix](http://healpix.sourceforge.net/) files.
import healpy as hp

from pympler.asizeof import asizeof

# Astropy offers some really nice FITS and conversion utils
# Our code requires astropy version >= 1.0
from astropy import units as u
from astropy.coordinates import SkyCoord, Galactic

# The TRUE Circle Constant (http://tauday.com/tau-manifesto).
TAU = np.pi * 2.


def _galactic2healpix(sky):
    """
    Acessing SkyCoord's properties is expensive, so we do it only once, and we
    also convert the coordinates to a spherical representation suitable
    for healpy. Also, note that sky's properties are Quantities, with Units,
    and so are the returned values of this function.
    """
    lats = (90. * u.degree - sky.b) * TAU / 360.  # 90 is for colatitude
    lngs = sky.l * TAU / 360.

    return [lats, lngs]


def _wpix2hpix(coords, wcs, frame):
    """
    From WCS pixel space (x/y) to HEALPix space (lat/lon).

    coords: ndarray
        Of shape (2, ...)

    Returns two Quantities, each of shape (...) matching the input `coords`.
    """
    # The order of the axes for the result is determined by the CTYPEia
    # keywords in the FITS header, therefore it may not always be of the
    # form (ra, dec). The lat, lng, lattyp and lngtyp members can be
    # used to determine the order of the axes.
    [lats, lngs] = wcs.all_pix2world(coords[0], coords[1], 0)
    sky = SkyCoord(lats, lngs, unit=u.degree, frame=frame)

    return _galactic2healpix(sky.transform_to(Galactic))


def _project_hpix_poly_to_wcs(nside, wcs, healpixs=None):
    """
    Return a list of lists of 4 (x, y) tuples, which are the coordinates of
    the vertices of the healpixels when projected into the `wcs` plane.
    """
    npix = hp.nside2npix(nside)
    if healpixs is None:
        healpixs = np.arange(npix)
    # Holder for the cartesian vertices of healpixs on the projection plane
    hpix_polys = [None] * npix
    # Collect the vector coordinates of the corners in the hp ref.
    # [ [x1, x2, ..., xn], [y1, y2, ..., yn], [z1, z2, ..., zn] ]
    corners_hp_vec = np.ndarray((3, len(healpixs) * 4))
    for i in range(len(healpixs)):
        # [ [x1, x2, x3, x4], [y1, y2, y3, y4], [z1, z2, z3, z4] ]
        corners = hp.boundaries(nside, healpixs[i])
        j = i*4
        corners_hp_vec[0][j:j+4] = corners[0]
        corners_hp_vec[1][j:j+4] = corners[1]
        corners_hp_vec[2][j:j+4] = corners[2]

    # Convert the corners into (theta, phi) (still in hp ref.)
    # [ [t1, t2, ..., tn], [p1, p2, ..., pn] ]
    corners_hp_ang = hp.vec2ang(np.transpose(corners_hp_vec))

    # Build the (expensive!) SkyCoord object with all our coords
    sky_b = -1 * (corners_hp_ang[0] * 360. / TAU - 90.)
    sky_l = corners_hp_ang[1] * 360. / TAU
    sky = SkyCoord(b=sky_b, l=sky_l, unit=u.degree, frame=Galactic)

    # Convert the corners to the WCS pixel space
    cors_gal_x, cors_gal_y = sky.to_pixel(wcs)

    # Store in memory the HEALPix polygons geometry in WCS pixel space
    for i in range(len(healpixs)):
        j = i*4
        # Finally, we make a list of (x, y) vertices in pixel referential,
        # which we index per healpixel id for later usage in the loop.
        hpix_poly = np.transpose([cors_gal_x[j:j+4], cors_gal_y[j:j+4]])
        hpix_polys[healpixs[i]] = hpix_poly

    return hpix_polys


def _mem(o):
    """
    Return the memory footprint of a variable, as a humanized string.
    """
    return _sizeof_fmt(asizeof(o))


def _total_sizeof(o):
    """
    Return the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {
        tuple: iter,
        list: iter,
        deque: iter,
        dict: dict_handler,
        set: iter,
        frozenset: iter,
    }
    seen = set()  # track which object id's have already been seen
    default_size = getsizeof(0)  # estimate sizeof object without __sizeof__

    def sizeof(_o):
        if id(_o) in seen:  # do not double count the same object
            return 0
        seen.add(id(_o))

        if isinstance(_o, np.ndarray):
            s = _o.nbytes
        else:
            s = getsizeof(_o, default_size)

        for typ, handler in all_handlers.items():
            if isinstance(_o, typ):
                s += sum(map(sizeof, handler(_o)))
                break
        return s

    return sizeof(o)


def _sizeof_fmt(num, suffix='o'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0

    return "%.1f%s%s" % (num, 'Yi', suffix)