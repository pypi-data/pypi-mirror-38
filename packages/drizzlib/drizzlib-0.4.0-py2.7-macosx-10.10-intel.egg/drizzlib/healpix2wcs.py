# Core imports
import os.path
import sys

# Numpy is your best friend when you have to handle numerical arrays of data
import numpy as np

# Healpy reads / writes to [HEALPix](http://healpix.sourceforge.net/) files
# Documentation for query_disc and query_polygon can be found in the source :
# https://github.com/healpy/healpy/blob/master/healpy/src/_query_disc.pyx
import healpy as hp

# Astropy offers some really nice FITS and conversion utils
# This package requires astropy version >= 1.0
from astropy import units as u
from astropy.coordinates import SkyCoord, Galactic
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import wcs_to_celestial_frame

# From our C extension `src/polyclip.c`, which stands for Polygon Clipping and
# helps us compute the area of intersection between WCS pixels and HEALPixels.
from polyclip import intersection_area

# Our private utils
from utils import TAU, _wpix2hpix

# TODO
# - [ ] Use logging module instead of print


# PRIVATE FUNCTIONS ###########################################################

def _log(something):
    print something


# PUBLIC FUNCTIONS ############################################################

# This @profile annotation is for `line_profiler`, see the bottom of this file.
# @profile
def healpix2wcs(
        healpix,
        healpix_hdu=1,
        header=None,
        header_hdu=0,
        output=None,
        crpix=None, cdelt=None, crval=None, ctype=None, size=None,
        equinox=2000.,
        use_bilinear_interpolation=False,
        ignore_blank=True,
        clobber=False):
    """
    Extract a rectangular image in the WCS format from the provided HEALPix.
    The characteristics of the output WCS image are determined either by a
    provided header (which is a WCS FITS file path whose header cards we use),
    or directly using some parameters of this function.

    healpix: str
        The path to the input HEALPix file to read from.
    healpix_hdu: int
        The id of the HDU (Header Data Unit) to read in the HEALPix FITS file.
    header: file path, file object, or file-like object
        The (path to the) FITS file whose WCS header we want to read and use.
        If an opened file object, its mode must be one of the following :
        `rb`, `rb+`, or `ab+`.
    header_hdu: int
        The id of the HDU (Header Data Unit) to read in the header FITS file.
    output: str
        The path to the output FITS file that will be generated.
    crpix: float[2]
        Equivalent to the CRPIX FITS header card.
        A pair of floats, in the `Y,X` order.
        If you do not provide a header, you must provide this value.
    cdelt: float[2]
        Equivalent to the CDELT FITS header card.
        A pair of floats, in the `Y,X` order.
        If you do not provide a header, you must provide this value.
    crval: float[2]
        Equivalent to the CRVAL FITS header card.
        A pair of floats, in the `Y,X` order.
        If you do not provide a header, you must provide this value.
    ctype: str[2]
        Equivalent to the CRVAL FITS header card.
        A pair of strings, in the `Y,X` order.
        If you do not provide a header, you must provide this value.
    size: int[2]
        The desired size of the output image.
        A pair of integers, in the `Y,X` order.
        If you do not provide a header, you must provide this value.
    equinox: float
        Equivalent to the EQUINOX FITS header card.
        If you do not provide a header, you should provide this value.
    use_bilinear_interpolation: boolean
        Whether to use a simple bilinear interpolation instead of the more
        expensive surface-pondered mean.
    ignore_blank: boolean
        Whether or not to ignore the `BLANK` values in the input HEALPix.
        If no `BLANK` keyword is defined in the HEALPix FITS metadata, this has
        no effect.
    clobber: boolean
        Whether or not to overwrite (aka. clobber) the `output` file if it
        already exists.
    """
    if header is not None:
        # Read the settings from the WCS FITS file provided as header
        h = fits.getheader(header, header_hdu)
        w = WCS(h)
        # Extract the dimensions of the image from the header
        x_dim = h['NAXIS1']
        y_dim = h['NAXIS2']
    else:
        # User wants to provide the header cards directly as keyword arguments
        def _missing(_property, _type='number'):
            raise ValueError("Provide either a FITS filepath in `header=`, "
                             "or a pair of %ss in the property `%s=`."
                             % (_type, _property))
        if crpix is None:
            _missing('crpix')
        if cdelt is None:
            _missing('cdelt')
        if crval is None:
            _missing('crval')
        if ctype is None:
            _missing('ctype', 'string')
        if size is None:
            _missing('size')

        # Create a new WCS object from scratch
        w = WCS(naxis=2)
        w.wcs.crpix = crpix
        w.wcs.cdelt = cdelt
        w.wcs.crval = crval
        w.wcs.ctype = ctype
        w.wcs.equinox = equinox

        x_dim = size[1]
        y_dim = size[0]

    # Debug
    _log("Using Python %s" % sys.version)

    # Make sure we can write to the output file
    if os.path.isfile(output) and not clobber:
        print("The output file already exists! Set clobber=True to overwrite.")
        return

    # Read the input HEALPix FITS file.  /!\ Expensive operation !
    m, h = hp.read_map(healpix, h=True, hdu=healpix_hdu)

    # Define a private tool for accessing HEALPix header cards values
    def _get_hp_card(name):
        for t in h:
            if t[0] == name:
                return t[1]
        return None

    # Ignore BLANK values only if they are defined in the header
    blank = _get_hp_card('BLANK')  #or -32768
    if blank is None:
        ignore_blank = False
    if ignore_blank:
        _log("Ignoring BLANK HEALPixels of value %.0f." % blank)

    # Collect information about the HEALPix (it's faster to do this only once)
    nside = hp.get_nside(m)

    _log("%d HEALPixels in the whole map." % hp.get_map_size(m))

    # Guess the coordinates frame from the WCS header cards.
    # We highly rely on astropy here, so this may choke on illegal headers.
    frame = wcs_to_celestial_frame(w)
    _log("Coordinates frame is '%s'." % frame)

    # Sanitize
    x_dim = int(x_dim)
    y_dim = int(y_dim)

    # Instantiate the output data
    data = np.ndarray((y_dim, x_dim))

    ## FIRST PASS
    # Collect the HPX coordinates of the center and corners of each WCS pixel.
    # We use the corners to efficiently select the healpixels to drizzle for
    # each WCS pixel, in the third pass.
    x_center = np.ndarray((y_dim, x_dim))
    y_center = np.ndarray((y_dim, x_dim))
    x_corner = np.ndarray((4, y_dim, x_dim))
    y_corner = np.ndarray((4, y_dim, x_dim))
    pad = 0.5 * 1.05  # bigger, to compensate the non-affine transformation
    # WARNING: optimal padding (10% right now) has NOT been computed.
    #          if too low, results are incorrect
    #          if too high, performance suffers
    for x in range(x_dim):
        for y in range(y_dim):
            x_center[y, x] = x
            y_center[y, x] = y
            x_corner[:, y, x] = np.array([x-pad, x+pad, x+pad, x-pad])
            y_corner[:, y, x] = np.array([y+pad, y+pad, y-pad, y-pad])

    # Transforming coordinates to the Galactic referential is faster with
    # one SkyCoord object than with many, hence this first pass, which enables
    # us to vectorize the transformation.
    [lat_centers, lng_centers] = _wpix2hpix([x_center, y_center], w, frame)
    [lat_corners, lng_corners] = _wpix2hpix([x_corner, y_corner], w, frame)

    ## SECOND PASS
    if use_bilinear_interpolation:
        # SECOND PASS : bilinear interpolation is fast and easy, but it will
        # yield incorrect results in some edge cases.
        for x in range(int(x_dim)):
            for y in range(int(y_dim)):

                # Coordinates in HEALPix space of the center of this pixel
                # Those are Quantity objects, so we pick their `value`
                theta = lat_centers[y, x].value
                phi = lng_centers[y, x].value

                # Healpy's bilinear interpolation
                v_interp = hp.get_interp_val(m, theta, phi)

                data[y, x] = v_interp

    else:
        # Memoization holder for the cartesian vertices of healpixs on
        # the flat plane of the projection.
        hpix_polys = [None] * hp.get_map_size(m)
        # The above list initialization is much, much faster than :
        # hpix_polys = [None for _ in range(hp.get_map_size(m))]

        # SECOND PASS : as converting our healpix polygons into pixel coords
        # is really expensive (like 84% of total time), we vectorize it.
        # This means selecting beforehand the HEALPixels intersecting with our
        # WCS image, and we do that by creating a polygon around our WCS image,
        # and using that polygon with `healpy`'s `query_polygon` method.
        # This makes the code harder to understand, but also much faster.
        # As the referential change from HEALPix to WCS is non-affine, a simple
        # rectangle of the size of the WCS image is not sufficient, as it will
        # miss some HEALPixels.
        # So we (arbitrarily!) pad it to make it a little big bigger.
        pad = 0.05 * (x_dim+y_dim)/2.
        wrap_poly_vertices = np.transpose(np.array([
            [-0.5-pad,      -0.5-pad],
            [-0.5-pad,      y_dim-0.5+pad],
            [x_dim-0.5+pad, y_dim-0.5+pad],
            [x_dim-0.5+pad, -0.5-pad],
        ]))
        wrap_poly_hp = _wpix2hpix(wrap_poly_vertices, w, frame)
        wrap_poly_hp = hp.ang2vec([v.value for v in wrap_poly_hp[0]],
                                  [v.value for v in wrap_poly_hp[1]])
        wrap_healpixs = hp.query_polygon(nside, wrap_poly_hp, inclusive=True)

        _log("%d HEALPixels in the WCS wrapper polygon." % len(wrap_healpixs))

        # Collect the vector coordinates of the corners in the hp ref.
        # [ [x1, x2, ..., xn], [y1, y2, ..., yn], [z1, z2, ..., zn] ]
        corners_hp_vec = np.ndarray((3, len(wrap_healpixs) * 4))
        for i in range(len(wrap_healpixs)):
            # [ [x1, x2, x3, x4], [y1, y2, y3, y4], [z1, z2, z3, z4] ]
            corners = hp.boundaries(nside, wrap_healpixs[i])
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
        cors_gal_x, cors_gal_y = sky.to_pixel(w)

        # Store in memory the HEALPix polygons geometry in WCS pixel space
        for i in range(len(wrap_healpixs)):
            j = i*4
            # Finally, we make a list of (x, y) vertices in pixel referential,
            # which we index per healpixel id for later usage in the loop.
            hpix_poly = np.transpose([cors_gal_x[j:j+4], cors_gal_y[j:j+4]])
            hpix_polys[wrap_healpixs[i]] = hpix_poly

        # This plotting helps debugging the above optimization
        # wcs_pix_polys = []
        # for x in range(int(x_dim)):
        #     for y in range(int(y_dim)):
        #         wpix_poly = np.array([
        #             [x - 0.5, y + 0.5],
        #             [x - 0.5, y - 0.5],
        #             [x + 0.5, y - 0.5],
        #             [x + 0.5, y + 0.5],
        #         ])
        #         wcs_pix_polys.append(wpix_poly)
        # _dbg_plot_poly(hpix_polys, wcs_pix_polys)
        ######################################################

        # THIRD PASS : rasterize healpixels on the (finite) wcs grid,
        # picking a mean pondered by the intersection area.
        for x in range(int(x_dim)):
            for y in range(int(y_dim)):

                # Vertices of the WCS pixel in WCS pixel space (obvious!)
                wpix_poly = np.array([
                    [x - 0.5, y - 0.5],
                    [x - 0.5, y + 0.5],
                    [x + 0.5, y + 0.5],
                    [x + 0.5, y - 0.5],
                ])

                # Tallies to compute the weighted arithmetic mean
                total = 0
                value = 0

                # Coordinates in HEALPix space of the center of this pixel.
                # Those are Quantity objects, so we pick their `value`.
                # theta = lat_centers[y, x].value
                # phi = lng_centers[y, x].value
                # This works only if there is less than 8 healpixels to drizzle
                # hpix_ids = list(hp.get_all_neighbours(nside, theta, phi))
                # hpix_ids.append(hp.ang2pix(nside, theta, phi))

                # Instead, we find all the HEALPixels that intersect with a
                # polygon slightly bigger than the pixel, whose vertices were
                # computed in the first pass.
                wrap_pix = hp.ang2vec(lat_corners[:, y, x].value,
                                      lng_corners[:, y, x].value)
                hpix_ids = hp.query_polygon(nside, wrap_pix, inclusive=True)

                # This behaves differently between python versions, and even if
                # we figure it out, this should stay a print and not a logging.
                # print("\rPIXEL %s, %s" % (x, y),)

                for hpix_id in hpix_ids:

                    # Healpy might return -1 when not found, ignore those.
                    if hpix_id == -1:
                        continue

                    hpix_value = m[hpix_id]

                    # Ignore BLANK values if configuration allows.
                    if ignore_blank and hpix_value == blank:
                        continue

                    hpix_poly = hpix_polys[hpix_id]

                    if hpix_poly is None:
                        # Even though we try to precompute the polygons in one
                        # fell swoop to avoid the expensive instanciation of a
                        # SkyCoord object, some pixels fall through the cracks
                        # and need to be converted on the fly.
                        # It's okay if this happens a couple of times,
                        # but if it happens too often, we lose in performance.
                        _log("\nWarning: healpixel %s escaped optimization."
                             % hpix_id)

                        corners = hp.boundaries(nside, hpix_id)
                        theta_phi = hp.vec2ang(np.transpose(corners))

                        sky_b = -1 * (theta_phi[0] * 360. / TAU - 90.)
                        sky_l = theta_phi[1] * 360. / TAU
                        sky = SkyCoord(b=sky_b, l=sky_l, unit=u.degree,
                                       frame=Galactic)

                        # Finally, make a list of (x, y) in pixel referential
                        hpix_poly = np.transpose(sky.to_pixel(w))
                        # ...which we memoize
                        hpix_polys[hpix_id] = hpix_poly

                    # Optimized C implementation of Sutherland-Hodgeman
                    # `intersection_area` is defined in `src/polyclip.c`.
                    # The intersection is computed in pixel space.
                    shared_area = intersection_area(hpix_poly, 4,
                                                    wpix_poly, 4)

                    total += shared_area
                    value += shared_area * hpix_value

                if total != 0:
                    v_drizzle = value / total
                else:
                    v_drizzle = value
                    _log("Warning: Sum of weights at (%d, %d) is 0." % (x, y))

                data[y, x] = v_drizzle

        _log("\n")

    if output is not None:
        fits.writeto(output, data, clobber=clobber)

    return data


### UTILS #####################################################################


def _dbg_plot_poly(healpolygons, wcspolygons):
    """
    This debug tool can be used to plot the healpix polygons, and the wcs grid
    in surimposition.

    healpolygons:
        List of lists of 4 (x,y) tuples.
    wcspolygons:
        List of lists of 4 (x,y) tuples.
    """
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    import matplotlib.patches as patches

    fig = plt.figure()
    ax = fig.add_subplot(111)

    xmin = 0
    xmax = 1
    ymin = 0
    ymax = 1

    for polygon in healpolygons:

        if polygon is None:
            continue

        verts = list(polygon)
        length = len(verts)

        xy = np.transpose(verts)
        xmin = min(xmin, np.min(xy[0]))
        xmax = max(xmax, np.max(xy[0]))
        ymin = min(ymin, np.min(xy[1]))
        ymax = max(ymax, np.max(xy[1]))

        verts.append((0., 0.))

        codes = [Path.MOVETO]
        for j in range(length-1):
            codes.append(Path.LINETO)
        codes.append(Path.CLOSEPOLY)

        path = Path(verts, codes)

        patch = patches.PathPatch(path, facecolor='orange', lw=1)
        ax.add_patch(patch)

    for polygon in wcspolygons:

        verts = list(polygon)
        length = len(verts)

        xy = np.transpose(verts)
        xmin = min(xmin, np.min(xy[0]))
        xmax = max(xmax, np.max(xy[0]))
        ymin = min(ymin, np.min(xy[1]))
        ymax = max(ymax, np.max(xy[1]))

        verts.append((0., 0.))

        codes = [Path.MOVETO]
        for j in range(length-1):
            codes.append(Path.LINETO)
        codes.append(Path.CLOSEPOLY)

        path = Path(verts, codes)

        patch = patches.PathPatch(path, alpha=0.3, facecolor='blue', lw=1)
        ax.add_patch(patch)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    plt.show()


### FOR THE PROFILER ##########################################################

# $ pip install line_profiler
# add @profile before the function you want to profile, and then run :
# $ kernprof -v -l drizzlib.py
# if __name__ == "__main__":
#     try:
#         healpix2wcs(
#             'tests/healpix/HFI_SkyMap_857_2048_R1.10_nominal_ZodiCorrected.fits',
#             header='tests/wcs/iris_100_2000_21jun06_bpix.fits',
#             output='tests/wcs/test.fits',
#             clobber=True
#         )
#     except KeyboardInterrupt:
#         pass