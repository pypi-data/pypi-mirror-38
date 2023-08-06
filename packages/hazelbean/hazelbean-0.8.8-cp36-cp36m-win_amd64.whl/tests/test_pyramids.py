from unittest import TestCase
import os, sys, time

# NOTE Awkward inclusion heere so that I don't have to run the test via a setup config each  time
sys.path.extend(['../..'])

import hazelbean as hb
import pandas as pd
import numpy as np

class DataStructuresTester(TestCase):
    def setUp(self):
        self.global_5m_raster_path = 'data/ha_per_cell_5m.tif'
        self.global_1deg_raster_path = 'data/global_1deg_floats.tif'
        self.two_polygon_shapefile_path = 'data/two_poly_wgs84_aoi.shp'

    def tearDown(self):
        pass

    def test_load_geotiff_chunk_by_rc(self):

        hb.load_geotiff_chunk_by_cr(self.global_1deg_raster_path, 1, 2, 5, 5)

    def test_load_geotiff_chunk_by_latlon(self):
        input_path = self.global_5m_raster_path
        ul_lat = 40
        ul_lon = -93
        lat_size = .2
        lon_size = 1
        hb.load_geotiff_chunk_by_latlon(input_path, ul_lat, ul_lon, lat_size, lon_size)

    def test_add_rows_or_cols_to_geotiff(self):
        incomplete_array = hb.load_geotiff_chunk_by_latlon(self.global_1deg_raster_path, 80, -180, 150, 360)
        # TODO Here is an interesting starting point to assess the question of how to generalize AF as flex inputs. For now it is path based.
        temp_path = hb.temp('.tif', 'test_add_rows_or_cols_to_geotiff', False)
        geotransform_override = hb.get_raster_info(self.global_1deg_raster_path)['geotransform']
        geotransform_override = [-180, 1, 0, 80, 0, -1]
        n_rows_override = 150

        hb.save_array_as_geotiff(incomplete_array, temp_path, self.global_1deg_raster_path, geotransform_override=geotransform_override, n_rows_override=n_rows_override)
        r_above, r_below, c_above, c_below = 10, 20, 0, 0
        hb.add_rows_or_cols_to_geotiff(temp_path, r_above, r_below, c_above, c_below)
