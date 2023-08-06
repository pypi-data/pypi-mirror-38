"""Hazelbean relies on pygeoprocessing, but there are some cases where an optimal change requires duplicating some code. To minimize upgrading challenges
Hazelbean offers a few functions that reimplement pgp and by convention keep a similar funciton name with the change listed after the matched function name."""

import os, sys, time, math
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
import numpy as np
import numpy as numpy

import hazelbean as hb

# Key lines here: for convenience and cross-compatibility, I import pgp into the hb namespace
import pygeoprocessing as pgp
import pygeoprocessing.geoprocessing as gp
import pygeoprocessing.geoprocessing_core as gpc
from pygeoprocessing.geoprocessing import *
from pygeoprocessing.geoprocessing_core import *

L = hb.get_logger('geoprocessing')

def align_and_resize_raster_stack_ensuring_fit(
        base_raster_path_list, target_raster_path_list, resample_method_list,
        target_pixel_size, bounding_box_mode, base_vector_path_list=None,
        raster_align_index=None, ensure_fits=False, all_touched=False,
        gtiff_creation_options=hb.DEFAULT_GTIFF_CREATION_OPTIONS):
    """Generate rasters from a base such that they align geospatially.

    This function resizes base rasters that are in the same geospatial
    projection such that the result is an aligned stack of rasters that have
    the same cell size, dimensions, and bounding box. This is achieved by
    clipping or resizing the rasters to intersected, unioned, or equivocated
    bounding boxes of all the raster and vector input.

    Parameters:
        base_raster_path_list (list): a list of base raster paths that will
            be transformed and will be used to determine the target bounding
            box.
        target_raster_path_list (list): a list of raster paths that will be
            created to one-to-one map with `base_raster_path_list` as aligned
            versions of those original rasters.
        resample_method_list (list): a list of resampling methods which
            one to one map each path in `base_raster_path_list` during
            resizing.  Each element must be one of
            "nearest|bilinear|cubic|cubic_spline|lanczos|mode".
        target_pixel_size (tuple): the target raster's x and y pixel size
            example: [30, -30].
        bounding_box_mode (string): one of "union", "intersection", or
            a list of floats of the form [minx, miny, maxx, maxy].  Depending
            on the value, output extents are defined as the union,
            intersection, or the explicit bounding box.
        base_vector_path_list (list): a list of base vector paths whose
            bounding boxes will be used to determine the final bounding box
            of the raster stack if mode is 'union' or 'intersection'.  If mode
            is 'bb=[...]' then these vectors are not used in any calculation.
        raster_align_index (int): indicates the index of a
            raster in `base_raster_path_list` that the target rasters'
            bounding boxes pixels should align with.  This feature allows
            rasters whose raster dimensions are the same, but bounding boxes
            slightly shifted less than a pixel size to align with a desired
            grid layout.  If `None` then the bounding box of the target
            rasters is calculated as the precise intersection, union, or
            bounding box.
        gtiff_creation_options (list): list of strings that will be passed
            as GDAL "dataset" creation options to the GTIFF driver, or ignored
            if None.

    Returns:
        None
    """
    last_time = time.time()

    # make sure that the input lists are of the same length
    list_lengths = [
        len(base_raster_path_list), len(target_raster_path_list),
        len(resample_method_list)]
    if len(set(list_lengths)) != 1:
        raise ValueError(
            "base_raster_path_list, target_raster_path_list, and "
            "resample_method_list must be the same length "
            " current lengths are %s" % (str(list_lengths)))

    # we can accept 'union', 'intersection', or a 4 element list/tuple
    if bounding_box_mode not in ["union", "intersection"] and (
            not isinstance(bounding_box_mode, (list, tuple)) or
            len(bounding_box_mode) != 4):
        raise ValueError("Unknown bounding_box_mode %s" % (
            str(bounding_box_mode)))

    if ((raster_align_index is not None) and
            ((raster_align_index < 0) or
             (raster_align_index >= len(base_raster_path_list)))):
        raise ValueError(
            "Alignment index is out of bounds of the datasets index: %s"
            " n_elements %s" % (
                raster_align_index, len(base_raster_path_list)))

    raster_info_list = [
        get_raster_info(path) for path in base_raster_path_list]

    if base_vector_path_list is not None:
        vector_info_list = [
            get_vector_info(path) for path in base_vector_path_list]
    else:
        vector_info_list = []

    # get the literal or intersecting/unioned bounding box
    if isinstance(bounding_box_mode, (list, tuple)):
        target_bounding_box = bounding_box_mode
    else:
        # either intersection or union
        target_bounding_box = reduce(
            functools.partial(hb.merge_bounding_boxes, mode=bounding_box_mode),
            [info['bounding_box'] for info in
             (raster_info_list + vector_info_list)])

    if bounding_box_mode == "intersection" and (
            target_bounding_box[0] > target_bounding_box[2] or
            target_bounding_box[1] > target_bounding_box[3]):
        raise ValueError("The rasters' and vectors' intersection is empty "
                         "(not all rasters and vectors touch each other).")

    if raster_align_index is not None:
        if raster_align_index >= 0:
            # bounding box needs alignment
            align_bounding_box = (
                raster_info_list[raster_align_index]['bounding_box'])
            align_pixel_size = (
                raster_info_list[raster_align_index]['pixel_size'])
            # adjust bounding box so lower left corner aligns with a pixel in
            # raster[raster_align_index]
            target_rc = [
                math.ceil((target_bounding_box[2] - target_bounding_box[0]) / target_pixel_size[0]),
                math.floor((target_bounding_box[3] - target_bounding_box[1]) / target_pixel_size[1])
            ]

            original_bounding_box = list(target_bounding_box)

            for index in [0, 1]:
                n_pixels = int((target_bounding_box[index] - align_bounding_box[index]) / float(align_pixel_size[index]))

                target_bounding_box[index] = align_bounding_box[index] + (n_pixels * align_pixel_size[index])
                target_bounding_box[index + 2] = target_bounding_box[index] + target_rc[index] * target_pixel_size[index]

            if ensure_fits:
                # This addition to the core geoprocessing code was to fix the case where the alignment moved the target tif
                # up and to the left, but in a way that then trunkated 1 row/col on the bottom right, causing wrong-shape
                # raster_math errors.z
                if original_bounding_box[2] > target_bounding_box[2]:
                    target_bounding_box[2] += target_pixel_size[0]

                if original_bounding_box[3] > target_bounding_box[3]:
                    target_bounding_box[3] -= target_pixel_size[1]


    option_list = list(gtiff_creation_options)
    if all_touched:
        option_list.append("ALL_TOUCHED=TRUE")

    for index, (base_path, target_path, resample_method) in enumerate(zip(
            base_raster_path_list, target_raster_path_list,
            resample_method_list)):
        last_time = gp._invoke_timed_callback(
            last_time, lambda: L.info(
                "align_dataset_list aligning dataset %d of %d",
                index, len(base_raster_path_list)), hb.LOGGING_PERIOD)
        option_list = []

        # My replacement call to the older version
        hb.warp_raster_HAZELBEAN_REPLACEMENT(
            base_path, target_pixel_size,
            target_path, resample_method,
            target_bb=target_bounding_box,
            gtiff_creation_options=option_list)

        # # PGP Replacement: warp_was give gdal error.
        # gp.warp_raster(
        #     base_path, target_pixel_size,
        #     target_path, resample_method,
        #     target_bb=target_bounding_box,
        #     gtiff_creation_options=option_list)



def warp_raster_HAZELBEAN_REPLACEMENT(
        base_raster_path, target_pixel_size, target_raster_path,
        resample_method, target_bb=None, target_sr_wkt=None,
        gtiff_creation_options=hb.DEFAULT_GTIFF_CREATION_OPTIONS):
    """Resize/resample raster to desired pixel size, bbox and projection.

    Parameters:
        base_raster_path (string): path to base raster.
        target_pixel_size (list): a two element list or tuple indicating the
            x and y pixel size in projected units.
        target_raster_path (string): the location of the resized and
            resampled raster.
        resample_method (string): the resampling technique, one of
            "nearest|bilinear|cubic|cubic_spline|lanczos|mode"
        target_bb (list): if None, target bounding box is the same as the
            source bounding box.  Otherwise it's a list of float describing
            target bounding box in target coordinate system as
            [minx, miny, maxx, maxy].
        target_sr_wkt (string): if not None, desired target projection in Well
            Known Text format.
        gtiff_creation_options (list or tuple): list of strings that will be
            passed as GDAL "dataset" creation options to the GTIFF driver.

    Returns:
        None
    """
    base_raster = gdal.OpenEx(base_raster_path)
    base_sr = osr.SpatialReference()
    base_sr.ImportFromWkt(base_raster.GetProjection())

    if target_bb is None:
        target_bb = get_raster_info(base_raster_path)['bounding_box']
        # transform the target_bb if target_sr_wkt is not None
        if target_sr_wkt is not None:
            target_bb = transform_bounding_box(
                get_raster_info(base_raster_path)['bounding_box'],
                get_raster_info(base_raster_path)['projection'],
                target_sr_wkt)

    target_geotransform = [
        target_bb[0], target_pixel_size[0], 0.0, target_bb[1], 0.0,
        target_pixel_size[1]]

    # this handles a case of a negative pixel size in which case the raster
    # row will increase downward
    if target_pixel_size[0] < 0:
        target_geotransform[0] = target_bb[2]
    if target_pixel_size[1] < 0:
        target_geotransform[3] = target_bb[3]
    target_x_size = abs((target_bb[2] - target_bb[0]) / target_pixel_size[0])
    target_y_size = abs((target_bb[3] - target_bb[1]) / target_pixel_size[1])

    if target_x_size - int(target_x_size) > 0:
        # target_x_size = int(target_x_size) + 1
        target_x_size = int(target_x_size) + 1
    else:
        target_x_size = int(target_x_size)

    if target_y_size - int(target_y_size) > 0:
        target_y_size = int(target_y_size) + 1
    else:
        target_y_size = int(target_y_size)

    if target_x_size == 0:
        L.warn(
            "bounding_box is so small that x dimension rounds to 0; "
            "clamping to 1.")
        target_x_size = 1
    if target_y_size == 0:
        L.warn(
            "bounding_box is so small that y dimension rounds to 0; "
            "clamping to 1.")
        target_y_size = 1

    local_gtiff_creation_options = list(gtiff_creation_options)
    # PIXELTYPE is sometimes used to define signed vs. unsigned bytes and
    # the only place that is stored is in the IMAGE_STRUCTURE metadata
    # copy it over if it exists; get this info from the first band since
    # all bands have the same datatype
    base_band = base_raster.GetRasterBand(1)
    metadata = base_band.GetMetadata('IMAGE_STRUCTURE')
    if 'PIXELTYPE' in metadata:
        local_gtiff_creation_options.append(
            'PIXELTYPE=' + metadata['PIXELTYPE'])

    # make directory if it doesn't exist
    try:
        os.makedirs(os.path.dirname(target_raster_path))
    except OSError:
        pass
    gdal_driver = gdal.GetDriverByName('GTiff')

    target_raster = gdal_driver.Create(
        target_raster_path, target_x_size, target_y_size,
        base_raster.RasterCount, base_band.DataType,
        options=local_gtiff_creation_options)
    base_band = None

    for index in range(target_raster.RasterCount):
        base_nodata = base_raster.GetRasterBand(1 + index).GetNoDataValue()
        if base_nodata is not None:
            target_band = target_raster.GetRasterBand(1 + index)
            target_band.SetNoDataValue(base_nodata)
            target_band = None

    # Set the geotransform
    target_raster.SetGeoTransform(target_geotransform)
    if target_sr_wkt is None:
        target_sr_wkt = base_sr.ExportToWkt()
    target_raster.SetProjection(target_sr_wkt)

    # need to make this a closure so we get the current time and we can affect
    # state
    reproject_callback = _make_logger_callback(
        "ReprojectImage %.1f%% complete %s, psz_message '%s'")

    # Perform the projection/resampling
    gdal.ReprojectImage(
        base_raster, target_raster, base_sr.ExportToWkt(),
        target_sr_wkt, hb.RESAMPLE_DICT[resample_method], 0, 0,
        reproject_callback, [target_raster_path])

    target_raster = None
    base_raster = None
    calculate_raster_stats(target_raster_path)


def _make_logger_callback(message):
    """Build a timed logger callback that prints `message` replaced.

    Parameters:
        message (string): a string that expects 3 placement %% variables,
            first for % complete from `df_complete`, second `psz_message`
            and last is `p_progress_arg[0]`.

    Returns:
        Function with signature:
            logger_callback(df_complete, psz_message, p_progress_arg)
    """

    def logger_callback(df_complete, psz_message, p_progress_arg):
        """The argument names come from the GDAL API for callbacks."""
        try:
            current_time = time.time()
            if ((current_time - logger_callback.last_time) > 5.0 or
                    (df_complete == 1.0 and
                     logger_callback.total_time >= 5.0)):
                L.info(
                    message, df_complete * 100, p_progress_arg[0],
                    psz_message)
                logger_callback.last_time = current_time
                logger_callback.total_time += current_time
        except AttributeError:
            logger_callback.last_time = time.time()
            logger_callback.total_time = 0.0

    return logger_callback


def calculate_raster_stats(raster_path):
    """Calculate and set min, max, stdev, and mean for all bands in raster.

    Parameters:
        raster_path (string): a path to a GDAL raster raster that will be
            modified by having its band statistics set

    Returns:
        None
    """
    raster = gdal.OpenEx(raster_path, gdal.GA_Update)
    raster_properties = get_raster_info(raster_path)
    for band_index in range(raster.RasterCount):
        target_min = None
        target_max = None
        target_n = 0
        target_sum = 0.0
        for _, target_block in iterblocks(
                raster_path, band_index_list=[band_index + 1]):
            nodata_target = raster_properties['nodata'][band_index]
            # guard against an undefined nodata target
            valid_mask = numpy.ones(target_block.shape, dtype=bool)
            if nodata_target is not None:
                valid_mask[:] = target_block != nodata_target
            valid_block = target_block[valid_mask]
            if valid_block.size == 0:
                continue
            if target_min is None:
                # initialize first min/max
                target_min = target_max = valid_block[0]
            target_sum += numpy.sum(valid_block)
            target_min = min(numpy.min(valid_block), target_min)
            target_max = max(numpy.max(valid_block), target_max)
            target_n += valid_block.size

        if target_min is not None:
            target_mean = target_sum / float(target_n)
            stdev_sum = 0.0
            for _, target_block in iterblocks(
                    raster_path, band_index_list=[band_index + 1]):
                # guard against an undefined nodata target
                valid_mask = numpy.ones(target_block.shape, dtype=bool)
                if nodata_target is not None:
                    valid_mask = target_block != nodata_target
                valid_block = target_block[valid_mask]
                stdev_sum += numpy.sum((valid_block - target_mean) ** 2)
            target_stddev = (stdev_sum / float(target_n)) ** 0.5

            target_band = raster.GetRasterBand(band_index + 1)
            target_band.SetStatistics(
                float(target_min), float(target_max), float(target_mean),
                float(target_stddev))
            target_band = None
        else:
            L.warn(
                "Stats not calculated for %s band %d since no non-nodata "
                "pixels were found.", raster_path, band_index + 1)
    raster = None



