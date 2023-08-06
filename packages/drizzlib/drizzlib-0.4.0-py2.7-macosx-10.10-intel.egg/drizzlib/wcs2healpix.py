# coding=utf-8

# Core imports
import os.path
import sys
from math import floor, ceil

# Forward compatibility
# Importing future breaks the line_profiler :(
# from future.builtins import range  # a generator

# Numpy is your best friend when you have to handle numerical arrays of data
import numpy as np

# Healpy reads / writes to [HEALPix](http://healpix.sourceforge.net/) files
# Documentation for query_disc and query_polygon can be found in the source :
# https://github.com/healpy/healpy/blob/master/healpy/src/_query_disc.pyx
import healpy as hp

# Astropy offers some really nice FITS and conversion utils
# This package requires astropy version >= 1.0
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import wcs_to_celestial_frame

# From our C extension `src/polyclip.c`, which stands for Polygon Clipping and
# helps us compute the area of intersection between WCS pixels and HEALPixels.
from polyclip import intersection_area

# Our private utils
from utils import TAU, _project_hpix_poly_to_wcs, _wpix2hpix, _mem, _sizeof_fmt

# TODO
# - [ ] Use logging module instead of print


# PRIVATE FUNCTIONS ###########################################################

def _log(something):
    print something


# PUBLIC FUNCTIONS ############################################################

# @profile
def wcs2healpix(wcs_files, nside=32, output=None, clobber=False,
                weights_cache=None, cache_dir=None, use_cache=True):
    """
    For each WCS image, project the healpixel grid in its plane, using the
    projection defined in the WCS, and for each healpixel, compute the weight
    of the contribution of each WCS pixel.
    Store the weights as geometry information in a file.
    For each healpixel, compute the weighed mean.
    Ouput the HEALPix file.

    wcs_files: str[]
        List of filepaths of input WCS FITS files to read from.
    nside: int
        Desired `nside` of the output HEALPix file.
    clobber: bool
        Should we overwrite the output file if it exists ?
    """

    def _use_cache():
        return cache_dir is not None and use_cache

    # Debug
    _log("Using Python %s" % sys.version)

    # Make sure we can write to the output file
    if os.path.isfile(output+'_healpix.fits') and not clobber:
        _log("The output file already exists! Set clobber=True to overwrite.")
        return None

    # Make sure the provided nside is OK
    if not hp.isnsideok(nside):
        _log("Provided nside (%d) is invalid. Provide a power of 2." % nside)
        return None

    # Prepare HEALPix data
    npix = hp.nside2npix(nside)
    _log("Number of pixels in the output HEALPix file : %d" % npix)

    # Prepare the geometry data (a dict)
    # The keys are the WCS filenames and the values are 2D maps of lists of
    # (hpix_id, weight) tuples.
    # Therefore, we know which healpixel affects which wcspixel for each file,
    # and how much, as it's a weighed mean.
    # weights = {}
    # _log("Weights initial memory footprint: %s." % _mem(weights))
    #
    # # The weights may be cached and restored, for performance
    # if weights_cache is None:
    #     weights_cache = {}
    #
    # not_cached_wcs_files = list(wcs_files)  # copy
    # for cached_file in weights_cache:
    #     not_cached_wcs_files.remove(cached_file)
    #     _log("Restoring WCS file '%s' data from cache." % cached_file)
    #     weights[cached_file] = weights_cache[cached_file]

    hpixs_values = np.zeros(npix)
    hpixs_weights = np.zeros(npix)

    for wcs_filepath in wcs_files:

        wcs_basename = os.path.basename(wcs_filepath)
        wcs_filename = wcs_basename.rsplit('.', 1)[0]  # remove extension

        _log("Handling WCS file '%s':" % wcs_filepath)

        # Read the settings from the WCS FITS file
        wcs_header = fits.getheader(wcs_filepath)
        wcs = WCS(wcs_header)
        # wcs.printwcs()
        # Extract the dimensions of the WCS image from the header
        x_dim = int(wcs_header['NAXIS1'])
        y_dim = int(wcs_header['NAXIS2'])
        wpix_cnt = x_dim * y_dim
        _log("  (x × y) : %d × %d = %d WCS pixels" % (x_dim, y_dim, wpix_cnt))

        # Guess the coordinates frame from the WCS header cards.
        # We highly rely on astropy, so this may choke on illegal headers.
        frame = wcs_to_celestial_frame(wcs)
        _log("  Coordinates frame : '%s'." % frame)

        # Pre-compute the HEALPix polygons, the
        # cartesian vertices of (all!) healpixs on the WCS projection plane.
        # We load them up from cache if there is a cached version.
        hpix_polys = None
        if _use_cache():
            hpix_polys_filepath = os.path.join(
                cache_dir, "%s_hpix_polys.npy" % wcs_filename
            )
            if os.path.isfile(hpix_polys_filepath):
                _log("  Loading %d HEALPix polygons from cache file '%s'..."
                     % (npix, hpix_polys_filepath))
                try:
                    hpix_polys = np.load(hpix_polys_filepath)
                except Exception, e:
                    _log("  FAILURE: %s" % e)
            else:
                _log("  No cache found for HEALPix polygons at '%s', "
                     "will compute them." % hpix_polys_filepath)
        if hpix_polys is None:
            _log("  Computing %d HEALPix polygons..." % npix)
            hpix_polys = _project_hpix_poly_to_wcs(nside, wcs)
            if cache_dir is not None:
                hpix_polys_filepath = os.path.join(
                    cache_dir, "%s_hpix_polys.npy" % wcs_filename
                )
                np.save(hpix_polys_filepath, hpix_polys)
                _log("  Wrote HEALPix polygons to file '%s'."
                     % hpix_polys_filepath)
        # _log("    Their memory footprint is %s." % _mem(hpix_polys))

        # Pre-compute the ranges
        # Python 2's range() is not a generator, so this works
        x_range = range(x_dim)
        y_range = range(y_dim)

        # Pre-compute the WCS polygons, the
        # cartesian vertices of all wcspixs on the WCS projection plane.
        # Load them up from cache if there is a cached version.
        wpix_polys = None
        if _use_cache():
            wpix_polys_filepath = os.path.join(
                cache_dir, "%s_%d_wpix_polys.npy" % (wcs_filename, nside)
            )
            if os.path.isfile(wpix_polys_filepath):
                _log("  Loading %d WCS polygons from cache file '%s'..."
                     % (wpix_cnt, wpix_polys_filepath))
                try:
                    wpix_polys = np.load(wpix_polys_filepath)
                except Exception, e:
                    _log("  FAILURE: %s" % e)
            else:
                _log("  No cache found for WCS polygons at '%s', "
                     "will compute them." % wpix_polys_filepath)
        if wpix_polys is None:
            wpix_polys = np.ndarray((y_dim, x_dim, 4, 2), dtype=float)
            _log("  Computing %d WCS polygons..." % wpix_cnt)
            for x in x_range:
                for y in y_range:
                    wpix_poly = np.array([
                        [x,     y],
                        [x,     y + 1],
                        [x + 1, y + 1],
                        [x + 1, y]
                    ])
                    wpix_polys[y, x] = wpix_poly
            if cache_dir is not None:
                wpix_polys_filepath = os.path.join(
                    cache_dir, "%s_%d_wpix_polys.npy" % (wcs_filename, nside)
                )
                np.save(wpix_polys_filepath, wpix_polys)
                _log("  Wrote WCS polygons to file '%s'."
                     % wpix_polys_filepath)
        # _log("    Their memory footprint is %s." % _mem(wpix_polys))

        # Define a (x, y) pair generator that skips WCS pixels that cannot
        # possibly intersect with the healpixel.
        def _each_wpix_for_hpix(_hpix_poly, x_limit, y_limit):
            x_y = np.transpose(_hpix_poly)
            x_min = int(max(floor(np.min(x_y[0])), 0))
            y_min = int(max(floor(np.min(x_y[1])), 0))
            x_max = int(min(ceil(np.max(x_y[0]) + 1), x_limit))
            y_max = int(min(ceil(np.max(x_y[1]) + 1), y_limit))

            for _x in range(x_min, x_max):
                for _y in range(y_min, y_max):
                    yield _x, _y

        # Weights (aka geometry info) for this WCS file.
        # Load them up from cache if there is a cached version.
        file_weights = None
        if _use_cache():
            weights_filepath = os.path.join(
                cache_dir, "%s_%d_weights.npy" % (wcs_filename, nside)
            )
            if os.path.isfile(weights_filepath):
                _log("  Loading weights from cache file '%s'..."
                     % weights_filepath)
                try:
                    file_weights = np.load(weights_filepath)
                except Exception, e:
                    _log("  FAILURE: %s" % e)
            else:
                _log("  No cache found for weights at '%s', "
                     "will compute them." % weights_filepath)

        if file_weights is None:
            # For each WCS pixel, a list of tuples (hpix_id, weight)
            file_weights = np.ndarray((y_dim, x_dim), dtype=list)

            # For each healpixel
            _log("  Computing weights of %d HEALPixels..." % npix)
            hpix_ids = range(npix)
            for hpix_id in hpix_ids:
                hpix_poly = hpix_polys[hpix_id]

                # Provide some feedback to the user
                # This slows the procedure quite a bit, actually.
                # _log("  Doing healpixel %d/%d (%.2f%%)"
                #      % (hpix_i+1, npix, 100.*(hpix_i+1)/npix))

                # For each WCS pixel close to the HEALPixel
                for x, y in _each_wpix_for_hpix(hpix_poly, x_dim, y_dim):

                    # Vertices of the WCS pixel in WCS pixel space
                    wpix_poly = wpix_polys[y, x]

                    # Optimized C implementation of Sutherland-Hodgeman
                    # `intersection_area` is defined in `src/polyclip.c`.
                    # This intersection is computed in WCS pixel space.
                    weight = intersection_area(hpix_poly, 4, wpix_poly, 4)

                    # Store the weight
                    if weight > 0:
                        if file_weights[y, x] is None:
                            file_weights[y, x] = []
                        file_weights[y, x].append((hpix_id, weight))

            # Store the geometry information to file
            if cache_dir is not None:
                weights_filepath = os.path.join(
                    cache_dir, "%s_%d_weights.npy" % (wcs_filename, nside)
                )
                _log("  Weights memory footprint : %s." % _mem(file_weights))
                np.save(weights_filepath, file_weights)
                _log("  Wrote weights to file '%s'." % weights_filepath)

        # Advance the computation of the mean
        shape = np.shape(file_weights)
        x_range = range(shape[1])
        y_range = range(shape[0])
        wcs_data = fits.getdata(wcs_filepath)
        _log("  Computing the weighted mean...")
        for x in x_range:
            for y in y_range:
                pix_weights = file_weights[y, x]
                if pix_weights is None:
                    continue
                for pix_weight in pix_weights:
                    hpix_i = pix_weight[0]
                    weight = pix_weight[1]
                    hpixs_values[hpix_i] += wcs_data[y, x] * weight
                    hpixs_weights[hpix_i] += weight

        # Free some memory
        del x_range, y_range
        del wcs_data
        del hpix_polys
        del wpix_polys
        del file_weights
        # weights[wcs_filepath] = file_weights

    # Store the geometry information to file
    # if output is not None:
        # np.save(output + '_geometry.npy', {
        #     'nside':   nside,
        #     'weights': weights,
        # })  # MemoryError ???
        # weights_file = '%s_%d_weights.npy' % (output, nside)
        # _log("Saving weights (%s in memory) to '%s'."
        #      % (_mem(weights), weights_file))
        # np.save(weights_file, weights)

    # Compute the weighted mean
    _log("Computing the final weighted mean...")
    # hpixs_values = np.zeros(npix)
    # hpixs_weights = np.zeros(npix)
    #
    # for wcs_filepath in wcs_files:
    #     file_weights = weights[wcs_filepath]
    #
    #     shape = np.shape(file_weights)
    #     # Pre-compute the ranges
    #     x_range = range(shape[1])
    #     y_range = range(shape[0])
    #     wcs_data = fits.getdata(wcs_filepath)
    #     for x in x_range:
    #         for y in y_range:
    #             pix_weights = file_weights[y, x]
    #             if pix_weights is None:
    #                 continue
    #             for pix_weight in pix_weights:
    #                 hpix_i = pix_weight[0]
    #                 weight = pix_weight[1]
    #                 hpixs_values[hpix_i] += wcs_data[y, x] * weight
    #                 hpixs_weights[hpix_i] += weight

    hpixs = hpixs_values / hpixs_weights

    if output is not None:
        hp.write_map(output+'_healpix.fits', hpixs)

    hp.mollview(map=hpixs)

    return hpixs


### FOR THE PROFILER ##########################################################

# $ pip install line_profiler
# add @profile before the function you want to profile, and then run :
# $ kernprof -v -l lib/wcs2healpix.py
# Warning: if you have `future` package installed, kernprof will fail.
if __name__ == "__main__":
    try:
        wcs2healpix(
            [
                'tests/wcs2healpix/set1/wcs/CHIPASS_Equ.fits',
                'tests/wcs2healpix/set1/wcs/CHIPASS_Gal_new.fits',
            ],
            nside=1024,
            output='tests/wcs2healpix/set1/result',
            clobber=True
        )
    except KeyboardInterrupt:
        pass