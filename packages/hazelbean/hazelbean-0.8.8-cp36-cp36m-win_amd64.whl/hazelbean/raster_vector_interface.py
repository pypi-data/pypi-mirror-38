import os, sys, shutil, random, math, atexit, time
from collections import OrderedDict
import functools
from functools import reduce
from osgeo import gdal, osr, ogr
import numpy as np
import random
import multiprocessing
import multiprocessing.pool
import hazelbean as hb
import scipy
import geopandas as gpd
import warnings
import netCDF4
import logging
import matplotlib.pyplot as plt
import hazelbean as hb

# Conditional imports
try:
    import geoecon as ge
except:
    ge = None

numpy = np
L = hb.get_logger('hb_rasterstats')


def zonal_statistics_faster(input_raster, zone_shapefile_path):

    input_path = hb.get_flex_as_path(input_raster)
    base_raster_path_band = (input_path, 1)

    # Test that input_raster and shapefile are in the same projection. Sillyness results if not.
    hb.assert_gdal_paths_in_same_projection([input_raster, zone_shapefile_path])

    start = time.time()
    r = hb.zonal_statistics(
        base_raster_path_band, zone_shapefile_path,
        aggregate_layer_name=None, ignore_nodata=True,
        polygons_might_overlap=True, working_dir=None)
    print(r)
    print('duration: ' + str(time.time() - start))

def zonal_statistics_rasterized(zones_path_or_array, values_path_or_array, zones_ndv=None, values_ndv=None, zones_dtype=None, values_dtype=None):
    """
    Calculate zonal statistics using a pre-generated raster ID array.

    :param zones_array:
    :param values_array:
    :param zones_ndv:
    :param values_ndv:
    :return:
    """

    # NOTE Everything currently forces to 64bit floats and ints.

    if type(zones_path_or_array) is str:
        if not zones_dtype:
            zones_dtype = hb.get_datatype_from_uri(zones_path_or_array)
        if not zones_ndv:
            zones_ndv = np.float64(hb.get_nodata_from_uri(zones_path_or_array))
            if zones_ndv is None:
                zones_ndv = np.float64(hb.default_no_data_values_by_gdal_number[zones_dtype])
        zones_array = hb.as_array(values_path_or_array).astype(hb.gdal_number_to_numpy_type[values_dtype])

    elif type(zones_path_or_array) is np.ndarray:
        zones_dtype = hb.numpy_type_to_gdal_number[zones_path_or_array.dtype]
        zones_ndv = np.float64(hb.default_no_data_values_by_gdal_number[zones_dtype])
        zones_array = zones_path_or_array.astype(hb.gdal_number_to_numpy_type[zones_dtype])

    else:
        raise TypeError('Unknown array type given to zones_path_or_array')

    if type(values_path_or_array) is str:
        if not values_dtype:
            values_dtype = hb.get_datatype_from_uri(values_path_or_array)
        if not values_ndv:
            values_ndv = np.float64(hb.get_nodata_from_uri(values_path_or_array))
            if values_ndv is None:
                values_ndv = np.float64(hb.default_no_data_values_by_gdal_number[values_dtype])
        values_array = hb.as_array(values_path_or_array).astype(hb.gdal_number_to_numpy_type[values_dtype])

    elif type(values_path_or_array) is np.ndarray:
        values_dtype = hb.numpy_type_to_gdal_number[values_path_or_array.dtype]
        values_ndv = np.float64(hb.default_no_data_values_by_gdal_number[values_dtype])
        values_array = values_path_or_array.astype(hb.gdal_number_to_numpy_type[values_dtype])

    else:
        raise TypeError('Unknown array type given to values_path_or_array')

    if zones_path_or_array.shape != values_path_or_array.shape:
        raise NameError('The zones array size is not the same as the values array. Zones: ' + str(zones_array.shape) + ' Values: ' + str(values_array.shape))

    if values_dtype <= 5:
        unique_ids, sums, counts = hb.zonal_stats_64bit_int_values(zones_array, values_array, zones_ndv, values_ndv)
    elif values_dtype == 6:
        unique_ids, sums, counts = hb.zonal_stats_64bit_float_values(zones_array, values_array, zones_ndv, values_ndv)
    elif values_dtype == 7:
        # Concurrency problem here? One solution: put pauses before and after cython calls? that seems horrible.
        # TODO HACK
        zones_array_int = zones_array.astype(np.int64)
        zones_ndv_int = np.int64(zones_ndv)
        unique_ids, sums, counts = hb.zonal_stats_64bit_float_values(zones_array_int, values_array, zones_ndv_int, values_ndv)
    else:
        raise TypeError('data type of values not understood.')

    zones_path_or_array = None
    values_path_or_array = None
    zones_array = None
    values_array = None

    return unique_ids, sums, counts


























