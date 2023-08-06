from nd import warp
from nd.io import from_netcdf
from nd.testing import generate_test_dataset
import numpy as np
from numpy.testing import assert_equal
import os


def test_warp_grid_shift():
    ds = generate_test_dataset(ntime=1)
    # [llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat]
    old_extent = [
        ds['lon'].min(),
        ds['lat'].min(),
        ds['lon'].max(),
        ds['lat'].max()
    ]
    new_extent = [
        ds['lon'].min() + 2,
        ds['lat'].min() + 2,
        ds['lon'].max() + 2,
        ds['lat'].max() + 2
    ]
    warped = warp.warp(ds, new_extent)


def test_get_extent():
    extent = (-10.0, 50.0, 0.0, 60.0)
    ds = generate_test_dataset(extent=extent)
    assert_equal(extent, warp._get_extent(ds))


def test_tie_points_to_gcps():
    pass


def test_fit_latlon():
    pass


def test_coord_transform():
    ll = np.meshgrid(
        np.linspace(50, 60, 20),
        np.linspace(-10, 0, 20)
    )
    pass


def test_common_extent_and_resolution():
    pass


def test_gdal_warp():
    pass


def test_resample():
    pass


def test_warp():
    pass


def test_warp_like():
    pass


def test_align(tmpdir):
    path = tmpdir.mkdir('aligned')
    # [llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat]
    extent1 = (-10, 50, 0, 60)
    extent2 = (-8, 52, 2, 62)
    ds1 = generate_test_dataset(extent=extent1)
    ds2 = generate_test_dataset(extent=extent2)
    warp.align([ds1, ds2], path)
    # Check whether the aligned files have been created
    assert_equal(os.listdir(path), ['data0_aligned.nc', 'data1_aligned.nc'])
    # Open the aligned files
    ds1_aligned = from_netcdf(str(path.join('data0_aligned.nc')))
    ds2_aligned = from_netcdf(str(path.join('data1_aligned.nc')))
    assert_equal(
        warp._get_extent(ds1_aligned),
        warp._get_extent(ds2_aligned)
    )
