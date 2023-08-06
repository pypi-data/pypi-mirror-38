import os, sys, warnings, logging, inspect, math

from osgeo import gdal, osr, ogr
import numpy as np
import hazelbean as hb

L = hb.get_logger('pyramids', logging_level='warning')

def load_geotiff_chunk_by_cr(input_path, c=None, r=None, c_size=None, r_size=None, datatype=None):
    """Convenience function to load a chunk of an array given explicit row and column info."""
    ds = gdal.OpenEx(input_path)
    n_c, n_r = ds.RasterXSize, ds.RasterYSize

    if not 0 <= r <= n_r:
        raise NameError('r given to load_geotiff_chunk_by_cr didnt fit. r, n_r: ' + str(r) + ' ' + str(n_r))

    if not 0 <= c <= n_c:
        raise NameError('c given to load_geotiff_chunk_by_cr didnt fit. c, n_c: ' + str(c) + ' ' + str(n_c))

    if not 0 <= r + r_size <= n_r:
        raise NameError('r_size given to load_geotiff_chunk_by_cr didnt fit. r_size, n_r: ' + str(r_size) + ' ' + str(n_r))

    if not 0 <= c + c_size <= n_c:
        raise NameError('c given to load_geotiff_chunk_by_cr didnt fit. c, n_c: ' + str(c_size) + ' ' + str(n_c))

    a = ds.ReadAsArray(c, r, c_size, r_size, buf_type=datatype)

    return a

def load_geotiff_chunk_by_latlon(input_path, ul_lat, ul_lon, lat_size, lon_size, datatype=None):
    """Load a geotiff chunk as a numpy array from input_path. Requires that input_path be pyramid_ready. If datatype given,
    returns the numpy array by GDAL number, defaulting to the type the data was saved as."""
    hb.is_path_pyramid_ready(input_path)
    c, r, c_size, r_size = latlon_heightwidth_to_cr_widthheight(input_path, ul_lat, ul_lon, lat_size, lon_size)
    a = load_geotiff_chunk_by_cr(input_path, c, r, c_size, r_size, datatype)

    return a

def latlon_heightwidth_to_cr_widthheight(input_path, ul_lat, ul_lon, lat_size, lon_size):
    "gdal Open uses col, row, n_cols, n_row notation. This function converts lat lon bb to rc in this order based on the proportional size of the input_path."
    r, c = hb.latlon_to_rc(ul_lat, ul_lon, input_path)
    r_right, c_right = hb.latlon_to_rc(ul_lat - lat_size, ul_lon + lon_size, input_path)

    r_size = r_right - r
    c_size = c_right - c

    if c_size == 0 or r_size == 0:
        L.debug('Inputs given result in zero size: ' + str(c) + ' ' + str(r) + ' ' + str(c_size) + ' ' + str(r_size))

    return c, r, c_size, r_size


def latlon_to_rc(lat, lon, input_path):
    """Calcualte the row and column index from a raster at input_path for a given lat, lon value."""
    ds = gdal.OpenEx(input_path)
    n_c, n_r = ds.RasterXSize, ds.RasterYSize
    gt = ds.GetGeoTransform()

    ulx, xres, _, uly, _, yres = gt[0], gt[1], gt[2], gt[3], gt[4], gt[5]
    prop_r = (lat + 90.0) / 180.0
    prop_c = (lon + 180.0) / 360.0

    r = (1 - prop_r) * n_r
    c = prop_c * n_c

    r = round(r)
    c = round(c)

    verbose = False
    if verbose:
        print ('lat', lat, 'lon', lon, 'n_c', n_c, 'n_r', n_r, 'ulx', ulx, 'xres', xres, 'uly', uly, 'yres', yres, 'prop_r', prop_r, 'prop_c', prop_c, 'r', r, 'c', c)

    return r, c


def get_latlon_heightwidth_from_bb(input_bounding_box):
    """Convert bounding boxes in format [minx, miny, maxx, maxy], as used by pygeoprocessing get_vector_info and get_raster_info,
    into [ul_latitude, ul_longitude, latitude heigh, longitude height]. This format is useful for interfaces such as gdal ReadAsArray()
    which uses Col, Row, Width, Height notation. """
    to_return = input_bounding_box[3], input_bounding_box[0], input_bounding_box[3] - input_bounding_box[1], input_bounding_box[2] - input_bounding_box[0]
    return to_return

def is_path_pyramid_ready(input_path, raise_exception=False):
    """Throw exception if input_path is not pyramid-ready. This requires that the file be global, geographic projection, and with resolution
    that is a factor/multiple of arcdegrees."""
    ds = gdal.OpenEx(input_path)
    print('input_path', input_path)
    n_c, n_r = ds.RasterXSize, ds.RasterYSize
    gt = ds.GetGeoTransform()

    ulx, xres, _, uly, _, yres = gt[0], gt[1], gt[2], gt[3], gt[4], gt[5]

    if ulx != -180.0 or uly != 90.0:
        result_string = 'Input path not pyramid ready because UL not at -180 90: ' + str(input_path)
        if raise_exception:
            raise NameError(result_string)
        else:
            L.info(result_string)
            return False


    lrx = round(ulx + xres * n_c, 9)
    lry = round(uly + yres * n_r, 9)

    if lrx != 180.0 or lry != -90.0:

        result_string = 'Input path not pyramid ready because its not the right size: ' + str(input_path) + '\n    ulx ' + str(ulx) + ', xres ' + str(xres) + ', uly ' + str(uly) + ', yres ' + str(yres) + ', lrx ' + str(lrx) + ', lry ' + str(lry)
        if raise_exception:
            raise NameError(result_string)
        else:
            L.warning(result_string)
            return False

    # Passed all the tests, thus is pyramid-ready
    return True

def is_path_same_geotransform(input_path, match_path, raise_exception=False):
    """Throw exception if input_path is not the same geotransform as the match path."""
    ds = gdal.OpenEx(input_path)
    gt = ds.GetGeoTransform()

    ds_match = gdal.OpenEx(match_path)
    gt_match = ds_match.GetGeoTransform()

    if not gt == gt_match:
        result_string = 'Input path did not have the same geotransform as match path: ' + str(input_path) + ', ' + str(match_path)
        if raise_exception:
            raise NameError(result_string)
        else:
            L.warning(result_string)
            return False


    # Passed all the tests
    return True


def add_rows_or_cols_to_geotiff(input_path, r_above, r_below, c_left, c_right):

    ds = gdal.OpenEx(input_path)
    input_array = ds.ReadAsArray()
    gt = ds.GetGeoTransform()
    gt_out = list(gt)
    gt_out = [gt[0] + c_left, gt[1] - r_above, 0.0, 80.0, 0.0, gt[5]]

    n_rows = ds.RasterYSize + r_above + r_below
    n_cols = ds.RasterXSize + c_left + c_right
    output_array = np.full_like(input_array, ds.GetRasterBand(1).GetNoDataValue())


def get_aspect_ratio_of_two_arrays(coarse_res_array, fine_res_array):
    # Test that map resolutions are workable multiples of each other
    # assert int(round(fine_res_array.shape[0] / coarse_res_array.shape[0])) == int(
    #     round(fine_res_array.shape[1] / coarse_res_array.shape[1]))
    aspect_ratio = int(round(fine_res_array.shape[0] / coarse_res_array.shape[0]))
    return aspect_ratio


def calc_proportion_of_coarse_res_with_valid_fine_res(coarse_res, fine_res):
    """Useful wehn allocating to border cells."""

    if not isinstance(coarse_res, np.ndarray):
        try:
            coarse_res = hb.as_array(coarse_res).astype(np.float64)
        except:
            raise NameError('Unable to load ' + str(coarse_res) + ' as array in calc_proportion_of_coarse_res_with_valid_fine_res.')

    if not isinstance(fine_res, np.ndarray):
        try:
            fine_res = hb.as_array(fine_res).astype(np.int64)
        except:
            raise NameError('Unable to load ' + str(fine_res) + ' as array in calc_proportion_of_coarse_res_with_valid_fine_res.')

    aspect_ratio = get_aspect_ratio_of_two_arrays(coarse_res, fine_res)
    coarse_res_proportion_array = np.zeros(coarse_res.shape).astype(np.float64)
    fine_res_proportion_array = np.zeros(fine_res.shape).astype(np.float64)

    proportion_valid_fine_per_coarse_cell = hb.cython_calc_proportion_of_coarse_res_with_valid_fine_res(coarse_res, fine_res)

    return proportion_valid_fine_per_coarse_cell